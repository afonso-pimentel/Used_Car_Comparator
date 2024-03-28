// index.js

const olxFunctions = require('./olx.js');
const puppeteer = require('puppeteer');

let carItems = [];


(async () => {

    // Usage example
    const searchURL = olxFunctions.buildSearchURLFromFile('filters.json');
    console.log('OLX Search URL:', searchURL);

    // Launch the browser and open a new blank page
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: false,
        userDataDir: "./tmp"
    });
    const page = await browser.newPage();

    // Navigate the page to a URL
    await page.goto(searchURL);

    let hasNextPage = true;
    while (hasNextPage) {
        await page.waitForSelector('[data-testid="l-card"]');
        const carHandles = await page.$$('[data-testid="listing-grid"] > [data-testid="l-card"]');
        for (const carHandle of carHandles) {
            let carLink = "Null";
            let carPrice = "0€";
            try {
                carLink = await page.evaluate(el => el.querySelector("a").getAttribute("href"), carHandle);
            } catch (error) {
            }
            try {
                carPrice = await page.evaluate(el => el.querySelector('[data-testid="ad-price"]').textContent, carHandle);
            } catch (error) {
            }
            if (carLink !== "Null" && carPrice !== "0€") {
                carItems.push({ carLink, carPrice });
            }
        }
        await page.waitForSelector('[data-testid="pagination-list-item"]');
        hasNextPage = await page.$('[data-testid="pagination-forward"]') !== null;
        if (hasNextPage) {
            await Promise.all([
                page.click('[data-testid="pagination-forward"]'),
                page.waitForNavigation({ waitUntil: "networkidle2" }),
            ]);
        }
    }

    console.log(carItems.length);
    await browser.close();
})();