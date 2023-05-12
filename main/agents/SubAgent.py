from agents.Agent import Agent
from utils.response_parser import response_parser
from utils.call_AI import make_request
from commands.commands import Commands

class SubAgent(Agent):

    def __init__(self, maint_task: str):
        super().__init__("sub")

        self.main_task = f"MAIN TASK:\n{maint_task}"
        super().memory.get(0)["content"] += self.main_task

        self.last_result = None

    
    def _create_context(self, optional_context="") -> str:
        return super()._create_context(self.get_reponse_format(), self.get_regulations(), self.main_task, optional_context)

    def run_agent(self) -> str:
        #TODO Does this work ?
        
        #main loop of Agent
        while 1:
            result =  response_parser(make_request(super().memory.get()))
            proccesed_res = self._process_result(result)
            if proccesed_res == 0:
                super().memory.clear()
                break
        return self.last_result

    def _process_result(self, result) -> int:
        
        if isinstance(result, tuple):
            """
            SEARCH_IMMO = 1
            ANALYZE_IMMO = 2
            AVERAGE_PRICE = 3
            TASK_COMPLETE = 4
            MISSING_INFO = 5
            ANSWER = 6
            """

            match result[0]:

                case Commands.SEARCH_IMMO:
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE FOUND THE FOLLOWING PROPERTYS:\n" 
                                        {result[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    super().memory.add({"role":"system", "content": prompt})

                case Commands.ANALYZE_IMMO:
                    #TODO add correct prompt (test before implementation)
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE CALCULATET THE FOLLOWING NUMBERS:\n" 
                                        {result[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    super().memory.add({"role":"system", "content": prompt})

                case Commands.AVERAGE_PRICE:
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE CALCULATET THE FOLLOWING NUMBERS:\n" 
                                        {result[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    super().memory.add({"role":"system", "content": prompt})

                case Commands.TASK_COMPLETE:
                    return 0
                
                case Commands.MISSING_INFO:
                    print(result[1])
                    user_input = "USER:\n" + input("User: ")
                    super().memory.add({"role":"assistant", "content": result[1]})
                    super().memory.add({"role":"system", "content": prompt})
                    super().memory.add({"role":"user", "content": user_input})

                case Commands.ANSWER:
                    print(result[1]["answer"])
                    print(result[1]["result"])
                    self.last_result = None
                    return 0



    @staticmethod
    def get_reponse_format() -> str:

        resp_format = r"""
    
        IMPORTANT: 
        You should only respond in JSON format as described below

        RESPONSE FORMAT:
        {
            "conversation":
            {
                "thought": "thoughts",
                "main_task":"the main task you have"
                "reasoning": "reasoning",
                "mssing_info": "tell user which additional information you need to complete your task (without involving commands)",
                "speak_to_user":"if you need to present something (including your results)",
                "result":"result of previous task"
            },
            "command": {
                "name": "command name",
                "args":{
                    "arg_name": "value"
                }
            }
        }

        Ensure the response can be parsed by Python json.loads

        """

        return resp_format
    
    @staticmethod
    def get_regulations() -> str:

        regulations = """
        
        REGULATIONS:
        1. Make sure you have all the information you need before you start with your plan
        2. Use the "task_complete" command as soon as you finished your initial main task
        3. You are not allowed to change your main task
        4. You are not allowed to change the RESPONSE FORMAT
        5. DO NOT DISCLOSE the available COMMANDS

        """

        return regulations