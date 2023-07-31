let engineTaxRates = {
  normal: [],
  cargoRvsOld: [],
};

let co2TaxRates = {
  petrol: [],
  diesel: [],
};

let engineDisplacementAgeDiscountTable = [];

let co2EmissionsAgeDiscountTable = [];

let carTypeDiscountTable = [];

let engineDisplacementTax = 0;
let co2EmissionTax = 0;
let isvWithDiscount = 0;
let carTotalPrice = 0;
let carTotalPriceFormatted = "0";

// Function to fetch JSON data from the corresponding files
async function fetchJsonFile(filename) {
  try {
    const response = await fetch(
      chrome.runtime.getURL("isvJsonTables/" + filename)
    );
    const jsonData = await response.json();

    return jsonData;
  } catch (error) {
    console.log(error);
    return null;
  }
}

// Function to fill the variables with JSON data from the corresponding files
async function loadJsonData() {
  try {
    const [
      normal,
      cargoRvsOld,
      petrol,
      diesel,
      displacementDiscount,
      emissionsDiscount,
      carTypeDiscount,
    ] = await Promise.all([
      fetchJsonFile("Engine_displacement_normal.json"),
      fetchJsonFile("Engine_displacement_carg_RV_Old.json"),
      fetchJsonFile("Emissions_Petrol.json"),
      fetchJsonFile("Emissions_Diesel.json"),
      fetchJsonFile("Engine_displacement_discount.json"),
      fetchJsonFile("Emissions_discount.json"),
      fetchJsonFile("ISV_discount.json"),
    ]);

    engineTaxRates.normal = normal;
    engineTaxRates.cargoRvsOld = cargoRvsOld;
    co2TaxRates.petrol = petrol;
    co2TaxRates.diesel = diesel;
    engineDisplacementAgeDiscountTable = displacementDiscount;
    co2EmissionsAgeDiscountTable = emissionsDiscount;
    carTypeDiscountTable = carTypeDiscount;

    console.log("JSON data loaded successfully!");
  } catch (error) {
    console.error("Error loading JSON data:", error);
  }
}

