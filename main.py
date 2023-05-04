import utils.pre_prompt as pre_prompt
import utils.response_parser as response_parser
import utils.call_AI as call_AI

prompt = pre_prompt.run_pre_prompt()


resp = call_AI.make_request(prompt)
resp_json = response_parser.response_parser(resp)
