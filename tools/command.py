def get_commands():
    """List of commands the AI can use for completing the desired task"""

    commands = """
    COMMANDS:

        "ImmoScout": "Only use this command to search for available real estate"
            "args":{
                "acquisition_type": "buy or rent (MUST BE SPECIFIED)"
                "minPrice": "the min price the User wants to pay (if specified)"
                "maxPrice": "the max price the User wants to pay (if specified)"
                "location": "only city the User is interested in (MUST BE SPECIFIED)"
                "radius" : "the radius around the location as integer (if specified)"
                "minLivingSpace": "min size of house or apartment"
                "maxLivingSpace": "max size of house or apartment"
                }

        "calcImmo": "Only use this command to analyze a property"
            "args":{
                "acquisition_type": "buy or rent (MUST BE SPECIFIED)"
                "minPrice": "the min price the User wants to pay (if specified)"
                "maxPrice": "the max price the User wants to pay (if specified)"
                "location": "only city the User is interested in (MUST BE SPECIFIED)"
                "radius" : "the radius around the location as integer (if specified)"
                "minLivingSpace": "min size of house or apartment"
                "maxLivingSpace": "max size of house or apartment"
            }

        "averagePrice": "Only use this command to find out if a purchase or rental price is appropriate"
            "args":{
                "address": "The address of the property"
                "acquisition_type": "buy or rent (MUST BE SPECIFIED)"
                "squaremeter": "the size of the house or apartment"
                "user_price": "the price the user pays or paid"
            }


    """

    return commands