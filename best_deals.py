import json
from urllib.parse import urljoin
import database_service as db
import autoscout as as24
import standvirtual as sv

MILEAGE_THRESHOLD = 10000

def scrape_used_cars():
    filters = {
        "brand": "audi",
        "model": "",
        "initial_year": "2010",
        "final_year": "",
        "initial_km": "",
        "final_km": "150000",
        "initial_power": "",
        "final_power": "",
        "power_type": "",
        "price_from": ""
    }

    filters_autoscout = {
        "brand": filters['brand'],
        "model": filters['model'],
        "initial_year": filters['initial_year'],
        "final_year": filters['final_year'],
        "initial_km": filters['initial_km'],
        "final_km": filters['final_km'],
        "initial_power": filters['initial_power'],
        "final_power": filters['final_power'],
        "power_type": filters['power_type'],
        "price_from": filters['price_from'],
        "price_to": "15000"
    }

    filters_standvirtual = {
        "brand": filters['brand'],
        "model": filters['model'],
        "initial_year": filters['initial_year'],
        "final_year": filters['final_year'],
        "initial_km": filters['initial_km'],
        "final_km": filters['final_km'],
        "initial_power": filters['initial_power'],
        "final_power": filters['final_power'],
        "power_type": filters['power_type'],
        "price_from": filters['price_from'],
        "price_to": "25000"
    }

    as24.scrape_cars(filters_autoscout)
    sv.scrape_cars(filters_standvirtual)

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
        mileage = car['car_details']['car_details']['mileage']['value']
        autoscout24_url = car['url']

        model_str = str(model)
        
        similar_cars_standvirtual = db.find_one(client_standvirtual, "standvirtual", "car_details", {
            "brand": brand,
            "car_details.model": {"$regex": model_str, "$options": 'i'},
            "car_details.productionDate": year,
            "car_details.mileage.value": {"$gte": mileage - MILEAGE_THRESHOLD, "$lte": mileage + MILEAGE_THRESHOLD},
            "car_details.engineDetails.fuelType": fuel_type
        })
        
        for sv_car in similar_cars_standvirtual:
            sv_price = sv_car['price']['value']
            sv_url = sv_car['url']
            price_diff = sv_price - autoscout24_price

            # Create a unique identifier for this car
            car_id = (brand, model, year, sv_price)

            # Check if the car is already in the list
            if car_id not in seen_cars:
                seen_cars.add(car_id)
                best_deals.append({
                    "brand": brand,
                    "model": model,
                    "fuel_type": fuel_type, 
                    "production_year": year,
                    "standvirtual_price": sv_price,
                    "autoscout24_price": autoscout24_price,
                    "price_difference": price_diff,
                    "mileage": mileage,
                    "standvirtual_url": sv_url,
                    "autoscout24_url": autoscout24_url
                })

    # Sort the best deals by the price difference in descending order
    best_deals_sorted = sorted(best_deals, key=lambda x: x['price_difference'], reverse=True)
    return best_deals_sorted

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
                "fuel_type": {"$first": "$car_details.engineDetails.fuelType"},
                "car_details": {"$first": "$$ROOT"},
                "url": {"$first": "$url"}
            }
        }
    ]
    collection_name = "car_details"
    return db.read_from_db(client, db_name, collection_name, pipeline)

# Scrape used cars from autoscout24 and standvirtual
# scrape_used_cars()

# Get the best deals
best_deals = get_best_deals()

# Save car_details to a file named "best_deals.json"
with open('best_deals.json', 'w') as file:
    json.dump(best_deals, file, indent=2)
print("Best deals written to best_deals.json")
