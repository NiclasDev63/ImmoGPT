import json
import re
import make_request


def response_parser(response: str) -> json:
    """
    Parses the response to get the answer and commands

    Args:
        response (str): The raw reponse from the API call

    Returns:
        json: Valid json which includes the command and answer

    Raises:
        json.decoder.JSONDecodeError: If the reponse can't get converted into JSON
    """


    response_json = ""

    try:
        response_json = json.loads(response)
    except json.decoder.JSONDecodeError:
        response_json = "{" + re.split("{|}", response)[1] + "}"
        response_json = re.sub("\n","", response_json)

        try:
            response_json = json.loads(response_json)
        except json.decoder.JSONDecodeError:
            prompt = f"Search for the two outer brackets in the following text \
            and only return the JSON within it including the brackets: {response_json}"

            try:
                response_json = json.loads(make_request(prompt))
            except json.decoder.JSONDecodeError:
                print("Cant extract json from reponse")

    if response_json != "":
        return response_json