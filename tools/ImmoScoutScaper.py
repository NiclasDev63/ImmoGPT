from bs4 import BeautifulSoup
import utils.get_coordinates as get_coordinates
import utils.get_random_agent as random_agent
import utils.call_AI as call_AI
import json
import requests
from datetime import datetime

class ImmoScoutScraper:
    """
    A class that searches ImmoScout for suitable properties

    Attributes:
        search_data (dict): Dict which contains the important information for the search

    """

    def __init__(self):
        self.data = None

        """
        This cookie needs to be set to scrap ImmoScout24.
        Unfortunately it is only a temporary cookie and must be renewed every few requests
        """
        self.reese84 = {
            "reese84": 
            "3:iMhyIb5H8eSghVfoF2gswA==:tqFamMyfLDPiY7fUOnBp8VOgWhvlPHzBqQ+6ed87/1h8l36eCe5VaV2w+3S5Z/mOvB9LsZssQ/AXS9o/AjJOsfU+FsGNx1BTdHxs/+5s5qe/iTXYvbpIu4/Wsy/x3R6Wc2OWZtQWSQt9b6cyMWzxJ5VYUenGK3xA+lwvCyGvI8G+y+C96eEk82whptlRA0OXnqThw5AkAnd3DKivlrYa8jyqL/IadVrYzJEy3YepXz7cTvjbESFdZeZ+9sq02bHCmKFqkM7dG6PxpPb+aYxbrBlSyvwvPOPZtq2dq23fnoveqG8c8uZoQyQNTv3LbgUq/3cQEz3as3CbsbaVifGaVH8+PV8rDJk/jVipi/0bZISUojB5VvhdBJXvNeV+L6DBhJMFOa6RkppDveOaGsP5sUNByQZn5cc0FDcJ1X3kBEb2/afs8PwTbE6h50t43w8b9+a20ofh0JgLP8OdXj1nlDdW1rS4itEG3QIHUjSDHFi0cWSE9HA4kmIgE99Fu2ulNL7VxCb56UW/O/cnQyz+EA==:Umt6M/OHINPo1lpFulAIv8zeMj35dYJ1DJs9kfqZVoA="
        }

        self.base_url = "https://www.immobilienscout24.de/Suche/radius/"

    
    def _prompt(self, data):
        prompt = f"""
            The user has asked you about the best properties in {self.data["location"]} which you have now selected from ImmoScout24. The following list contains the data of the properties you have picked out in Json format, of which you now pick out 5 (if available) and give the user all the important data.
            It is very Important, that you give the user the matching link and only select properties which are in the LIST WITH THE DATA.

            LIST WITH THE DATA:

            {data}
        
        """

        return prompt


    def scrapImmos(self, search_data):

        """Searches for properties with the desired parameters"""

        self.data = search_data
        url = self._create_url()
        if url != -1:
            resp = requests.get(url, cookies=self.reese84, headers = random_agent.random_agent())
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                data_list_of_dic = self._extract_results(self._html_parser(soup))
                if data_list_of_dic != -1:
                    print(call_AI.make_request(self._prompt(data_list_of_dic)))

            else: 
                print("Can't reach ImmoScout")


    def _create_url(self) -> str:

        """Creates an Immoscout24 link with the desired parameters"""

        price_url = self._extract_price()
        coord_url = self._extract_coords()

        if price_url != -1 and coord_url != -1:
            return self.base_url + price_url + self._extract_squaremeters() + coord_url
        else: 
            print("Can't create URL for request")
            return -1

    def _extract_squaremeters(self) -> str:

        """Converts the wanted squaremeters into url format"""

        url = "livingspace="

        if "minLivingSpace" in self.data and self.data["minLivingSpace"] != None:
            url += str(self.data["minLivingSpace"])
        if "maxLivingSpace" in self.data and self.data["maxLivingSpace"] != None:
            url += "-" + str(self.data["maxLivingSpace"])

        url += "&"

        if url.endswith("livingspace=&"): return ""
        else: return url

    def _extract_price(self) -> str:
        
        """Converts the wanted price into url format"""

        url = ""

        if "type" not in self.data or self.data["type"] == None: 
            print("Can't parse type from json")
            return -1
        
        elif self.data["type"] == "rent": url += "wohnung-mieten?"
        else: url += "wohnung-kaufen?"

        url += "price="

        if "minPrice" in self.data and self.data["minPrice"] != None:
            url += str(self.data["minPrice"])

        if "maxPrice" in self.data and self.data["maxPrice"] != None:
            url += "-" + str(self.data["maxPrice"])
        
        url += "&"

        if url.endswith("price=&"): url = url.replace("price=&", "")
        
        return url

    
    def _extract_coords(self) -> str:
        
        """Converts the desired location into url format"""

        if "location" in self.data and self.data["location"] != None:
            coords = get_coordinates.get_coordinates(self.data["location"])
            if coords != -1:

                radius = 1
                if "radius" in self.data and self.data["radius"] != None \
                and self.data["radius"] != '' and int(self.data["radius"]) > 1:
                    radius = self.data["radius"]

                return "geocoordinates=" + str(coords[0]) + ";" + str(coords[1]) + ";" + str(radius)
            else: return -1
        else:
            print("Can't parse location from json")
            return -1
        
        
    def _html_parser(self, soup: BeautifulSoup) -> dict:
        
        """Parses the html to get the results"""

        scripts = soup.find_all("script")
        for script in scripts:
            try:
                a = script.string.strip()
                if 'IS24.resultList' in a:
                    s = script.string.split('\n')
                    for line in s:
                        if line.strip().startswith('resultListModel'):
                            resultListModel = line.strip('resultListModel: ')
                            immo_json = json.loads(resultListModel[:-1])

                            searchResponseModel = immo_json[u'searchResponseModel']
                            resultlist_json = searchResponseModel[u'resultlist.resultlist']

                            return resultlist_json

            except AttributeError:
                print("Can't parse ImmoScout results")
                return -1
    

    def _extract_results(self, resp: dict) -> list[dict]:
        
        """Parses the resultlist_json and extracts the important information"""

        try:
            if resp == -1:
                return -1
            
            if resp['paging']['numberOfHits'] == 0:
                print("Unfortionatly there were no results, try changing your search parameters")
                return -1
            
            results_json = [{} for _ in resp['resultlistEntries'][0][u'resultlistEntry']]
            for idx, i in enumerate(resp['resultlistEntries'][0][u'resultlistEntry']):
                if isinstance(i, dict):
                    
                    realEstate_json = i[u"resultlist.realEstate"]

                    results_json[idx]["adress"] = realEstate_json["address"]["description"]["text"]

                    results_json[idx]["squaremeter"] = realEstate_json["livingSpace"]

                    results_json[idx]["immo_id"] = i["realEstateId"]

                    results_json[idx]["price"] = realEstate_json["price"]["value"]

                    results_json[idx]["number_of_rooms"] = realEstate_json["numberOfRooms"]

                    results_json[idx]["publish_date"] = datetime.fromisoformat(i["@publishDate"]).strftime("%d. %B %Y, %H:%M Uhr")

                    results_json[idx]["link"] = "https://www.immobilienscout24.de/" + str(results_json[idx]["immo_id"])

        except KeyError as e:
                print("Can't parse ImmoScout results")
                return -1
        
        return results_json
            