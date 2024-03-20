import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import database_service as db
import mapping_service as ms

def scrape_cars(filters):
    brand = filters['brand']
    model = filters['model']
    fuel_type = filters['fuel']
    initial_year = filters['initial_year']
    final_year = filters['final_year']
    initial_km = filters['initial_km']
    final_km = filters['final_km']
    initial_power = filters['initial_power']
    final_power = filters['final_power']
    power_type = filters['power_type']
    price_from = filters['price_from']
    price_to = filters['price_to']

    base_url = 'https://www.autoscout24.fr'

    # Initialize variables for page iteration
    current_page = 1

    car_details = []

    search_filters = [
        (brand, f'/{brand}'),
        (model, f'/{model}'),
        (fuel_type, f'fuel={fuel_type}&'),
        (initial_year, f'fregfrom={initial_year}&'),
        (final_year, f'fregto={final_year}&'),
        (initial_km, f'kmfrom={initial_km}&'),
        (final_km, f'kmto={final_km}&'),
        (initial_power, f'powerfrom={initial_power}&powertype={power_type}&'),
        (final_power, f'powerto={final_power}&'),
        (price_from, f'pricefrom={price_from}&'),
        (price_to, f'priceto={price_to}&')
    ]

    car_links = []

    while True:
        url = base_url + '/lst'

        # Flag to keep track of whether a '?' has been added
        sort_order_added = False
        add_sort_order = False

        for filter_value, filter_url in search_filters:
            if filter_value is brand and not filter_value and not sort_order_added:
                url += '?atype=C&cy=F&desc=0&'
                sort_order_added = True
            if filter_value is model and not sort_order_added:
                add_sort_order = True
            url += filter_url if filter_value else ''
            if add_sort_order:
                url += '?atype=C&cy=F&desc=0&'
                add_sort_order = False

        url += f'&search_id=zlebw2rdlq&sort=standard&source=listpage_pagination&ustate=N%2CU&page={current_page}'

        # print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # add current page car links to the array
        car_links.extend(soup.find_all(
            'a', class_='ListItem_title__ndA4s ListItem_title_new_design__QIU2b Link_link__Ajn7I'))
        
        # Check if there are more pages
        pagination = soup.find('div', class_='ListPage_pagination__4Vw9q')
        if not pagination:
            break

        # Move to the next page
        current_page += 1

    for link in car_links:
        car_url = urljoin(base_url, link['href'])
        car_response = requests.get(car_url)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')
        script_tag = car_soup.find('script', type='application/ld+json')

        if script_tag:
            carburant_title_div = car_soup.find('div', class_='VehicleOverview_itemTitle__S2_lb', string='Carburant')

            # Check if the "Carburant" title div is found
            if carburant_title_div:
                # Find the next sibling div element that contains the actual fuel information
                carburant_value_div = carburant_title_div.find_next_sibling('div', class_='VehicleOverview_itemText__AI4dA')
                
                # Extract and print the fuel information text
                if carburant_value_div:
                    fuel = carburant_value_div.get_text(strip=True)

            else:
                print("Title 'Carburant' not found in the HTML content")
                ignore_car = True

            json_data = script_tag.string.strip()
            car_info = json.loads(json_data)
            try:
                enginePower = car_info['offers']['itemOffered']['vehicleEngine'][0]['enginePower'][0].get('value', None)
            except:
                enginePower = None

            try:
                engineDisplacement = car_info['offers']['itemOffered']['vehicleEngine'][0].get('engineDisplacement', {}).get('value', None)
                ignore_car = False
            except:
                engineDisplacement = None
                ignore_car = True   

            try:
                emissionsCO2 = car_info['offers']['itemOffered'].get('emissionsCO2', None)
            except:
                emissionsCO2 = 0

            engineDetails = {
                'enginePower': enginePower,
                'engineDisplacement': engineDisplacement,
                'emissionsCO2': emissionsCO2,
                'fuelType': ms.get_fuel_type(fuel) if fuel else 'Unknown' 
            }

            try:
                mileage = {
                    'value': int(car_info['offers']['itemOffered']['mileageFromOdometer'].get('value', None)),
                    'unitCode': car_info['offers']['itemOffered']['mileageFromOdometer'].get('unitText', None)
                }
                ignore_car = False
            except:
                mileage = {
                    'value': 0,
                    'unitCode': "KMT"
                }
                ignore_car = True

            try:
                production_date = car_info['offers']['itemOffered'].get(
                    'productionDate', None).split('-')[0]
                ignore_car = False
            except:
                production_date = None
                ignore_car = True

            if not ignore_car:
                # Simplify the car_info object to include selected fields
                simplified_info = {
                    'brand': car_info['brand'].get('name', None),
                    'name': car_info['name'],
                    'price': {
                        'value': car_info['offers']['price'],
                        'currency': car_info['offers']['priceCurrency']
                    },
                    'url': car_url,
                    'address': {
                        'streetAddress': car_info['offers'].get('offeredBy', {}).get('address', {}).get('streetAddress', None),
                    },
                    'car_details': {
                        'name': car_info['offers']['itemOffered']['name'],
                        'manufacturer': car_info['offers']['itemOffered'].get('manufacturer', None),
                        'model': car_info['offers']['itemOffered'].get('model', None),
                        'productionDate': production_date,
                        'mileage': mileage,
                        'engineDetails': engineDetails,
                    }
                }
                car_details.append(simplified_info)

    # Save car_details to a file named "car_details.json"
    with open('car_details_as.json', 'w') as file:
        json.dump(car_details, file, indent=2)

    db_name = "autoscout24"
    collection_name = "car_details"
    client = db.connect_db(db_name)
    db.write_to_db(client, db_name, collection_name, car_details)

    print("Car details saved to car_details_as.json and database")
