import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

brand = 'bmw'
model = '530'
initial_year = '2000'
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

while True:
    # Construct the URL with the dynamic variables and current page
    url = f'{base_url}/lst/{brand}/{model}?atype=C&cy=F&desc=0&fregfrom={initial_year}&fregto={final_year}&kmfrom={initial_km}&kmto={final_km}&powerfrom={initial_power}&powerto={final_power}&powertype={power_type}&pricefrom={price_from}&priceto={price_to}&search_id=zlebw2rdlq&sort=standard&source=listpage_pagination&ustate=N%2CU&page={current_page}'

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
