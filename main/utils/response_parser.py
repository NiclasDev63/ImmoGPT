import json
import re
import utils.call_AI as call_AI
import tools.ImmoScoutScaper as ImmoScoutScaper
import utils.get_avg_buy_rent_price as get_avg_buy_rent_price
from typing import Tuple
import utils.memory as memory

def response_parser(response: str) -> str or int:
    #TODO make this Class the return result of command
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

    print("DATA", response)

    try:
        response_json = json.loads(response)
    except json.decoder.JSONDecodeError:
        response_json, e = _get_json_from_response(response)
        if e == '0': response_json = json.loads(response_json)
        else:
            if e.startswith("Expecting property name enclosed in double quotes") or \
                    e.startswith("Expecting value"):
                response_json = _add_quotes_to_property_and_value(response_json, e)
                if _is_valid_json(response_json):
                    response_json = json.loads(response_json)
                else:
                    response_json = _get_json_from_ai(response_json)


    if isinstance(response_json, dict) and "command" in response_json:
        #print(response_json)
        command = response_json["command"]
        if command != None and "name" in command:
            
            if command["name"] == None or command["name"] == "": 
                print(response_json["answer"])
                memory.Memory.add({"role":"assistant", "content": response_json["answer"]})

            elif command["name"] == "ImmoScout":
                print("Using ImmouScout command")
                immoscraper = ImmoScoutScaper.ImmoScoutScraper()
                immoscraper.scrapImmos(command["args"])

            elif command["name"] == "averagePrice":
                print("Using averagePrice command")
                get_avg_buy_rent_price.get_price(command["args"])

            elif command["name"] == "task_complete":
                print("Using task_complete command")
                return 0


def _get_json_from_ai(bad_json: str) -> str or int:
    # If nothing works, trying to get ChatGPT to parse the reponse
    prompt = f"Fix the following invalid JSON and only return the correct JSON without any other information: {bad_json}"
    try:
        response_json = call_AI.make_request(prompt)
        return json.loads(_get_json_from_response(response_json))
    except json.decoder.JSONDecodeError:
        print("Cant extract json from response")
        return -1

def _get_json_from_response(response: str) -> Tuple[str, str]:
    response_json = response
    try:
        response_json = re.search(r'{.*}', response, re.DOTALL).group(0)
        response_json = re.sub("\s", " ", response_json)
        json.loads(response_json)
        return response_json, '0'
    except (json.decoder.JSONDecodeError, AttributeError) as e:
        return response_json, str(e)


def _add_quotes_to_property_and_value(bad_json: str, error_msg: str) -> str:
    while error_msg.startswith("Expecting property name enclosed in double quotes") or \
        error_msg.startswith("Expecting value"):
        char_pos = _extract_char_pos(error_msg)
        bad_json = bad_json[:char_pos] + "\"" + bad_json[char_pos:]
        try:
            json.loads(bad_json)
            break
        except json.decoder.JSONDecodeError as e:
            error_msg = str(e)
    return bad_json

def _is_valid_json(json_str: str) -> bool:
    try:
        json.loads(json_str)
        return True
    except json.decoder.JSONDecodeError:
        return False


def _extract_char_pos(error_msg: str) -> int:
    return int(re.compile(r"\(char (\d+)\)").search(error_msg)[1])
