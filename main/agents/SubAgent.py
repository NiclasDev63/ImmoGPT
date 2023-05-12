from agents.Agent import Agent
from utils.response_parser import response_parser
from utils.call_AI import make_request
from commands.commands import Commands

class SubAgent(Agent):

    def __init__(self, maint_task: str):
        super().__init__("sub")

        self.main_task = f"MAIN TASK:\n{maint_task}"
        super().memory.get(0)["content"] += self.main_task

        self.short_term_tasks = []

    
    def _create_context(self) -> str:
        return super()._create_context(self._get_reponse_format(), self._get_regulations(), self.main_task)

    def run_agent(self):
        #TODO relocate Case logic and memory management to _process_result
        
        while 1:
            result =  response_parser(make_request(super().memory.get()))
            if result != None:
                if result == 0: break
                prompt = self._create_context() + "\n" + result
                if result == 1: 
                    prompt += "User: " + input("User: ")
                    super().memory.add({"role": "user", "content": prompt}) #User Answer
                else: super().memory.add({"role": "system", "content": prompt}) #Result of main task (use breake here too?)
            else: break
        return result

    def _process_result(self, result):
        
        if isinstance(result, tuple):
            #TODO Implement cases
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
                    pass
                case Commands.ANALYZE_IMMO:
                    pass
                case Commands.AVERAGE_PRICE:
                    pass
                case Commands.TASK_COMPLETE:
                    pass
                #TODO get user input
                case Commands.MISSING_INFO:
                    pass
                case Commands.ANSWER:
                    pass



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
                "missing_information":"information you need to complete the task",
                "mssing_info": "short summary of the missing information",
                "speak_to_user":"if you need to present something (including your results)"
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

        """

        return regulations