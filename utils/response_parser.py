import json
import re
import utils.call_AI as call_AI
import tools.ImmoScoutScaper as ImmoScoutScaper
import utils.get_avg_buy_rent_price as get_avg_buy_rent_price


def response_parser(response: str) -> dict:
    """
    Parses the response to get the answer and commands

    Args:
        response (str): The raw reponse from the API call

    Returns:
        dict: Valid json which includes the command and answer

    Raises:
        json.decoder.JSONDecodeError: If json can't get extracted from the response
    """

    response_json = ""

    try:
        response_json = json.loads(response)
    except json.decoder.JSONDecodeError:
        try:
            response_json = re.search(r'{.*}', response, re.DOTALL).group(0)
            response_json = re.sub("\s", " ", response_json)
            response_json = json.loads(response_json)
        except (json.decoder.JSONDecodeError, AttributeError) as e:
            # If nothing works, trying to get ChatGPT to parse the reponse
            prompt = f"Search for the two outer brackets in the following text \
            and only return the JSON within it including, the brackets: {response_json}"

            try:
                response_json = json.loads(call_AI.make_request(prompt))
            except json.decoder.JSONDecodeError:
                print("Cant extract json from response")

    print(response)           
    if isinstance(response_json, dict) and "command" in response_json:
        print(response_json)
        command = response_json["command"]
        if command != None and "name" in command:
            
            if command["name"] == None or command["name"] == "": 
                print(response_json["answer"])

            if command["name"] == "ImmoScout":
                print("Using ImmouScout command")
                immoscraper = ImmoScoutScaper.ImmoScoutScraper()
                immoscraper.scrapImmos(command["args"])

            if command["name"] == "averagePrice":
                print("Using averagePrice command")
                get_avg_buy_rent_price.get_price(command["args"])