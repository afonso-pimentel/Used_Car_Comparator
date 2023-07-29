function extractCarInformation() {
  // Function to extract data for mobile.de
  function extractMobileDeData() {
    const carPriceElement = document.querySelector(
      '[data-testid="prime-price"]'
    );
    const carYearElement = document.querySelector("#firstRegistration-v");
    const carEngineElement = document.querySelector("#cubicCapacity-v");
    const carEmissionsElement = document.querySelector("#envkv\\.emission-v");

    if (
      carPriceElement &&
      carYearElement &&
      carEngineElement &&
      carEmissionsElement
    ) {
      const carPrice = carPriceElement.textContent.trim();
      const carYear = carYearElement.textContent.trim();
      const carEngineDisplacement = carEngineElement.textContent.trim();
      const carEmissions = carEmissionsElement.textContent.trim();

      // Additional processing if needed, e.g., converting strings to numbers

      console.log("Car Price:", carPrice);
      console.log("Car Year:", carYear);
      console.log("Car Engine Displacement:", carEngineDisplacement);
      console.log("Car Emissions:", carEmissions);
    } else {
      console.log("Failed to extract data from mobile.de");
      // Implement a fallback option or show a message to the user.
    }
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
