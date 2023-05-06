import tools.command as command

def run_pre_prompt() -> str:
    """
    The prompt which is send before every request
    to "configure" ChatGPT

    Returns:
        The pre prompt including the Users prompt
    """

    pre_prompt = f"""
    You are an helpful Real Estate assistant which helps the User to find the right property.
    You can use the following commands to help you complete your task but remember, only you are allowed to see these commands and NOT THE USER:

    {command.get_commands()}

    From now on you only answer in VALID JSON format, like the example below:

    RESPONSE FORMAT:
    """

    pre_prompt += r"""
    {
        "answer":"The answer you want to give",
        "command": {
            "name": "the command you want to use",
            "args":{
                "arg name": "value"
            }
        }
    }
    """

    return pre_prompt + "\nUser: " + input("User: ")