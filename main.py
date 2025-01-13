import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

CONFIG = {
    # Zillow
    "zillow_url": "https://appbrewery.github.io/Zillow-Clone/",
    # Google
    "google_forms": "https://forms.gle/C8bBpunhsvXes7zy9",

}
SELECTORS = {
    # Zillow
    "all_listings": "ul.List-c11n-8-84-3-photo-cards li",
    "listing_link": ".StyledPropertyCardDataArea-anchor",
    "listing_price": ".PropertyCardWrapper__StyledPriceLine",
    "listing_address": "address",
    # Google
    "link_input" : "div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input",
    "price_input" : "div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input",
    "address_input" : "div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input",
    "submit_button" : "div.DE3NNc.CekdCb > div.lRwqcd > div"

}


class ZillowScrapingBot:
    def __init__(self):
        self.zillow_response = requests.get(url=CONFIG["zillow_url"])
        self.soup = BeautifulSoup(self.zillow_response.text, "html.parser")
        self.driver = webdriver.Chrome(options=self.get_chrome_options(False))

    def get_listings_info(self) -> dict:
        """
        Returns the link, price, and address for each listing on the page

        Returns:
            Dictionary : Contains the information about each listing indexed from 0
        """
        # Declare the dictionary that will house all the listings
        listings_properties = {}

        # Find all the listings
        listings = self.soup.select(SELECTORS["all_listings"])
        # Get the info from each listing
        for index, listing in enumerate(listings):
            try:
                # Extract link
                link_tag = listing.select_one(SELECTORS["listing_link"])
                if link_tag:
                    link = link_tag['href']
                else:
                    # TODO: Fix some listings not being returned
                    print(f"Failed to get link for:\n{listing.prettify()}")
                    continue
                # Extract price
                price_tag = listing.select_one(SELECTORS["listing_price"])
                price = price_tag.text.split("/")[0].split("+")[0] if price_tag else "No price"

                # Extract address
                address_tag = listing.select_one(SELECTORS["listing_address"])
                address = address_tag.text.strip() if address_tag else "No address"

                # Store in dictionary
                listings_properties[index] = {
                    "link": link,
                    "price": price,
                    "address": address,
                }
            except Exception as e:
                print(f"Error processing listing {index}: {e}")

        print(listings_properties)
        return listings_properties

    def add_listings(self):
        """
        Adds scraped listings to Google Sheets using Google forms
        """
        # Get the listings
        listings_data = self.get_listings_info()

        for listing in listings_data.values():
            print(listing)
            # Visit the Google form
            self.driver.get(url=CONFIG["google_forms"])
            time.sleep(1)

            # Fill in the information
            link_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["link_input"])
            link_input.send_keys(listing["link"])
            price_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["price_input"])
            price_input.send_keys(listing["price"])
            address_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["address_input"])
            address_input.send_keys(listing["address"])

            # Press the submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["submit_button"])
            submit_button.click()
            time.sleep(1)


    def get_chrome_options(self, detach: bool = True) -> Options:
        """
        Creates and configures Chrome options for the selenium webdriver.

        Args:
            detach (bool): Whether to keep the browser window open after execution.

        Returns:
            Options : A configured chrome options object.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", detach)
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        return chrome_options


listings_bot = ZillowScrapingBot()
listings_bot.get_listings_info()
listings_bot.add_listings()
