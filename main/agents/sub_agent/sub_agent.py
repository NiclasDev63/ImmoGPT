from agents.agent import Agent
from utils.response_parser import response_parser
from utils.call_AI import make_request
from commands.commands import Commands
from agents.sub_agent.SubAgentResponseTypes import SubAgentReponseTypes
from pre_prompt.pre_prompt import pre_prompt

#TODO Make this a variable
CONTINUOS_LIMIT = 3


class SubAgent(Agent):

    def __init__(self, maint_task: str, initial_memory: str = ""):
        Agent.__init__(self)
        self._init_memory()

        self.main_task = f"MAIN TASK:\n{maint_task}"
        self.memory.get(0)["content"] += self.main_task

        if initial_memory:
            prompt = self._create_context(optional_context=initial_memory)
            self.memory.add({"role":"system", "content": prompt})

        self.last_result = None

    def run_agent(self) -> str:
        #TODO Does this work ?
        
        #main loop of Agent
        continuous_counter = 1
        while 1:
            if continuous_counter >= CONTINUOS_LIMIT: print("CONTINUOS_LIMIT reached"); break
            response =  response_parser(make_request(self.memory.get()), agent_type="sub")
            print("SUB AGENT RESPONSE: ", response)
            proccesed_resp = self._process_reponse(response)
            print("SUB AGENT MEMORY: ", self.memory.get())
            if proccesed_resp == 0:
                self.memory.clear()
                break
            continuous_counter += 1
        return self.last_result

    def _init_memory(self):
        pre_prmpt = pre_prompt("sub")
        resp_format = self.get_reponse_format()
        regulations = self.get_regulations()
        self.memory.add({"role": "system", "content": pre_prmpt + resp_format + regulations})

    def _create_context(self, optional_context="") -> str:
        return Agent._create_context(self.get_reponse_format(), self.get_regulations(), self.main_task, optional_context)

    def _process_reponse(self, response: tuple) -> int:
        
        if isinstance(response, tuple):
            """
            SEARCH_IMMO = 1
            ANALYZE_IMMO = 2
            AVERAGE_PRICE = 3
            TASK_COMPLETE = 4
            MISSING_INFO = 5
            ANSWER = 6
            """

            match response[0]:

                case Commands.SEARCH_IMMO:
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE FOUND THE FOLLOWING PROPERTYS:\n" 
                                        {response[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    self.memory.add({"role":"system", "content": prompt})

                case Commands.ANALYZE_IMMO:
                    #TODO add correct prompt (test before implementation)
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE CALCULATET THE FOLLOWING NUMBERS:\n" 
                                        {response[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    self.memory.add({"role":"system", "content": prompt})

                case Commands.AVERAGE_PRICE:
                    self.last_result = f"""
                                        RESULT OF PREVIOUS TASK:\n" 
                                        "YOU HAVE CALCULATET THE FOLLOWING NUMBERS:\n" 
                                        {response[1]}
                                        """
                    
                    prompt = self._create_context(optional_context=self.last_result)
                    self.memory.add({"role":"system", "content": prompt})

                case Commands.TASK_COMPLETE:
                    return 0
                
                case SubAgentReponseTypes.MISSING_INFO:
                    print(response[1])
                    user_input = "USER:\n" + input("User: ")
                    self.memory.add({"role":"assistant", "content": response[1]})
                    prompt = self._create_context()
                    self.memory.add({"role":"system", "content": prompt})
                    self.memory.add({"role":"user", "content": user_input})

                case SubAgentReponseTypes.ANSWER:
                    print(response[1]["answer"])
                    print(response[1]["result"])
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