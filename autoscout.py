import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

brand = 'bmw'
model = '120'
initial_year = ''
final_year = '2023'
initial_km = '10000'
final_km = '175000'
initial_power = '54'
final_power = '294'
power_type = 'hp'
price_from = '1500'
price_to = '40000'

base_url = 'https://www.autoscout24.fr'

# Initialize variables for page iteration
current_page = 1

car_details = []

search_filters = [
    (brand, f'/{brand}'),
    (model, f'/{model}'),
    (initial_year, f'fregfrom={initial_year}&'),
    (final_year, f'fregto={final_year}&'),
    (initial_km, f'kmfrom={initial_km}&'),
    (final_km, f'kmto={final_km}&'),
    (initial_power, f'powerfrom={initial_power}&powertype={power_type}&'),
    (final_power, f'powerto={final_power}&'),
    (price_from, f'pricefrom={price_from}&'),
    (price_to, f'priceto={price_to}&')
]

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

    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    car_links = soup.find_all(
        'a', class_='ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l')

    for link in car_links:
        car_url = urljoin(base_url, link['href'])
        car_response = requests.get(car_url)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')
        script_tag = car_soup.find('script', type='application/ld+json')

        if script_tag:
            json_data = script_tag.string.strip()
            car_info = json.loads(json_data)

            engineDetails = {
                'enginePower': car_info['offers']['itemOffered']['vehicleEngine'][0]['enginePower'][0].get('value', None),
                'engineDisplacement': car_info['offers']['itemOffered']['vehicleEngine'][0].get('engineDisplacement', {}).get('value', None),
                'emissionsCO2': car_info['offers']['itemOffered'].get('emissionsCO2', None)
            }

            mileage = {
                'value': int(car_info['offers']['itemOffered']['mileageFromOdometer'].get('value', None)),
                'unitCode': car_info['offers']['itemOffered']['mileageFromOdometer'].get('unitText', None)
            }

            production_date = car_info['offers']['itemOffered'].get(
                'productionDate', None).split('-')[0]

            # Simplify the car_info object to include selected fields
            simplified_info = {
                'brand': car_info['brand'].get('name', None),
                'name': car_info['name'],
                'price': {
                    'value': car_info['offers']['price'],
                    'currency': car_info['offers']['priceCurrency']
                },
                'url': car_info['offers']['url'],
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

    # Check if there are more pages
    pagination = soup.find('div', class_='ListPage_pagination__v_4ci')
    if not pagination:
        break

    # Move to the next page
    current_page += 1

# Save car_details to a file named "car_details.json"
with open('car_details_as.json', 'w') as file:
    json.dump(car_details, file, indent=2)

print("Car details saved to car_details_as.json")
