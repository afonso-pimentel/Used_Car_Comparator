import requests
from bs4 import BeautifulSoup
import json

# Step 1: Extract car brand codes
url = 'https://suchen.mobile.de/fahrzeuge/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

brand_codes = {}
brand_elements = soup.find_all('ul', class_='brand-model-list')
for brand_element in brand_elements:
    brand = brand_element.find('span', class_='brand').text.strip()
    brand_code = brand_element.find('span', class_='brand')['data-makeid']
    brand_codes[brand] = brand_code

# # Step 2: Define filter structure and map car brands to codes
# filters = {
#     'makeModelVariant1.makeId': brand_codes,
#     'makeModelVariant1.modelId': {}
# }

page_number = 1  # Replace with the desired page number


# Step 3 and 4: Extract item details and iterate through search result pages
brand_code = '1900'  # Replace with the extracted brand code for 'Audi'
model_code = '9' # Replace with the extracted model code for 'A4'
initial_year = '2001' # Replace with the desired initial year
final_year = '2018' # Replace with the desired final year
initial_km = '50000' # Replace with the desired initial km
final_km = '125000' # Replace with the desired final km
initial_power = '66' # Replace with the desired initial power
final_power = '146' # Replace with the desired final power
power_type = 'kw' 
price_from = '3500' # Replace with the desired initial price
price_to = '7500' # Replace with the desired final price

base_url = 'https://suchen.mobile.de/fahrzeuge/search.html'

# List of search filters and their corresponding values
search_filters = [
    ('dam', '0'),
    ('fr', f'{initial_year}:{final_year}'),
    ('isSearchRequest', 'true'),
    ('ml', f'{initial_km}:{final_km}'),
    ('ms', f'{brand_code};{model_code};;;;'),
    ('p', f'{price_from}:{price_to}'),
    ('pw', f'{initial_power}:{final_power}'),
    ('ref', 'dsp'),
    ('s', 'Car'),
    ('vc', 'Car')
]


while True:
    # Construct the URL with the dynamic variables
    url = base_url + '?'
    
    # Iterate over the search filters and add them to the URL
    for filter_name, filter_value in search_filters:
        url += f'{filter_name}={filter_value}&'

    # Add the page number to the URL
    url += f'pageNumber={page_number}'

    # Perform the search and extract item details
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    
    car_details = []
    car_links = []

    # Extract item details from the search result page
    item_elements = soup.find_all('div', class_='cBox-body--resultitem')

    for item_element in item_elements:
        car_link = item_element.find('a', class_='link--muted')['href']
        car_links.append(car_link)
        
    for link in car_links:
        car_response = requests.get(link)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')
        script_tag = car_soup.find('script', type='application/ld+json')

        if script_tag:
            json_data = script_tag.string
            
            if json_data and '"@type":"Car"' in json_data:
                car_info = json.loads(json_data)
                
        item = {}

        productionDate = car_details_element.find('div', id='firstRegistration-v').text.strip()

        engineDetails = {
                    'enginePower': int(car_details_element.find('div', id='power-v').text.strip().split()[0]),
                    'engineDisplacement': int(car_details_element.find('div', id='cubicCapacity-v').text.strip().replace('.', '').split()[0]),
                    'emissionsCO2': int(car_details_element.find('div', id='envkv.emission-v').text.strip().split()[0])
            }

        mileage = {
                    'value': int(car_info['mileageFromOdometer'].get('value', None).strip().replace('.', '').split()[0]),
                    'unitCode': car_info['mileageFromOdometer'].get('unitText', None)
                }

        price_element = item_element.find('span', class_='h3', attrs={'data-testid': 'prime-price'})
        if price_element:
            item['price'] = {
                'value': int(car_info['offers']['priceSpecification']['price']),
                'currency': car_info['offers']['priceSpecification']['priceCurrency']
            }

        address_element = item_element.find('p', id='seller-address')
        if address_element:
            item['address'] = {'streetAddress': address_element.text.strip()}
        
        car_details_element = item_element.find('div', id='td-box')
        if car_details_element:
            item['car_details'] = {
                'name': car_info['name'],
                'manufacturer': brand,
                'model': car_info['model'],
                'productionDate': productionDate,
                'mileage': mileage,
                'engineDetails': engineDetails
            }

        car_details.append(item)

    # Check if there are more pages to iterate through
    next_page_element = soup.find('a', class_='page-link next')
    if next_page_element:
        page_number += 1
    else:
        break

# Save car_details to a file named "car_details_md.json"
with open('car_details_md.json', 'w') as file:
    json.dump(car_details, file, indent=2)

print("Car details saved to car_details_md.json")