import gpt4free
import random
from gpt4free import Provider
import openai
import tools.memory as memory

def make_request(prompt: str) -> str:
    """
    Makes a request to one Provder from provider_list

    Args:
        prompt (str): The prompt to send to the API

    Returns:
        str: The answer to the prompt

    Raises:
        Exception: If any error occurs while making the request
    """


    # openai.api_key = OPENAI_API_KEY
    # print("USING AI AND PRINTING MEMORY: ", memory.Memory.get())
    # completion = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages= memory.Memory.get()
    # )

    # return completion.choices[0].message.content


    """ called_provider = set()

        provider_list = {
            "You": Provider.You,
            "Theb": Provider.Theb,
            "UseLess": Provider.UseLess
        }

        get_provider = lambda: random.choice(list(provider_list.items()))
        
        response = ""

        while 1:

            if len(called_provider) == 3: print("No Provider available")

            choosen_provider = get_provider()
            called_provider.add(choosen_provider[1])
            print("USING: ", choosen_provider[0])

            try:
                response = gpt4free.Completion.create(choosen_provider[1], prompt=prompt)
                break
            except Exception as e:
                print("Exception thrown while using: ", choosen_provider[0])
                print("Error: ", e)
    

        if choosen_provider[0] == "UseLess": return response["text"]
        else: return response
        """