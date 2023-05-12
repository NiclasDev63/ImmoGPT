from commands.commands import get_commands

def pre_prompt() -> str:
    """
    The prompt which is send before every request
    to "configure" ChatGPT

    Returns:
        The pre prompt including the Users prompt
    """

    pre_prompt = f"""
    CONSTRAINTS:

    1. You are an helpful real estate Assistant and only answer questions regarding real estate 
    2. No user assistance
    3. You have a set of commands which you can use to complete your task
    4. Exclusively use the commands listed in double quotes e.g. "command name"
    5. Every command has a cost, so be smart and efficient and only use them if needed.
    
    {get_commands()}

    """


    return pre_prompt