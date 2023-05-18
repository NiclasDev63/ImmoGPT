from agents.agent import Agent
from utils.response_parser import response_parser
from utils.call_AI import make_request
from pre_prompt.pre_prompt import pre_prompt

#TODO Add Milvus (and embedding model) for better context creation (only for main agent)
class MainAgent(Agent):
    #TODO Implement class

    def __init__(self):
        Agent.__init__(self)
        self._init_memory()

    def run_agent(self, user_prompt: str):
        self.memory.add({"role": "user", "content": self._create_context(user_prompt) + "\n"})

        response = response_parser(make_request(self.memory.get()), agent_type="main")
        print("MAIN MEMORY: ", self.memory.get())
        return response[1] if response else None
    
    def _create_context(self, optional_context: str="") -> str:
        return Agent._create_context(self.get_reponse_format(), self.get_regulations(), optional_context=optional_context)

    def add_memory(self, role: str,  memory: str):
        self.memory.add({"role": role, "content": memory})

    def _init_memory(self):
        pre_prmpt = pre_prompt("main")
        self.memory.add({"role": "system", "content": pre_prmpt + "\n" + self._create_context()})

    @staticmethod
    def get_reponse_format() -> str:
        #TODO Improve plan creation
        resp_format = r"""
    
        IMPORTANT: 
        You should only respond in JSON format as described below

        RESPONSE FORMAT:
        {
            "thought": "thoughts",
            "reasoning": "reasoning",
            "plan":[-short bullet list\n-that conveys step-by-step plan\n-including needed information]
            "speak":"your answer, if you dont need a plan or have any questions"
        }

        Ensure the response can be parsed by Python json.loads

        """

        return resp_format
    
    @staticmethod
    def get_regulations() -> str:

        regulations = """
        
        REGULATIONS:

        1. Always make sure you ask the user if you need fourther details before you create a plan
        2. You are NOT ALLOWED TO CHANGE the RESPONSE FORMAT

        """

        return regulations