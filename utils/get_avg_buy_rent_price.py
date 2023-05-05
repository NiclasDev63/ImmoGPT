import re
import requests
from bs4 import BeautifulSoup
import utils.get_random_agent as get_random_agent
import utils.call_AI as call_AI

def get_price(data: dict) -> None or int:

    """
    Crawls https://www.homeday.de/de/preisatlas to receive the average buy or rent 
    price in the neighborhood
    """
    address = ""
    acquisition_type = ""
    squaremeter = 0
    user_price = 0

    if "address" in data and data["address"] != None:
        address = data["address"]

    if "acquisition_type" in data and data["acquisition_type"] != None:
        acquisition_type = data["acquisition_type"]

    if "squaremeter" in data and data["squaremeter"] != None:
        squaremeter = float(data["squaremeter"])
    
    if "user_price" in data and data["user_price"] != None:
        user_price = data["user_price"]



    if acquisition_type == "buy": acquisition_type = "sell"
    else: acquisition_type = "rent"

    if address == "":
        print("Can't parse address to calculate average price")
        return -1
    if squaremeter <= 0:
        print("Can't parse squaremeter to calculate average price")
        return -1

    url = f"https://www.homeday.de/de/preisatlas/dreieich/{address}?property_type=apartment&marketing_type={acquisition_type}&map_layer=standard&utm_medium=partner&utm_source=immocation&utm_campaign=rate_of_return_q42018&utm_content=data_table"
    
    resp = requests.get(url, headers=get_random_agent.random_agent())

    if resp.status_code == 200:

        soup_sell = BeautifulSoup(resp.text, 'html.parser')

        price_as_str = soup_sell.find("p", {"class": "price-block__price__average"}).text

        res = re.split("\s", price_as_str)[1]

        if acquisition_type == "sell": res = res.replace(".", "")
        
        else: res = int(res.split(".")[0]) + int(res.split(".")[1]) * 0.1

        res = res * squaremeter

        print(call_AI.make_request(_prompt(res, acquisition_type, squaremeter, user_price)))
    
    else:
        print("Can't reach homeday to get average price")
        return -1
    
def _prompt(avg_price: float, acquisition_type: str, squaremeter: float, user_price: int):
    if acquisition_type == "sell": acquisition_type = "buy"
    prompt = f"""
    Your task is to find out if a property has a reasonable price.
    Below you will find all the information you need to make your decision.
    After you have decided, share your answer with the user.
    Answer short and correct and make sure to mention the average price.

    DATA:
    average price in the Neighborhood for a property of {squaremeter} : {avg_price}
    determines if the user bought or rents the property: {acquisition_type}
    squaremeter: {squaremeter}
    the price the user paid to {acquisition_type} the property: {user_price}
    """

    return prompt
    