import re
import requests
from bs4 import BeautifulSoup
import utils.get_random_agent as get_random_agent

def get_price(data: dict) -> dict:

    """
    Crawls https://www.homeday.de/de/preisatlas to receive the average buy or rent 
    price in the neighborhood
    """
    address = ""
    acquisition_type = ""
    squaremeter = 0

    if "location" in data and data["location"] != None:
        address = data["location"]

    if "acquisition_type" in data and data["acquisition_type"] != None:
        acquisition_type = data["acquisition_type"]

    if "squaremeter" in data and data["squaremeter"] != None:
        squaremeter = float(data["squaremeter"])



    if acquisition_type == "buy": acquisition_type = "sell"
    else: acquisition_type = "rent"

    if address == "":
        print("Can't parse address to calculate average price")
        return -1
    if squaremeter <= 0:
        print("Can't parse squaremeter to calculate average price")
        return -1
    
    #TODO Fix URL
    url = f"https://www.homeday.de/de/preisatlas/dreieich/{address}?property_type=apartment&marketing_type={acquisition_type}&map_layer=standard&utm_medium=partner&utm_source=immocation&utm_campaign=rate_of_return_q42018&utm_content=data_table"
    
    resp = requests.get(url, headers=get_random_agent.random_agent())

    if resp.status_code == 200:

        soup_sell = BeautifulSoup(resp.text, 'html.parser')

        price_as_str = soup_sell.find("p", {"class": "price-block__price__average"}).text

        res = re.split("\s", price_as_str)[1]

        if acquisition_type == "sell": res = int(res.replace(".", ""))
        
        else: res = int(res.split(".")[0]) + int(res.split(".")[1]) * 0.1

        avg_price = res * squaremeter

        resp_json = {"avg_price": avg_price, "acquisition_type": acquisition_type, "address": address, "squaremeter": squaremeter}

        return resp_json
    
    else:
        print("Can't reach homeday to get average price")
        return -1