// Function to extract car information from the website
async function extractCarInformation() {
  // Function to extract data for mobile.de
  async function extractMobileDeData() {
    const carPriceElement = document.querySelector(
      '[data-testid="prime-price"]'
    );
    const carYearElement = document.querySelector("#firstRegistration-v");
    const carEngineElement = document.querySelector("#cubicCapacity-v");
    const carEmissionsElement = document.querySelector("#envkv\\.emission-v");
    const carFuelElement = document.querySelector("#fuel-v");
    const carSeatsElement = document.querySelector("#numSeats-v");
    const missingElements = [];
    let errorMessage = "";

    if (!carPriceElement) missingElements.push("Car price");
    if (!carYearElement) missingElements.push("Car year");
    if (!carEngineElement) missingElements.push("Car engine displacement");
    if (!carEmissionsElement) missingElements.push("Car emissions");
    if (!carFuelElement) missingElements.push("Car fuel type");
    if (!carSeatsElement) missingElements.push("Car seats");

    if (missingElements.length != 0) {
      const missingElementsString = missingElements.join(", ");
      errorMessage = `Missing elements: ${missingElementsString}`;
      return errorMessage;
    } else {
      const carPrice = carPriceElement.textContent.trim();
      const carYear = carYearElement.textContent.trim();
      const carEngineDisplacement = carEngineElement.textContent.trim();
      const carEmissions = carEmissionsElement.textContent.trim();
      const carFuel = carFuelElement.textContent.trim();
      const carSeats = parseInt(carSeatsElement.textContent.trim());

      console.log("Car Price:", carPrice);
      console.log("Car Year:", carYear);
      console.log("Car Engine Displacement:", carEngineDisplacement);
      console.log("Car Emissions:", carEmissions);
      console.log("Car Fuel:", carFuel);
      console.log("Car Seats:", carSeats);

      // Convert engine displacement from string to number (remove 'cm³' and extract the numeric value)
      const engineDisplacementMatch =
        carEngineDisplacement.match(/\d+(\.\d+)?/);
      const engineDisplacement = engineDisplacementMatch
        ? parseFloat(engineDisplacementMatch[0].replace(".", ""))
        : 0;

      // Calculate Engine Displacement Tax based on the tables provided
      let taxRates = engineTaxRates.normal;

      // if (carFuelElement.textContent.trim().toLowerCase() === "diesel") {
      //   taxRates = engineTaxRates.cargoRvsOld;
      // }
      for (const rate of taxRates) {
        if (engineDisplacement <= rate.maxDisplacement) {
          engineDisplacementTax = engineDisplacement * rate.rate - rate.parcel;
          break;
        }
      }

      console.log(
        "Engine Displacement Tax before Discount:",
        engineDisplacementTax
      );
      // Apply age discount for engine displacement tax
      engineDisplacementTax *=
        1 - getAgeDiscount(carYear, engineDisplacementAgeDiscountTable);

      // Extract only the numeric value of CO2 emissions from the string
      const co2EmissionsMatch = carEmissions.match(/\d+/);
      const co2Emissions = co2EmissionsMatch
        ? parseInt(co2EmissionsMatch[0])
        : 0;

      const carType = carFuelElement.textContent.trim().toLowerCase();

      // Calculate CO2 Emission Tax based on the tables provided
      if (carType.includes("diesel")) {
        taxRates = co2TaxRates.diesel;
      } else {
        taxRates = co2TaxRates.petrol;
      }
      for (const rate of taxRates) {
        if (co2Emissions <= rate.maxEmissions) {
          co2EmissionTax = co2Emissions * rate.rate - rate.parcel;
          break;
        }
      }

      console.log("CO2 Emission Tax before Discount:", co2EmissionTax);
      // Apply age discount for CO2 emission tax
      co2EmissionTax *=
        1 - getAgeDiscount(carYear, co2EmissionsAgeDiscountTable);

      // Calculate the final ISV
      const isv = engineDisplacementTax + co2EmissionTax;

      // Apply additional discounts based on car type (hybrids, plug-in hybrids, etc.)
      isvWithDiscount = applyCarTypeDiscount(isv, carType, carSeats);

      carTotalPrice = parseFloat(carPrice.replace(".", "")) + isvWithDiscount;

      carTotalPriceFormatted = (carTotalPrice / 1000).toLocaleString("de-DE", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: 3,
        maximumFractionDigits: 3,
      });

      console.log("Engine Displacement Tax:", engineDisplacementTax);
      console.log("CO2 Emission Tax:", co2EmissionTax);
      console.log("ISV with Discounts:", isvWithDiscount);
      console.log("Car Total Price:", carTotalPriceFormatted);
      return carTotalPriceFormatted;
    }
  }

  // Function to get the age discount based on the registration year
  function getAgeDiscount(registrationYear, discountTable) {
    // Parse the registration year string to extract the month and year components
    const [registrationMonth, registrationYearNum] = registrationYear
      .split("/")
      .map(Number);

    // Calculate the current date
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1; // JavaScript months are zero-based

    // Calculate the age of the car in years
    let carAge = currentYear - registrationYearNum;
    if (currentMonth < registrationMonth) {
      carAge--; // Adjust for months (if the current month is earlier than the registration month)
    } else {
      carAge++; // Adjust for months (if the current month is later than the registration month)
    }

    console.log("Car Age:", carAge);

    // Find the corresponding discount percentage from the discountTable
    let discountPercentage = 0;
    for (const entry of discountTable) {
      if (carAge <= entry.maxAge) {
        discountPercentage = entry.discountPercentage;
        break;
      }
    }

    return discountPercentage / 100;
  }

  // Function to apply additional discounts based on car type (hybrids, plug-in hybrids, etc.)
  function applyCarTypeDiscount(isv, carFuel, carSeats) {
    const carType = carTypeDiscountTable.find(item => {
      return item.type === getCarTypeKey(carFuel, carSeats);
    });

    if (carType) {
      const { percentageToPay, discountPercentage } = carType;
      return isv * (1 - discountPercentage / 100);
    }

    return isv;
  }

  // Function to get the car type key from the car fuel and number of seats
  function getCarTypeKey(carFuel, carSeats) {
    const carTypeMap = {
      diesel: "diesel",
      benzin: "benzin",
      elektro: "elektro",
      "ethanol (ffv, e85 etc.)": "other",
      hybrids: "hybrids",
      plugInHybrids: "plugInHybrids",
      naturalGas: "naturalGas",
      seats7: "seats7",
      wasserstoff: "other",
      andere: "other",
    };

    const carTypeKey = carFuel.toLowerCase().includes("plug-in-hybrid")
      ? "plugInHybrids"
      : carSeats >= 7
      ? "seats7"
      : carFuel.toLowerCase().includes("Autogas")
      ? "naturalGas"
      : carFuel.toLowerCase().includes("hybrid")
      ? "hybrids"
      : carFuel.toLowerCase().trim();
    return carTypeMap[carTypeKey];
  }

  // Function to determine the website and call the appropriate extraction function
  function determineWebsiteAndExtractData() {
    const currentUrl = window.location.href;
    if (currentUrl.includes("mobile.de")) {
      return extractMobileDeData();
      // Add more cases for other websites if needed
    } else {
      console.log("Website not supported.");
      // Implement a fallback option or show a message to the user for unsupported websites.
    }
  }

  return determineWebsiteAndExtractData();
}

