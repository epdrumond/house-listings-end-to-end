import urllib.parse
import unicodedata
from unidecode import unidecode
import pandas as pd

import os
from dotenv import load_dotenv
import psycopg2

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


def connect_to_db() -> str:
    """
    Connects to the SQLite database.

    Parameters:
        db_path (str): The path to the SQLite database file.

    Returns:
        
    """

    # Load environment variables from .env file
    load_dotenv()

    host = os.getenv("POSTGRES_HOST")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=host,
        user=user,      
        password=password,
        database=database
    )
    cur = conn.cursor()

    return cur, conn


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the raw data into a format suitable for insertion into the database.

    Parameters:
        data (pd.DataFrame): The raw data to be transformed.

    Returns:
        pd.DataFrame: The transformed data ready for insertion.
    """
    transformed_data = data.copy()

    # Field transform: link
    transformed_data["id"] = [
        link.split("-id-")[1].split("/")[0] 
        for link in transformed_data["link"]
    ]

    # Field transform: location
    transformed_data["listing_info"] = [
        loc.split(" em ")[0] 
        for loc in transformed_data["location"]
    ]
    transformed_data["region"] = [
        loc.split(" em ")[1].split(",")[0] 
        for loc in transformed_data["location"]
    ]
    transformed_data.drop(columns=["location"], inplace=True)
    
    # Field transform: size
    transformed_data["size_m2"] = [
        int(size.replace("Tamanho do imóvel ", "").split(" m²")[0])
        for size in transformed_data["size"]
    ]
    transformed_data.drop(columns=["size"], inplace=True)

    #Field transform: bedrooms 
    transformed_data["bedrooms"] = [
        int(bedrooms.replace("Quantidade de quartos ", ""))
        for bedrooms in transformed_data["bedrooms"].fillna("0")
    ]

    #Field transform: bathrooms 
    transformed_data["bathrooms"] = [
        int(bathrooms.replace("Quantidade de banheiros ", ""))
        for bathrooms in transformed_data["bathrooms"].fillna("0")
    ]

    #Field transform: parking_spaces 
    transformed_data["parking_spaces"] = [
        int(parking.replace("Quantidade de vagas de garagem ", ""))
        for parking in transformed_data["parking_spaces"].fillna("0")
    ]

    #Field transform: price 
    transformed_data["iptu"] = [
        price.split("IPTU R$ ")[1] 
        if "IPTU R$ " in price 
        else None
        for price in transformed_data["price"]
    ]
    transformed_data["condominium"] = [
        price.split("Cond. R$ ")[1].split("•")[0]
        if "Cond. R$ " in price 
        else None
        for price in transformed_data["price"]
    ]
    transformed_data["price"] = [
        price.split("/mês")[0].replace("R$ ", "")
        if "R$ " in price 
        else None
        for price in transformed_data["price"]
    ]

    # Additional transformations can be added here as needed
    return transformed_data

def insert_raw_data(cur, conn, schema_name: str, table_name: str, data: list) -> None:
    """
    Inserts raw data into the specified table in the database.

    Parameters:
        cur (cursor): The database cursor.
        conn (connection): The database connection.
        schema_name (str): The name of the schema where the table is located.
        table_name (str): The name of the table to insert data into.
        data (list): A list of dictionaries containing the data to be inserted.
    """
    if not data:
        return
    
    columns = data[0].keys()
    values = [[item[col] for col in columns] for item in data]

    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
    
    psycopg2.extras.execute_values(cur, insert_query, values)
    conn.commit()

if __name__ == "__main__":
    pass
    # cur, conn = connect_to_db()

    # cur.execute("SELECT version();")
    # print(cur.fetchone())




    

