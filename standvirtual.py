import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

brand = 'bmw'
model = 'serie-3'
sub_model = '320'
initial_year = '2000'
final_year = '2023'
initial_km = '10000'
final_km = '175000'
initial_power = '50'
final_power = '294'
power_type = 'hp'
price_from = '1500'
price_to = '30000'

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

while True:

    # Construct the URL with the dynamic variables and current page
    url = f'{base_url}/carros/{brand}/{sub_model}/desde-?{initial_year}?search%5Bfilter_enum_engine_code%5D={model}&search%5Bfilter_float_engine_power%3Afrom%5D={initial_power}&search%5Bfilter_float_engine_power%3Ato%5D={final_power}&search%5Bfilter_float_first_registration_year%3Ato%5D={final_year}&search%5Bfilter_float_mileage%3Afrom%5D={initial_km}&search%5Bfilter_float_mileage%3Ato%5D={final_km}&search%5Bfilter_float_price%3Afrom%5D={price_from}&search%5Bfilter_float_price%3Ato%5D={price_to}&search%5Bfilter_enum_engine_code%5D={model}&page={current_page}&search%5Badvanced_search_expanded%5D=true'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the h2 elements with the specified class
    h2_elements = soup.find_all(
        'h2', attrs={'data-testid': 'ad-title'})

    # Extract the href attribute from the <a> elements and store them in the car_links array
    car_links = []
    for h2 in h2_elements:
        a_tag = h2.find('a')
        href = a_tag.get('href')
        car_links.append(href)

    for link in car_links:
        car_response = requests.get(link)
        car_soup = BeautifulSoup(car_response.content, 'html.parser')
        script_tag = car_soup.find('script', type='application/ld+json')

        # Find the ul element
        ul_element = car_soup.select_one('#parameters > ul:nth-child(1)')

        engine_power = "-1"
        displacement = "-1"
        emissions_co2 = "-1"

        # Find the li element containing "Potência" span
        for li_element in ul_element.find_all('li'):
            span_element = li_element.find('span')
            if span_element and span_element.get_text(strip=True) == 'Cilindrada':
                displacement_element = li_element.find(
                    class_='offer-params__value')
                displacement = displacement_element.get_text(strip=True)
            if span_element and span_element.get_text(strip=True) == 'Potência':
                engine_power_element = li_element.find(
                    class_='offer-params__value')
                engine_power = engine_power_element.get_text(strip=True)
            if span_element and span_element.get_text(strip=True) == 'Emissões CO2':
                emissions_element = li_element.find(
                    class_='offer-params__value')
                emissions_co2 = emissions_element.get_text(strip=True)
                break

        address = car_soup.select_one(
            '#seller-bottom-info > div > section > section.seller-bottom-info__map.collapsible.active > div > article > a')

        if script_tag:
            json_data = script_tag.string.strip()
            car_info = json.loads(json_data)

            engineDetails = {
                'enginePower': extract_numeric_value(engine_power),
                'engineDisplacement': extract_numeric_value(displacement),
                'emissionsCO2': extract_numeric_value(emissions_co2)
            }

            mileage = {
                'value': int(car_info['mileageFromOdometer'].get('value', None)),
                'unitCode': car_info['mileageFromOdometer'].get('unitCode', None)
            }

            # Simplify the car_info object to include selected fields
            simplified_info = {
                'brand': car_info['brand'],
                'name': car_info['name'],
                'price': {
                    'value': int(car_info['offers']['price']),
                    'currency': car_info['offers']['priceCurrency']
                },
                'url': car_info['url'],
                'address': {
                    'streetAddress': address.get_text(strip=True),
                },
                'car_details': {
                    'name': car_info['name'],
                    'manufacturer': car_info['brand'],
                    'model': car_info['model'],
                    'productionDate': car_info['dateVehicleFirstRegistered'],
                    'mileage': mileage,
                    'engineDetails': engineDetails,
                }
            }

            car_details.append(simplified_info)

    # Check if there are more pages
    next_page_button = soup.find('li', {'title': 'Next Page'})

    pagination = next_page_button.get('aria-disabled', 'false')
    if pagination == 'true':
        # If the next page button is disabled, it means we are on the last page
        break

    # Move to the next page
    current_page += 1

# Save car_details to a file named "car_details.json"
with open('car_details_sv.json', 'w') as file:
    json.dump(car_details, file, indent=2)

print("Car details saved to car_details_sv.json")
