from agents.sub_agent.sub_agent import SubAgent
from agents.main_agent.main_agent import MainAgent

def main():
    main_agent = MainAgent()
    while 1:
        user_input = input("User: ")
        resp = main_agent.run_agent(user_input)
        if isinstance(resp, list) and len(resp) > 0:
            result = ""
            print("PLAN: ", resp, "\n")
            for task in resp:
                sub_agent = SubAgent(maint_task=task, initial_memory=result)
                response = sub_agent.run_agent()
                result = response if response else ""
                if result: del sub_agent
                else: break
            main_agent.add_memory(role= "assistant", memory= result)
        elif resp: print("Assistant: ", resp);  main_agent.add_memory(role="assistant", memory=resp)




if __name__ == "__main__":
    main()

#TODO implement logger instead of using print for better understanding and logging the behaviour of AI