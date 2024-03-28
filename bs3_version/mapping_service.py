fuelType = {
    "petrol hybrid": ["électrique/essence", "híbrido (gasolina)"],
    "diesel hybrid": ["électrique/diesel", "híbrido (diesel)"],
    "electric": ["electrique", "eléctrico"],
    "diesel": ["diesel"],
    "petrol": ["essence","gasolina"],
    "naturalGas": ["gnl","gnc"],
    "GPL": ["gpl"],
    "hydrogen": ["hydrogène", "hidrógenio"],
}

def get_fuel_type(fuel):
    fuel = fuel.lower()
    for k, v in fuelType.items():
        if fuel in v:
            return k
    return None