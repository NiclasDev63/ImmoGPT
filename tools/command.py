def get_commands():
    """List of commands the AI can use for completing the desired task"""

    commands = """
    COMMANDS:

        "google": "Searches the web and can help you find informations"
            "google_args": "The prompt you want so search for in google"

        "ImmoScout": "Use this command to search for real estate"
            "type": "buy or rent (MUST BE SPECIFIED)"
            "minPrice": "the min price the User wants to pay (if specified)"
            "maxPrice": "the max price the User wants to pay (if specified)"
            "location": "the location the User is interested in (MUST BE SPECIFIED)"
            "radius" : "the radius around the location as integer (if specified)"
            "minLivingSpace": "min size of house or apartment"
            "maxLivingSpace": "max size of house or apartment"

    if any of the arguments which must be specified isn't specified and you can't guess what the User wants, tell the User to specifie these arguments

    """

    return commands