import urllib.parse
import unicodedata

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
    state_noaccents = unicodedata.normalize('NFKD', state).encode('ASCII', 'ignore').decode('ASCII')
    city_noaccents = unicodedata.normalize('NFKD', city).encode('ASCII', 'ignore').decode('ASCII')

    # Build the string
    query = (
        f"%2C{state_enc}%2C{city_enc}%2C%2C%2C%2C%2Ccity%2CBR%3E"
        f"{state_noaccents}%3ENULL%3E{city_noaccents}%2C"
        f"{latitude}%2C{longitude}%2C"
    )

    print(state_enc, state_noaccents)
    print(city_enc, city_noaccents)

    return query

def build_url(base_url: str, params: dict) -> str:
    

