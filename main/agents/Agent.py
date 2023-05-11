from utils.memory import Memory
from pre_prompt.pre_prompt import pre_prompt


class Agent:

    def __init__(self):

        self.memory = Memory()

    def _create_context(self, resp_format: str, regulations: str, main_task: str="") -> str:

        context = resp_format

        context += regulations

        context += main_task

        return context


    
    def _get_reponse_format(self) -> str:
        pass

    def _get_regulations(self) -> str:
        pass


