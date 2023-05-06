import utils.pre_prompt as pre_prompt
import utils.response_parser as response_parser
import utils.call_AI as call_AI


""" if __name__ == "__main__":
    chats = [{"role": "system", "content": pre_prompt.run_pre_prompt()}]
    while 1:
        chats.append({"role": "user", "content": input("User: ")})
        resp = call_AI.make_request(chats)
        chats.append({"role": "assistant", "content": resp})
        resp_json = response_parser.response_parser(resp)
        print(chats) """


prompt = [{"role": "system", "content": pre_prompt.run_pre_prompt()}]
prompt.append[{"role": "user", "content": input("User: ")}]
resp = call_AI.make_request(prompt)