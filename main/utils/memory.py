from utils.get_tokens import num_tokens_from_string

MAX_TOKENS = 4096 #Using gpt-3.5-turbo-0301

class Memory:

    def __init__(self):
        self.memory: list[dict] = []


    def get(self, idx: int=None) -> dict or list[dict]:
        if idx != None: return self.memory[idx]
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
    

    def get_mem_token_count(self) -> int:
        return num_tokens_from_string(self.get_mem_as_str())
    

    def add(self, chatlog: dict):
        """max memory size is 4096 tokens"""
        
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
        
        while self.get_mem_token_count() + num_tokens_from_string(chatlog["content"]) > MAX_TOKENS:
            self.remove()

        self.memory.append(chatlog)


    def remove(self):
        if len(self.memory) > 1:
            self.memory.pop(1)
        raise IndexError("Can't delete pre prompt")


    def clear(self):
        while len(self.memory) > 1:
            self.memory.remove()