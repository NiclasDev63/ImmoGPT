import tools.command as command

def run_pre_prompt() -> str:
    """
    The prompt which is send before every request
    to "configure" ChatGPT

    Returns:
        The pre prompt including the Users prompt
    """

    pre_prompt = f"""
    You can use the following commands to help you complete your task:

    {command.get_commands()}

    Use the commands only if needed (if you not sure about your answer).
    These commands are only for you and the User cant use these commands.

    From now on you only answer in VALID JSON format, like the example below:
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