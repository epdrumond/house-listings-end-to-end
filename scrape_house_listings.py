import requests
from bs4 import BeautifulSoup
import time
import random
import itertools 

from utils import *

URL = "https://www.zapimoveis.com.br/aluguel/apartamentos/ce+fortaleza/?onde=%2CCear%C3%A1%2CFortaleza%2C%2C%2C%2C%2Ccity%2CBR%3ECeara%3ENULL%3EFortaleza%2C-3.73272%2C-38.527013%2C&tipos=apartamento_residencial&transacao=aluguel&origem=busca-recente"

URL_PARAMS = {
    "transacao": "source_data/house_use.txt",
    "tipos": "source_data/house_type.txt",
    "onde": "source_data/cities.txt",
    
}

def scrape_listings(base_url):
    page = 1
    while True:

        # Extract data from the URL with the current page number
        url = f"{base_url}&pagina={page}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"house_listings_page{page}.html", "w", encoding="utf-8") as file:
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

    # Generate an URL for each parameter combination
    scraping_urls = {}
    
    param_combinations = itertools.product(*url_params.values())
    param_combinations = [dict(zip(url_params.keys(), combination)) for combination in param_combinations]
    for combination in param_combinations:
        transaction_type = combination["transacao"]
        base_location = combination["onde"][0]
        listing_type = combination["tipos"]
        query_location = combination["onde"][1]

        combination_name = f"{transaction_type}_{base_location}_{listing_type}"
        scraping_urls[combination_name] = f"{BASE_URL}{transaction_type}/imoveis/{base_location}/?onde={query_location}?tipos={listing_type}&transacao={transaction_type}"

        print(scraping_urls)
        break

if __name__ == "__main__":
    get_house_listings()
    

        