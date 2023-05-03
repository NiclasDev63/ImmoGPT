

def run_pre_prompt() -> str:
    """
    The prompt which is send before every request
    to "configure" ChatGPT

    Returns:
        The pre prompt including the Users prompt
    """

    pre_prompt = f"""
    You can use the following commands to help you complete your task:

    COMMANDS:

    "google": "Searches the web and can help you find informations"
        "args": "The prompt you want so search for in google"

    "calculate": "helps you answer mathematical questions"

    These commands are only for you and the User cant use these commands

    From now on you only answer in JSON format, like the example below:
    """

    pre_prompt += '{ \
        "answer": "your answer to the question from the user", \
        "commandName": "the command you want to use" \
        "args": "The prompt you want so search for in google" \
    }'

    return pre_prompt + input("User: ")