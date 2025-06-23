import urllib.parse
import unicodedata
from unidecode import unidecode
import pandas as pd

def build_location_query(state, city, latitude, longitude):
    ''''
    Builds a query string for a location based on state, city, latitude, and longitude.
    
    Parameters:
        state (str): The state name.
        city (str): The city name.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    
    Returns:
        str: A formatted query string.
    '''
    # URL-encode state and city for the first URL reference
    state_enc = urllib.parse.quote(state)
    city_enc = urllib.parse.quote(city)
    
    # Remove accents for second URL reference
    state_noaccents = "+".join(unicodedata.normalize('NFKD', state).encode('ASCII', 'ignore').decode('ASCII').split())
    city_noaccents = "+".join(unicodedata.normalize('NFKD', city).encode('ASCII', 'ignore').decode('ASCII').split())

    # Build the string
    query = (
        f"%2C{state_enc}%2C{city_enc}%2C%2C%2C%2C%2Ccity%2CBR%3E"
        f"{state_noaccents}%3ENULL%3E{city_noaccents}%2C"
        f"{latitude}%2C{longitude}%2C"
    )

    return query


def map_parameters(params: dict) -> dict:
    """
    Maps the parameters to their respective values for the URL.

    Parameters:
        params (dict): A dictionary of the parameters to be mapped and the files with all possible values. 
            Parameter keys are displayed in portuguese, as they are going to be used in a URL.

    Returns:
        dict: A dictionary with the mapped parameters.
    """
    url_params = {}

    # Transaction type (sell or rent)
    if params["transacao"]:
        url_params["transacao"] = pd.read_csv(params["transacao"])["house_use_url_string"].values.tolist()
    else:
        url_params["transacao"] = ["venda"]

    # There are two location parameters in the URL. Since they are not independet from each other, 
    # we are going to map them together.

    # Location 
    locations_df = pd.read_csv(params["onde"]) 
    locations_df["base_url_location"] = locations_df.apply(
        lambda row: f"""{row['state_code'].lower()}+{'-'.join(unidecode(row['capital']).split()).lower()}""", axis=1
    )
    locations_df["url_location_query"] = locations_df.apply(
        lambda row: build_location_query(
            row["state"], 
            row["capital"], 
            row["latitude"], 
            row["longitude"]
            ), axis=1
    )
    url_params["onde"] = locations_df[["base_url_location", "url_location_query"]].values.tolist()

    # Listings type 
    url_params["tipos"] = pd.read_csv(params["tipos"])["house_type_url_string"].values.tolist()

    return url_params




# https://www.zapimoveis.com.br/
#     venda/
#     apartamentos/
#     ce+fortaleza/
#     ?onde=%2CCear%C3%A1%2CFortaleza%2C%2C%2C%2C%2Ccity%2CBR%3ECeara%3ENULL%3EFortaleza%2C-3.73272%2C-38.527013%2C
#     &tipos=apartamento_residencial
#     &transacao=venda

    

