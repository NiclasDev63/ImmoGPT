import requests
import os

def get_coordinates(city: str) -> tuple(float, float):
    """
    Converts the desired location into coordinates using the "GeoDB Cities API" from RapidAPI
    https://rapidapi.com/wirefreethought/api/geodb-cities/

    Args:
        city (str): The desired location

    Returns:
        tuple(float, float): The Latitude and Longitude of the location
        
    """

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {"namePrefix": city}

    headers = {
        "X-RapidAPI-Key": os.getenv("X_RapidAPI_Key"),
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        response = response.json()
        return response["data"][0]["latitude"], response["data"][0]["longitude"]
    else: 
        print("Can't get coordinates")
        return -1