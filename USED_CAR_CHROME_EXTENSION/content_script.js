async function extractCarInformation() {
  // Tax rates and discount tables
  const engineTaxRates = {
    normal: [
      { maxDisplacement: 1000, rate: 1.04, parcel: 808.6 },
      { maxDisplacement: 1250, rate: 1.12, parcel: 810.18 },
      { maxDisplacement: Infinity, rate: 5.34, parcel: 5899.89 },
    ],
    cargoRvsOld: [
      { maxDisplacement: 1250, rate: 5.05, parcel: 3173.03 },
      { maxDisplacement: Infinity, rate: 11.98, parcel: 11560.45 },
    ],
  };

  const co2TaxRates = {
    petrol: [
      { maxEmissions: 99, rate: 4.4, parcel: 406.67 },
      { maxEmissions: 115, rate: 7.7, parcel: 715.23 },
      { maxEmissions: 145, rate: 50.06, parcel: 5622.8 },
      { maxEmissions: 175, rate: 58.32, parcel: 6800.16 },
      { maxEmissions: 195, rate: 148.54, parcel: 22502.16 },
      { maxEmissions: Infinity, rate: 195.86, parcel: 31800.11 },
    ],
    diesel: [
      { maxEmissions: 79, rate: 5.5, parcel: 418.13 },
      { maxEmissions: 95, rate: 22.33, parcel: 1760.55 },
      { maxEmissions: 120, rate: 75.45, parcel: 6852.98 },
      { maxEmissions: 140, rate: 167.36, parcel: 18023.73 },
      { maxEmissions: 160, rate: 186.12, parcel: 20686.59 },
      { maxEmissions: Infinity, rate: 255.64, parcel: 31855.14 },
    ],
  };

  const engineDisplacementAgeDiscountTable = [
    { maxAge: 1, discountPercentage: 10 },
    { maxAge: 2, discountPercentage: 20 },
    { maxAge: 3, discountPercentage: 28 },
    { maxAge: 4, discountPercentage: 35 },
    { maxAge: 5, discountPercentage: 43 },
    { maxAge: 6, discountPercentage: 52 },
    { maxAge: 7, discountPercentage: 60 },
    { maxAge: 8, discountPercentage: 65 },
    { maxAge: 9, discountPercentage: 70 },
    { maxAge: 10, discountPercentage: 75 },
    { maxAge: Infinity, discountPercentage: 80 },
  ];

  const co2EmissionsAgeDiscountTable = [
    { maxAge: 2, discountPercentage: 10 },
    { maxAge: 4, discountPercentage: 20 },
    { maxAge: 6, discountPercentage: 28 },
    { maxAge: 7, discountPercentage: 35 },
    { maxAge: 9, discountPercentage: 43 },
    { maxAge: 10, discountPercentage: 52 },
    { maxAge: 12, discountPercentage: 60 },
    { maxAge: 13, discountPercentage: 65 },
    { maxAge: 14, discountPercentage: 70 },
    { maxAge: 15, discountPercentage: 75 },
    { maxAge: Infinity, discountPercentage: 80 },
  ];

  const carTypeDiscountTable = {
    hybrids: { percentageToPay: 60, discountPercentage: 40 },
    plugInHybrids: { percentageToPay: 25, discountPercentage: 75 },
    naturalGas: { percentageToPay: 40, discountPercentage: 60 },
    seats7: { percentageToPay: 40, discountPercentage: 60 },
  };

  // Function to extract data for mobile.de
  function extractMobileDeData() {
    const carPriceElement = document.querySelector(
      '[data-testid="prime-price"]'
    );
    const carYearElement = document.querySelector("#firstRegistration-v");
    const carEngineElement = document.querySelector("#cubicCapacity-v");
    const carEmissionsElement = document.querySelector("#envkv\\.emission-v");
    const carFuelElement = document.querySelector("#fuel-v");
    const carSeatsElement = document.querySelector("#numSeats-v");

    if (
      carPriceElement &&
      carYearElement &&
      carEngineElement &&
      carEmissionsElement &&
      carFuelElement &&
      carSeatsElement
    ) {
      const carPrice = carPriceElement.textContent.trim();
      const carYear = carYearElement.textContent.trim();
      const carEngineDisplacement = carEngineElement.textContent.trim();
      const carEmissions = carEmissionsElement.textContent.trim();
      const carFuel = carFuelElement.textContent.trim();
      const carSeats = parseInt(carSeatsElement.textContent.trim());

      // Additional processing if needed, e.g., converting strings to numbers

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
      let engineDisplacementTax = 0;
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
      let co2EmissionTax = 0;
      if (carType === "diesel") {
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
      // Apply age discount for CO2 emission tax
      co2EmissionTax *=
        1 - getAgeDiscount(carYear, co2EmissionsAgeDiscountTable);

      // Calculate the final ISV
      const isv = engineDisplacementTax + co2EmissionTax;

      // Apply additional discounts based on car type (hybrids, plug-in hybrids, etc.)
      const isvWithDiscount = applyCarTypeDiscount(isv, carType, carSeats);

      console.log("Engine Displacement Tax:", engineDisplacementTax);
      console.log("CO2 Emission Tax:", co2EmissionTax);
      console.log("ISV with Discounts:", isvWithDiscount);
    } else {
      console.log("Failed to extract data from mobile.de");
      // Implement a fallback option or show a message to the user.
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
    const carTypeKey = getCarTypeKey(carFuel, carSeats);

    if (carTypeKey in carTypeDiscountTable) {
      const { percentageToPay, discountPercentage } =
        carTypeDiscountTable[carTypeKey];
      return isv * (1 - discountPercentage / 100);
    }

    return isv;
  }

  function getCarTypeKey(carFuel, carSeats) {
    const carTypeMap = {
      diesel: "diesel",
      benzin: "benzin",
      elektro: "elektro",
      "ethanol (ffv, e85 etc.)": "other",
      hybrids: "hybrids",
      "autogas (lpg)": "other",
      "erdgas (cng)": "naturalGas",
      wasserstoff: "other",
      andere: "other",
    };

    const carTypeKey = carFuel.toLowerCase().includes("plug-in-hybrid")
      ? "plugInHybrids"
      : carFuel.toLowerCase().includes("hybrid")
      ? "hybrids"
      : carFuel.toLowerCase().trim();
    return carTypeMap[carTypeKey] + (carSeats >= 7 ? "-seats7" : "");
  }

  // Function to determine the website and call the appropriate extraction function
  function determineWebsiteAndExtractData() {
    const currentUrl = window.location.href;
    if (currentUrl.includes("mobile.de")) {
      extractMobileDeData();
      // Add more cases for other websites if needed
    } else {
      console.log("Website not supported.");
      // Implement a fallback option or show a message to the user for unsupported websites.
    }
  }

  determineWebsiteAndExtractData();
}

// Call the function to extract car information when the content script is executed.
extractCarInformation();
