import json
import re
import utils.call_AI as call_AI
from tools import ImmoCalculator, ImmoScoutScaper, get_avg_buy_rent_price
from typing import Tuple
from commands.commands import Commands
from agents.main_agent.MainAgentReponseTypes import MainAgentReponseTypes
from agents.sub_agent.SubAgentResponseTypes import SubAgentReponseTypes

def response_parser(response: str, agent_type: str) -> Tuple[Commands, str]:
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
    #TODO Delete
    # response = r"""{
    #         "thought": "The user wants to buy an apartment in Frankfurt am Main.",
    #         "reasoning": "To assist the user in finding a suitable apartment in Frankfurt am Main, I can use the 'search_immo' command with the 'acquisition_type' set to 'kaufen' (buy) and the 'location' set to 'Frankfurt am Main'.",
    #         "plan": [
    #         "- Use 'search_immo' command",
    #         "- Set 'acquisition_type' to 'kaufen' (buy)",
    #         "- Set 'location' to 'Frankfurt am Main'"
    #         ],
    #         "speak": ""
    #         }"""

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

    print("REPONSE JSON: ", response_json, "\n")

    if isinstance(response_json, dict):
        return _extract_result_from_subAgent(response_json) if agent_type == "sub" else _extract_result_from_mainAgent(response_json)

#TODO Maybe always return what the main agent hast to say ?
def _extract_result_from_mainAgent(response_json: dict):
    plan = response_json["plan"] if "plan" in response_json else None
    if isinstance(plan, list) and len(plan) > 0:
        final_plan = []
        count = -1
        for p in plan:
            if p[0] == "-":
                final_plan[count] += p
            else:
                final_plan.append(p)
                count += 1
        print("Returning Plan")
        return MainAgentReponseTypes.PLAN, final_plan
    
    speak = response_json["speak"] if "speak" in response_json else None
    if speak and speak != "":
        print("Answering the user")
        return MainAgentReponseTypes.SPEAK, speak



def _extract_result_from_subAgent(response_json: dict):
        
        if "conversation" in response_json:
            conversation_json = response_json["conversation"]
            missing_info = conversation_json["mssing_info"] if "mssing_info" in conversation_json else None
            if missing_info and missing_info != "":
                print("Missing Information")
                return SubAgentReponseTypes.MISSING_INFO, missing_info

            answer = conversation_json["speak_to_user"] if "speak_to_user" in conversation_json else None
            if answer and answer != "":
                result = conversation_json["result"] if "result" in conversation_json else None
                final_answer = {"answer": answer, "result": result}
                print("Answering the user")
                return SubAgentReponseTypes.ANSWER, final_answer
            

        command = response_json["command"] if "command" in response_json else None
        if command and "name" in command:
            #TODO Make the functions (commands) actually return the result (and only the result)
            
            if command["name"] == "search_immo":
                print("Using search_immo command")
                immoscraper = ImmoScoutScaper.ImmoScoutScraper()
                return Commands.SEARCH_IMMO, immoscraper.scrapImmos(command["args"])

            elif command["name"] == "average_price":
                print("Using average_price command")
                return Commands.AVERAGE_PRICE, get_avg_buy_rent_price.get_price(command["args"])
            
            elif command["name"] == "analyze_immo":
                print("Using analyze_immo command")
                return Commands.ANALYZE_IMMO, ImmoCalculator.ImmoCalculator.analyze_immo(command["args"])

            elif command["name"] == "task_complete":
                print("Using task_complete command")
                return Commands.TASK_COMPLETE, 0


def _get_json_from_ai(bad_json: str) -> str or int:
    # If nothing works, trying to get GPT3.5 to parse the response
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
