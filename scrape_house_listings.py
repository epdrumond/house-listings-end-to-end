import requests
from bs4 import BeautifulSoup
import time
import random
import itertools 

from utils import *

URL_PARAMS = {
    "transacao": "source_data/house_use.txt",
    "tipos": "source_data/house_type.txt",
    "onde": "source_data/cities.txt"    
}
DESTINATION_FOLDER = "scraped_data/"

def scrape_listings(base_url: str, destination_file: str) -> str:
    page = 1
    while True:

        # Extract data from the URL with the current page number
        url = f"{base_url}&pagina={page}"
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"{DESTINATION_FOLDER}{destination_file}_p{page}.html"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(response.text)
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
    
def get_house_listings() -> None:
    """
    Scrapes house listings from mapped parameters and saves them to HTML files.
    """
    BASE_URL = "https://www.zapimoveis.com.br/"

    # Map parameters to be used in setting up the scraping URLs
    url_params = map_parameters(URL_PARAMS)

    # Loop through all combinations of parameters and scrape listings
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
        scrape_listings(combination_url, combination_name)
        
        if idx > 5:
            break

if __name__ == "__main__":
    get_house_listings()
    

        