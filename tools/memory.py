class Memory:
    memory: list[dict] = []

    @classmethod
    def get(cls) -> list[dict]:
        return cls.memory
    
    @classmethod
    def add(cls, chatlog: dict):
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
        if len(cls.memory) + 1 > 10:
            cls.remove()
        cls.memory.append(chatlog)

    @classmethod
    def remove(cls):
        if len(cls.memory) > 0:
            cls.memory.pop(0)

    @classmethod
    def clear(cls):
        cls.memory = []