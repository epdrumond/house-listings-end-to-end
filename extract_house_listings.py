from bs4 import BeautifulSoup

def extract_house_listings(file_path):
    """"
    Extracts house listings from a local HTML file and returns a list of dictionaries with relevant details.

    Parameters:
    file_path (str): The path to the HTML file containing the house listings.
    Returns:
    list: A list of dictionaries, each containing details of a house listing.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    
    fields_mapping = {
        "listings": ("li", {"data-cy": "rp-property-cd"}),
        "location": ("h2", {"data-cy": "rp-cardProperty-location-txt"}),
        "location_detail": ("p", {"data-cy": "rp-cardProperty-street-txt"}),
        "size": ("li", {"data-cy": "rp-cardProperty-propertyArea-txt"}),
        "bedrooms": ("li", {"data-cy": "rp-cardProperty-bedroomQuantity-txt"}),
        "bathrooms": ("li", {"data-cy": "rp-cardProperty-bathroomQuantity-txt"}),
        "parking_spaces": ("li", {"data-cy": "rp-cardProperty-parkingSpacesQuantity-txt"}),
        "price": ("div", {"data-cy": "rp-cardProperty-price-txt"})
    }

    listings = []
    for idx, listing in enumerate(soup.find_all(fields_mapping["listings"][0], attrs=fields_mapping["listings"][1])):
        
        listing_dict = {}

        # Extract listing link for later ID retrieval
        try:
            listing_dict["link"] = listing.find("a", attrs={"href": True})["href"]
        # Some items in the list are not really listings, so we skip them
        except TypeError:
            continue
        

        for field, (tag, attrs) in fields_mapping.items():
            if field == "listings":
                continue

            element = listing.find(tag, attrs=attrs)
            if element:
                listing_dict[field] = element.get_text()
            else:
                listing_dict[field] = None

        listings.append(listing_dict)
    
    return listings

if __name__ == "__main__":
    file_path = "house_listings.html"
    listings = extract_house_listings(file_path)
    print(listings)
    