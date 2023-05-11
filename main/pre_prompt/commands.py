def get_commands():
    """List of commands the AI can use for completing the desired task"""

    commands = """
    
    COMMANDS:

    1. ImmoScout24 Search: "search_immo",
            args:{
                    "acquisition_type": "<acquisition_type of property>",
                    "min_price": "<min_price of property> (optional)",
                    "max_price": "<max_price of property>(optional)",
                    "location": "<location of property>",
                    "radius" : "<radius around location>(optional)",
                    "min_living_space": "<min livingspace>(optional)",
                    "max_living_space": "<max livingspace>(optional)",
                    "number_of_rooms": "<number of rooms>"(optional)"
                }

    2. Property Analyzation: "analyze_immo":, 
        args:[
                {"property_1":
                    {"link": "ImmoScout24 link (use this if available)"} OR
                    {
                    "acquisition_type": "<acquisition_type of property>",
                    "price": "<Price of property>",
                    "location": "<location of property>",
                    "squaremeter": "<squaremeter>"
                    }
                }
                ]
            

    3. Calculate average property price in Area: "average_price",
        args:{
                "location": "<location of property>"
                "acquisition_type": "<acquisition_type>"
                "squaremeter": "<squaremeter>"
            }
        description:"

    4. Task Complete (Shutdown): "task_complete", args: "reason": "<reason>", description: "use this, if you finished your main task"

    """

    return commands