import json
from urllib.parse import urljoin
import database_service as db
import autoscout as as24
from isv_calculator import calculateIsv
import standvirtual as sv
import execjs


MILEAGE_THRESHOLD = 60000

def scrape_used_cars(filters):
    # filters = {
    #     "brand": "mini",
    #     "model": "",
    #     "initial_year": "2008",
    #     "final_year": "",
    #     "initial_km": "",
    #     "final_km": "200000",
    #     "initial_power": "150",
    #     "final_power": "",
    #     "power_type": "",
    #     "price_from": ""
    # }
    clean_option = input("Do you want to clean the database before getting best deals? (y/n): ").strip().lower()
    if clean_option == 'y':
        print("Cleaning the database...\n")
        db_name = "autoscout24"
        collection_name = "car_details"
        client = db.connect_db(db_name) 
        db.clean_db(client, db_name, collection_name)

        db_name = "standvirtual"
        collection_name = "car_details"
        client = db.connect_db(db_name) 
        db.clean_db(client, db_name, collection_name)
        print("Database was cleaned.\n")
    elif clean_option == 'n':
        print("Adding cars to the database...\n")
    else:
        print("Invalid choice. Please enter 'y' or 'n'.\n")

    # Read the content of the JSON file
    with open('fuel_types.json', 'r') as file:
        fuel_types = json.load(file)

    filters_autoscout = {
        "brand": filters['brand'],
        "model": filters['model'],
        "fuel": fuel_types[filters['fuel']][0],
        "initial_year": filters['initial_year'],
        "final_year": filters['final_year'],
        "initial_km": filters['initial_km'],
        "final_km": filters['final_km'],
        "initial_power": filters['initial_power'],
        "final_power": filters['final_power'],
        "power_type": filters['power_type'],
        "price_from": filters['price_from'],
        "price_to": filters['price_to_autoscout']
    }

    filters_standvirtual = {
        "brand": filters['brand'],
        "model": filters['model'],
        "fuel": fuel_types[filters['fuel']][1],
        "initial_year": filters['initial_year'],
        "final_year": filters['final_year'],
        "initial_km": filters['initial_km'],
        "final_km": filters['final_km'],
        "initial_power": filters['initial_power'],
        "final_power": filters['final_power'],
        "power_type": filters['power_type'],
        "price_from": filters['price_from'],
        "price_to": filters['price_to_standvirtual']    
    }

    while True:
        scrape_as = input("Do you want to scrape Autoscout cars?: (y/n)\n")
        if scrape_as == 'y':
            print("Getting Autoscout cars...\n")
            as24.scrape_cars(filters_autoscout)
            break
        elif scrape_as == 'n':
            break      
        else:
            print("Invalid choice. Please try again.\n")

    while True:
        scrape_sv = input("Do you want to scrape Standvirtual cars?: (y/n)\n")
        if scrape_sv == 'y':
            print("Getting Standivrtual cars...\n")
            sv.scrape_cars(filters_standvirtual)
            break
        elif scrape_sv == 'n':
            break      
        else:
            print("Invalid choice. Please try again.\n") 
    
    

def get_best_deals():
    client_autoscout24 = db.connect_db("autoscout24")
    client_standvirtual = db.connect_db("standvirtual")
    cheapest_cars_autoscout24 = get_cheapest_cars(client_autoscout24,"autoscout24")
    best_deals = []
    seen_cars = set()


    for car in cheapest_cars_autoscout24:
        brand = car['_id']['brand']
        model = car['_id']['model']
        year = car['_id']['year']
        autoscout24_price = car['cheapest_price']
        fuel_type = car['car_details']['car_details']['engineDetails']['fuelType']
        engine_displacement = car['car_details']['car_details']['engineDetails']['engineDisplacement']
        engine_power = car['car_details']['car_details']['engineDetails']['enginePower']
        emissions = car['car_details']['car_details']['engineDetails']['emissionsCO2']
        mileage = car['car_details']['car_details']['mileage']['value']
        autoscout24_url = car['url']

        model_str = str(model)

        query = { "brand": brand,
            "car_details.model": {"$regex": model_str, "$options": 'i'},
            "car_details.productionDate": {"$gte": str(int(year) - 1), "$lte": str(int(year) + 1)},
            "car_details.mileage.value": {"$gte": mileage - MILEAGE_THRESHOLD, "$lte": mileage + MILEAGE_THRESHOLD},
            "car_details.engineDetails.fuelType": fuel_type,
            "car_details.engineDetails.engineDisplacement": {"$gte": engine_displacement*0.95, "$lte": engine_displacement*1.05} if engine_displacement else engine_displacement,
            "car_details.engineDetails.enginePower": {"$gte": engine_power*0.95, "$lte": engine_power*1.05}
        }
                
        similar_cars_standvirtual = db.find_one(client_standvirtual, "standvirtual", "car_details", query)
        
        for sv_car in similar_cars_standvirtual:
            sv_price = sv_car['price']['value']
            sv_url = sv_car['url']
            sv_emissions = sv_car['car_details']['engineDetails']['emissionsCO2']
            if not emissions:
                emissions = sv_emissions

            # Create a unique identifier for this car
            car_id = (brand, model, year, sv_price)

            totalPrice = calculateIsv(engine_displacement, emissions, fuel_type, autoscout24_price, int(year))

            print(totalPrice)

            if totalPrice and totalPrice < sv_price:

                price_diff = sv_price - totalPrice
                # Check if the car is already in the list
                if car_id not in seen_cars:
                    seen_cars.add(car_id)
                    best_deals.append({
                        "brand": brand,
                        "model": model,
                        "fuel_type": fuel_type,
                        "engine_displacement": engine_displacement,
                        "engine_power": engine_power,
                        "emissions": emissions if emissions else "no info", 
                        "production_year": int(year),
                        "standvirtual_price": sv_price,
                        "autoscout24_price": autoscout24_price,
                        "mileage": mileage,
                        "standvirtual_url": sv_url,
                        "autoscout24_url": autoscout24_url,
                        "price_with_isv": totalPrice,
                        "price_difference": price_diff
                    })

    # Sort the best deals by the price difference in descending order
    best_deals_sorted = sorted(best_deals, key=lambda x: x['price_difference'], reverse=True)
    
    # Save car_details to a file named "best_deals.json"
    with open('best_deals.json', 'w') as file:
        json.dump(best_deals_sorted, file, indent=2)
    print("Best deals written to best_deals.json")
    return

def get_cheapest_cars(client, db_name):
    pipeline = [
        {
            "$sort": {
                "brand": 1,
                "car_details.model": 1,
                "car_details.productionDate": 1,
                "price.value": 1
            }
        },
        {
            "$group": {
                "_id": {
                    "brand": "$brand",
                    "model": "$car_details.model",
                    "year": "$car_details.productionDate"
                },
                "cheapest_price": {"$first": "$price.value"},
                "engine_displacement": {"$first": "$car_details.engineDetails.engineDisplacement"},
                "engine_power": {"$first": "$car_details.engineDetails.enginePower"},
                "fuel_type": {"$first": "$car_details.engineDetails.fuelType"},
                "car_details": {"$first": "$$ROOT"},
                "url": {"$first": "$url"}
            }
        }
    ]
    collection_name = "car_details"
    return db.read_from_db(client, db_name, collection_name, pipeline)