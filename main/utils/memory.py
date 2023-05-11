import utils.get_tokens as get_tokens
from pre_prompt.pre_prompt import pre_prompt

MAX_TOKENS = 4096 #Using gpt-3.5-turbo-0301


class Memory:
    
    def __init__(self):
        self.memory: list[dict] = []
        self.memory.append({"role":"system", "content": pre_prompt()})


    def get(self) -> list[dict]:
        return self.memory
    

    def get_latest_task(self) -> str:
        for i in reversed(self.memory):
            if i["role"] == "user":
                return i["content"]
            
    
    def get_mem_as_str(self) -> str:
        mem = ""
        for i in self.memory:
            mem += i["content"]
        return mem
    

    def add(self, chatlog: dict):
        """max memory size is 10 entries"""
        
        if not isinstance(chatlog, dict):
            raise TypeError("chatlog has to be of type dict")
        if not "role" in chatlog:
            raise KeyError("Missing key role")
        if not chatlog["role"] in ["system", "user", "assistant"]:
            raise NameError(f"{chatlog['role']} is not a valid role")
        if not "content" in chatlog:
            raise KeyError("Missing key content")
        if chatlog["content"] == "":
            return 
        
        while get_tokens(self.get_mem_as_str() + chatlog["content"]) > MAX_TOKENS:
            self.remove()

        self.memory.append(chatlog)


    def remove(self):
        if len(self.memory) > 1:
            self.memory.pop(1)
        raise IndexError("Can't delete pre prompt")


    def clear(self):
        self.memory = []