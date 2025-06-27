import requests
from bs4 import BeautifulSoup
import time
import random
import itertools 
from datetime import datetime
import pandas as pd

from utils import *
from extract_house_listings import extract_house_listings

URL_PARAMS = {
    "transacao": "source_data/house_use.txt",
    "tipos": "source_data/house_type.txt",
    "onde": "source_data/cities.txt"    
}

def scrape_listings(base_url: str) -> list:
    """    
    Scrapes house listings from a given URL and returns a list of listings.  
    Parameters:
        base_url (str): The base URL to scrape listings from.
    Returns:
        list: A list of dictionaries, each containing details of a house listing.
    Raises:
        ValueError: If the URL is invalid or if the page content cannot be fetched.
    """
    
    listings_data = []
    page = 1

    while True:

        # Extract data from the URL with the current page number    
        url = f"{base_url}&pagina={page}"
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            listings_data.extend(extract_house_listings(page_content))
        else:
            return "Error: Unable to fetch data from the URL."

        # Check for a next page
        soup = BeautifulSoup(response.text, "html.parser")
        next_page = soup.find("button", {"data-testid": "next-page"})
        if next_page.has_attr("disabled"):
            break
        page += 1

        # Sleep to avoid overwhelming the server
        time.sleep(random.uniform(1, 5))

    # Validate the amount of listings found matches the page header 
    total_listings = int(soup.find("h1", {"data-cy": "rp-searchTitle-txt"}).get_text().split()[0])
    if total_listings != len(listings_data):
        print(total_listings, len(listings_data))
        raise ValueError(f"Expected {total_listings} listings, but found {len(listings_data)}.")    

    return listings_data
    
def get_house_listings() -> None:
    """
    Scrapes house listings from mapped parameters and saves them to HTML files.
    """
    BASE_URL = "https://www.zapimoveis.com.br/"

    # Map parameters to be used in setting up the scraping URLs
    url_params = map_parameters(URL_PARAMS)

    # Loop through all combinations of parameters and scrape listings
    scraping_date = datetime.now().strftime("%Y-%m-%d")

    param_combinations = itertools.product(*url_params.values())
    param_combinations = [dict(zip(url_params.keys(), combination)) for combination in param_combinations]
    for idx, combination in enumerate(param_combinations):
        # Generate an URL for each parameter combination
        transaction_type = combination["transacao"]
        base_location = combination["onde"][0]
        listing_type = combination["tipos"]
        query_location = combination["onde"][1]

        combination_name = f"{transaction_type}_{base_location}_{listing_type}"
        combination_url = f"{BASE_URL}{transaction_type}/imoveis/{base_location}/?onde={query_location}?tipos={listing_type}&transacao={transaction_type}"

        # Scrape the listings for the current combination
        combination_data = scrape_listings(combination_url)

        if len(combination_data) == 0:
            print(f"No listings found for combination: {combination_name}")
            continue

        # Extract relevant data from the listings
        break

if __name__ == "__main__":
    get_house_listings()
    
    

        