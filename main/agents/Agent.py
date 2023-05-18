from utils.memory import Memory


class Agent:

    def __init__(self):
        
        self.memory = Memory()

    def run_agent(self):
        pass

    def _process_reponse(self, response: tuple) -> int:
        pass
    
    def _init_memory(self):
        pass

    @staticmethod
    def _create_context(resp_format: str, regulations: str, main_task: str="", optional_context: str="") -> str:

        context = resp_format

        context += regulations

        context += main_task

        context += optional_context

        context += "REMEMBER TO ONLY USE THE DESIRED RESPONSE FORMAT"

        return context

    @staticmethod
    def get_reponse_format() -> str:
        pass

    @staticmethod
    def get_regulations() -> str:
        pass


