import utils.pre_prompt as pre_prompt
import utils.response_parser as response_parser
import utils.make_request as make_request

prompt = pre_prompt.run_pre_prompt()


resp = make_request(prompt)
resp_json = response_parser(resp)
print(resp_json)


