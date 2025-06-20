import requests
from bs4 import BeautifulSoup

import time
import random

URL = "https://www.zapimoveis.com.br/aluguel/apartamentos/ce+fortaleza/?onde=%2CCear%C3%A1%2CFortaleza%2C%2C%2C%2C%2Ccity%2CBR%3ECeara%3ENULL%3EFortaleza%2C-3.73272%2C-38.527013%2C&tipos=apartamento_residencial&transacao=aluguel&origem=busca-recente"

def get_house_listings(base_url):
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
    
if __name__ == "__main__":
    listings = get_house_listings(URL)

        