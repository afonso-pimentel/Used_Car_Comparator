import json
import best_deals as bdeals

class Filters:
    def __init__(self, brand='', model='', initial_year='', final_year='', initial_km='', final_km='',
                 initial_power='', final_power='', power_type='', price_from='', price_to_autoscout='',
                 price_to_standvirtual=''):
        self.brand = brand
        self.model = model
        self.initial_year = initial_year
        self.final_year = final_year
        self.initial_km = initial_km
        self.final_km = final_km
        self.initial_power = initial_power
        self.final_power = final_power
        self.power_type = power_type
        self.price_from = price_from
        self.price_to_autoscout = price_to_autoscout
        self.price_to_standvirtual = price_to_standvirtual


def add_search_criteria():
    print("Add search criteria:")
    filters = {
        "brand": input("Brand (press enter for empty): ").strip(),
        "model": input("Model (press enter for empty): ").strip(),
        "initial_year": input("Initial year (press enter for empty): ").strip(),
        "final_year": input("Final year (press enter for empty): ").strip(),
        "initial_km": input("Initial km (press enter for empty): ").strip(),
        "final_km": input("Final km (press enter for empty): ").strip(),
        "initial_power": input("Initial power (press enter for empty): ").strip(),
        "final_power": input("Final power (press enter for empty): ").strip(),
        "power_type": input("Power type (press enter for empty): ").strip(),
        "price_from": input("Price from (press enter for empty): ").strip(),
        "price_to_autoscout": input("Price to (AutoScout24) (press enter for empty): ").strip(),
        "price_to_standvirtual": input("Price to (StandVirtual) (press enter for empty): ").strip()
    }

    # Save filters to a file named "filters.json"
    with open('filters.json', 'w') as file:
        json.dump(filters, file, indent=2)

    return filters


def scrape_car_info(filters):
    print("Scraping car info...")
    bdeals.scrape_used_cars(filters)


def get_best_deals():
    print("Getting best deals...")  # Placeholder for actual implementation
    bdeals.get_best_deals()

def main():
    while True:
        print("\nMenu:")
        print("1. Add search criteria")
        print("2. Scrape car info")
        print("3. Get best deals")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            filters = add_search_criteria()
            print("Search criteria added:", filters)
        elif choice == '2':
            # Read the content of the JSON file
            with open('filters.json', 'r') as file:
                filters = json.load(file)
            print(filters)
            scrape_car_info(filters)
        elif choice == '3':
            get_best_deals()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
