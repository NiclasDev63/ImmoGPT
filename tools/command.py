def get_commands():
    """List of commands the AI can use for completing the desired task"""

    commands = """
     COMMANDS:

    1. "ImmoScout": "Only use this command to search for available real estate"
        "args":{
            "acquisition_type": "<acquisition_type>"
            "minPrice": "<minPrice of property>"
            "maxPrice": "<maxPrice of property>"
            "location": "<location of property>"
            "radius" : "<radius>"
            "minLivingSpace": "<min livingspace>"
            "maxLivingSpace": "<max livingspace>"
            }

    2. "calcImmo": "Only use this command to analyze a property"
        "args":{ "The same as command "ImmoScout" uses}

    3. "averagePrice": "Helpful to find out if a purchase or rental price is appropriate"s
        "args":{
            "location": "<location of property>"
             "acquisition_type": "<acquisition_type>"
            "squaremeter": "<squaremeter>"
        }

    4. "getMemory": "Use this if you want to recall something from the past"

    Remember every command has a cost, so be smart and efficient and only use them if you have all the needed information.
    Exclusively use the commands listed in double quotes e.g. "command name"

    """

    return commands