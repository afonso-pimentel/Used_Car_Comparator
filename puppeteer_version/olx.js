const fs = require('fs');
const querystring = require('querystring');

// Function to map fuel filter to its corresponding third value
function mapFuelFilterToValue(fuelFilter) {
    // Read and parse the fuel types JSON file
    const fuelTypes = JSON.parse(fs.readFileSync('fuel_types.json', 'utf8'));
    // Get the array corresponding to the provided fuel filter
    const aliasesArray = fuelTypes[fuelFilter];
    
    // If the array exists and has at least three elements, return the third element
    if (aliasesArray && aliasesArray.length >= 3) {
        return aliasesArray[2];
    } else {
        return null; // Return null if the fuel filter is not found or the array is too short
    }
}


function buildOLXSearchURL(filters) {
    const baseUrl = 'https://www.olx.pt/carros-motos-e-barcos/carros/';
    const queryParams = {};

    // Conditionally add filters to queryParams if they are provided
    if (filters.brand) queryParams[''] = filters.brand;
    if (filters.model) queryParams['search[filter_enum_modelo][0]'] = filters.model;
    if (filters.initial_year) queryParams['search[filter_float_year:from]'] = filters.initial_year;
    if (filters.final_year) queryParams['search[filter_float_year:to]'] = filters.final_year;
    if (filters.fuel) queryParams['search[filter_enum_combustivel][0]'] = mapFuelFilterToValue(filters.fuel);
    if (filters.initial_power) queryParams['search[filter_float_engine_power:from]'] = filters.initial_power;
    if (filters.final_power) queryParams['search[filter_float_engine_power:to]'] = filters.final_power;
    if (filters.initial_km) queryParams['search[filter_float_quilometros:from]'] = filters.initial_km;
    if (filters.final_km) queryParams['search[filter_float_quilometros:to]'] = filters.final_km;
    if (filters.price_from) queryParams['search[filter_float_price:from]'] = filters.price_from;
    if (filters.price_to) queryParams['search[filter_float_price:to]'] = filters.price_to;

    const queryString = querystring.stringify(queryParams);

    return `${baseUrl}${filters.brand}/?${queryString}`;
}

function buildSearchURLFromFile(filePath) {
    try {
        const jsonData = fs.readFileSync(filePath, 'utf8');
        const filters = JSON.parse(jsonData);
        const searchURL = buildOLXSearchURL(filters);
        return searchURL;
    } catch (error) {
        console.error('Error reading or parsing JSON file:', error);
        return null;
    }
}

module.exports = {
    buildOLXSearchURL,
    buildSearchURLFromFile
};

// const searchURL = buildSearchURLFromFile('filters.json');
// console.log('OLX Search URL:', searchURL);
