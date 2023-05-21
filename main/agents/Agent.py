from utils.memory import Memory


class Agent:

    """
    Is the parent class of all agents

    Attributes:
        memory (Memory): contains the memory of the agent
    """

    def __init__(self):
        
        self.memory = Memory()

    
    def run_agent(self):
        """The main loop of the agent"""
        pass

    @staticmethod
    def _create_context(resp_format: str, regulations: str, main_task: str="", optional_context: str="") -> str:

        """
        creates context which is send with every prompt

        Args:
            resp_format: The response format of the respective agent

            regulations: The regulations of the respective agent

            main_task: The main task of the subagent

            optional_context: optional context which can be added if needed

        Returns:
            The agents context

        
        """

        context = resp_format

        context += regulations

        context += main_task

        context += optional_context

        context += "REMEMBER TO ONLY USE THE DESIRED RESPONSE FORMAT"

        return context

    @staticmethod
    def get_reponse_format() -> str:
        """
        Returns:
            the respective response format

        """

        pass



    def _init_memory(self):
        """initializes the memory of the agent"""
        pass
    @staticmethod
    def get_regulations() -> str:
        """
        Returns:
            the respective regulations of the agent

        """
        pass


