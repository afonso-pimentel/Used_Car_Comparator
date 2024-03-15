import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import database_service as db
import mapping_service as ms

def scrape_cars(filters):
    brand = filters['brand']
    model = ''
    sub_model = filters['model']
    initial_year = filters['initial_year']
    final_year = filters['final_year']
    initial_km = filters['initial_km']
    final_km = filters['final_km']
    initial_power = filters['initial_power']
    final_power = filters['final_power']
    power_type = filters['power_type']
    price_from = filters['price_from']
    price_to = filters['price_to']

    base_url = 'https://www.standvirtual.com'


    def extract_numeric_value(string):
        parts = string.split(' ')
        if len(parts) > 0:
            if len(parts) == 3:
                numeric_string = ''.join(filter(str.isdigit, parts[0] + parts[1]))
            else:
                numeric_string = ''.join(filter(str.isdigit, parts[0]))
            if numeric_string:
                return int(numeric_string)
        return None


    # Initialize variables for page iteration
    current_page = 1

    car_details = []

    # List of search filters and their corresponding values
    search_filters = [
        (brand, f'/{brand}'),
        (sub_model, f'/{sub_model}'),
        (initial_year, f'/desde-{initial_year}?'),
        (model, f'search%5Bfilter_enum_engine_code%5D={model}&'),
        (initial_power, f'search%5Bfilter_float_engine_power%3Afrom%5D={initial_power}&'),
        (final_power, f'search%5Bfilter_float_engine_power%3Ato%5D={final_power}&'),
        (final_year, f'search%5Bfilter_float_first_registration_year%3Ato%5D={final_year}&'),
        (initial_km, f'search%5Bfilter_float_mileage%3Afrom%5D={initial_km}&'),
        (final_km, f'search%5Bfilter_float_mileage%3Ato%5D={final_km}&'),
        (price_from, f'search%5Bfilter_float_price%3Afrom%5D={price_from}&'),
        (price_to, f'search%5Bfilter_float_price%3Ato%5D={price_to}&')
    ]

    car_links = []
    
    while True:
        # Construct the URL with the dynamic variables and current page
        url = f'{base_url}/carros'

        # Flag to keep track of whether a '?' has been added
        question_mark_added = False

        # Iterate over the search filters and add them to the URL if the value is not empty
        for filter_value, filter_url in search_filters:
            if filter_value:
                if filter_value == initial_year:
                    question_mark_added = True
                if 'search' in filter_url and not question_mark_added:
                    url += '?'
                    question_mark_added = True
                url += filter_url

        url += f'search%5Badvanced_search_expanded%5D=true&page={current_page}'

        # Construct the URL with the dynamic variables and current page
        # url = f'{base_url}/carros/{brand}/{sub_model}/desde-?{initial_year}?search%5Bfilter_enum_engine_code%5D={model}&search%5Bfilter_float_engine_power%3Afrom%5D={initial_power}&search%5Bfilter_float_engine_power%3Ato%5D={final_power}&search%5Bfilter_float_first_registration_year%3Ato%5D={final_year}&search%5Bfilter_float_mileage%3Afrom%5D={initial_km}&search%5Bfilter_float_mileage%3Ato%5D={final_km}&search%5Bfilter_float_price%3Afrom%5D={price_from}&search%5Bfilter_float_price%3Ato%5D={price_to}&search%5Bfilter_enum_engine_code%5D={model}&page={current_page}&search%5Badvanced_search_expanded%5D=true'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the current page car links
        current_page_car_links = soup.find_all(
            'h1', class_="ekwd5px9 ooa-1ed90th er34gjf0")
        
        # print(url)

        # Extract the href attribute from the <a> elements and store them in the car_links array
        for car_link in current_page_car_links:
            a_tag = car_link.find('a')
            href = a_tag.get('href')
            car_links.append(href)

        # Check if there are more pages
        next_page_button = soup.find('li', {'title': 'Next Page'})
        if next_page_button is None:
            break
        else:
            # Check if the next page button is disabled
            pagination = next_page_button.get('aria-disabled', 'false')
            if pagination == 'true':
                # If the next page button is disabled, it means we are on the last page
                break

        # Move to the next page
        current_page += 1
    

    for link in car_links:
        car_response = requests.get(link)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')

        engine_power = "-1"
        displacement = "-1"
        emissions_co2 = "-1"

        # Find all ul elements with class "advert-details-item"
        car_name_elem = car_soup.find(class_='offer-title big-text ezl3qpx2 ooa-ebtemw er34gjf0')
        if(not car_name_elem):
            break
        else:
            car_name = car_name_elem.get_text(strip=True)
            car_price = car_soup.find(class_='offer-price__number eqdspoq4 ooa-o7wv9s er34gjf0').get_text(strip=True) + " €"
            detail_list = car_soup.select('[data-testid="advert-details-item"]')

            # Iterate over the detail_list
            for detail_item in detail_list:
                # Find the li elements within the current ul element
                # value of the title
                item_title = detail_item.find(class_='e18eslyg4 ooa-12b2ph5')
                # value of the item
                item_value = detail_item.find(class_='e16lfxpc0 ooa-1pe3502 er34gjf0')

                # Search for the desired information within the li elements
                if item_title and item_title.get_text(strip=True) == 'Marca':
                    if(not item_value):
                        item_value = detail_item.find(class_='e16lfxpc1 ooa-1ftbcn2')
                    brand = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Modelo':
                    if(not item_value):
                        item_value = detail_item.find(class_='e16lfxpc1 ooa-1ftbcn2')
                    model = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Combustível':
                    if(not item_value):
                        item_value = detail_item.find(class_='e16lfxpc1 ooa-1ftbcn2')
                    fuel = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Quilómetros':
                    mileage = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Cilindrada':
                    displacement = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Potência':
                    engine_power = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Emissões CO2':  
                    emissions_co2 = item_value.get_text(strip=True)
                if item_title and item_title.get_text(strip=True) == 'Ano':
                    productionYear = item_value.get_text(strip=True)

            address = car_soup.select_one(
                '#content-seller-area-section > div.ooa-yd8sa2.ep9j6b612 > div > a')

            engineDetails = {
                'enginePower': extract_numeric_value(engine_power),
                'engineDisplacement': extract_numeric_value(displacement),
                'emissionsCO2': extract_numeric_value(emissions_co2),
                'fuelType': ms.get_fuel_type(fuel) if fuel else 'Unknown'
            }

            mileage = {
                'value': extract_numeric_value(mileage),
                'unitCode': "KMT"
            }

            # Simplify the car_info object to include selected fields
            simplified_info = {
                'brand': brand,
                'name': car_name,
                'price': {
                    'value': extract_numeric_value(car_price),
                    'currency': "EUR"
                },
                'url': link,
                'address': {
                    'streetAddress': address.get_text(strip=True),
                },
                'car_details': {
                    'name': car_name,
                    'manufacturer': brand,
                    'model': model,
                    'productionDate': productionYear,
                    'mileage': mileage,
                    'engineDetails': engineDetails,
                }
            }

            car_details.append(simplified_info)

    # Save car_details to a file named "car_details.json"
    with open('car_details_sv.json', 'w') as file:
        json.dump(car_details, file, indent=2)

    db_name = "standvirtual"
    collection_name = "car_details"
    client = db.connect_db(db_name)
    db.write_to_db(client, db_name, collection_name, car_details)

    print("Car details saved to car_details_sv.json and to the database")
