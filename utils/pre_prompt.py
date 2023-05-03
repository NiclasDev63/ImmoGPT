

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
        "google_args": "The prompt you want so search for in google"

    "calculate": "helps you add two numbers"
        "number1": "the first number to add"
        "number2": "the second number to add"

    Use the commands only if needed (if you not sure about your answer).
    These commands are only for you and the User cant use these commands.

    From now on you only answer in JSON format, like the example below:
    """

    pre_prompt += r"""
    {
        "answer":"The answer you want to give",
        "command": {
            "name": "command name",
            "args":{
                "arg name": "value"
            }
        }
    }
    """

    return pre_prompt + input("User: ")