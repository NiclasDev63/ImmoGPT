import utils.pre_prompt as pre_prompt
import utils.response_parser as response_parser
import utils.call_AI as call_AI
import utils.memory as memory


""" if __name__ == "__main__":
    chats = [{"role": "system", "content": pre_prompt.run_pre_prompt()}]
    while 1:
        chats.append({"role": "user", "content": input("User: ")})
        resp = call_AI.make_request(chats)
        chats.append({"role": "assistant", "content": resp})
        resp_json = response_parser.response_parser(resp)
        print(chats) """

if __name__ == "__main__":
    prompt = pre_prompt.run_pre_prompt()

    while 1:
        memory.Memory.add({"role":"system", "content": prompt})
        memory.Memory.add({"role":"user", "content": input("User: ")})
        #print("MEMORY OUTPUT: ", memory.Memory.get_mem_as_str())
        resp = call_AI.make_request(memory.Memory.get_mem_as_str())
        resp = response_parser.response_parser(resp)