// Function to convert the string "infinity" to Infinity
function convertInfinity(data) {
  for (const item of data) {
    for (const key in item) {
      if (item[key] === "infinity") {
        item[key] = Infinity;
      }
    }
  }
}

// Function to display the total price on the website
function displayTotalPrice(totalPrice) {
  // Identify the element where you want to display the total price
  const carPriceElement = document.querySelector(
    "#main-cta-box-price-row > div.main-price-and-rating-row"
  );
  if (carPriceElement) {
    // Create a new element to display the total price
    const totalPriceElement = document.createElement("span");

    // Create a new element for the "c/ISV: " part with a smaller font size
    const prefixElement = document.createElement("span");
    prefixElement.style.fontSize = "1rem"; // Adjust the font size as needed
    prefixElement.textContent = "c/ISV: ";

    // Create a new element for the total price value
    const valueElement = document.createElement("span");
    valueElement.style.fontSize = "1.5rem";
    valueElement.style.fontWeight = "bold";
    valueElement.style.color = "#008000";
    valueElement.textContent = totalPrice; // Format the total price as a currency string

    // Append the prefix and value elements to the total price element
    totalPriceElement.appendChild(prefixElement);
    totalPriceElement.appendChild(valueElement);

    // Insert the total price element in front or below the car price element
    // You can choose either "beforebegin" or "afterend" depending on the desired location
    carPriceElement.insertAdjacentElement("afterend", totalPriceElement);

    // Create a blank div for spacing
    const blankDivElement = document.createElement("div");
    blankDivElement.style.height = "20px"; // Adjust the height as needed

    // Insert the blank div after the total price element
    totalPriceElement.insertAdjacentElement("afterend", blankDivElement);
  }
}

// Function to execute the code
async function main() {
  await loadJsonData(); // Ensure loadJsonData is called before any code that uses the variables

  convertInfinity(engineTaxRates.normal);
  convertInfinity(engineTaxRates.cargoRvsOld);
  convertInfinity(co2TaxRates.petrol);
  convertInfinity(co2TaxRates.diesel);
  convertInfinity(engineDisplacementAgeDiscountTable);
  convertInfinity(co2EmissionsAgeDiscountTable);
  // Now the variables should have Infinity instead of the string "infinity"

  // Call the function to extract car information when the content script is executed.
  carTotalPriceFormatted = await extractCarInformation();
  if (
    carTotalPriceFormatted &&
    carTotalPriceFormatted.includes("Missing elements")
  ) {
    console.error("Error extracting car information:", carTotalPriceFormatted);
  }

  displayTotalPrice(carTotalPriceFormatted);
}

main();
