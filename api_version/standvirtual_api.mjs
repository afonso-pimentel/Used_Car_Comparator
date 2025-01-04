import fetch from "node-fetch";
import fs from "fs";

async function fetchAds(filters, outputFile) {
  const baseUrl = "https://www.standvirtual.com/api/v1/search/?json=1";
  let ads = [];
  let currentPage = 1;

  try {
    while (true) {
      // Construct URL with filters and pagination
      const url = `${baseUrl}&${new URLSearchParams({
        ...filters,
        page: currentPage,
      }).toString()}`;

      console.log(`Fetching page ${currentPage}: ${url}`);
      const response = await fetch(url);
      if (!response.ok)
        throw new Error(
          `Failed to fetch page ${currentPage}: ${response.statusText}`
        );

      const data = await response.json();

      // Check if ads are available
      if (data.search_result.ads.length === 0) break;

      // Extract relevant details from each ad
      const formattedAds = data.search_result.ads.map(ad => ({
        brand: ad.params.find(param => param[0] === "Marca")?.[1] || "N/A",
        name: ad.title || "N/A",
        price: {
          value:
            parseFloat(ad.gross_price?.replace(" EUR", "").replace(",", "")) ||
            "N/A",
          currency: "EUR",
        },
        url: ad.url || "N/A",
        address: ad.dealer_info?.address || "N/A",
        car_details: {
          model: ad.params.find(param => param[0] === "Modelo")?.[1] || "N/A",
          productionDate:
            ad.params.find(param => param[0] === "Ano")?.[1]?.trim() || "N/A",
          mileage:
            ad.params
              .find(param => param[0] === "Quilómetros")?.[1]
              ?.replace(" km", "")
              .replace(",", "") || "N/A",
          engineDetails: {
            enginePower:
              ad.params
                .find(param => param[0] === "Potência")?.[1]
                ?.replace(" cv", "") || "N/A",
            fuelType:
              ad.params.find(param => param[0] === "Combustível")?.[1] || "N/A",
          },
        },
      }));

      // Add formatted ads to the list
      ads = ads.concat(formattedAds);

      // Break if no more pages
      if (currentPage >= data.search_result.total_pages) break;
      currentPage++;
    }

    // Save ads to a JSON file
    fs.writeFileSync(outputFile, JSON.stringify(ads, null, 2));
    console.log(`Saved ${ads.length} ads to ${outputFile}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
}

// Example usage with filters
const filters = {
  "search[filter_enum_make]": "bmw",
  "search[filter_enum_model]": "120",
  "search[filter_enum_engine_code]": "serie-1",
  "search[filter_enum_fuel_type]": "diesel",
  "search[filter_float_engine_power:from]": "100",
  "search[filter_float_engine_power:to]": "200",
  "search[filter_float_first_registration_year:to]": "2024",
  "search[filter_float_mileage:from]": "25000",
  "search[filter_float_mileage:to]": "200000",
  "search[filter_float_price:from]": "10000",
  "search[filter_float_price:to]": "40000",
};

fetchAds(filters, "ads.json");
