# ImmoGPT: A Chatbot specified to Real Estate
ImmoGPT is an LLM based Chatbot which can be used to find a suitable property.  
It uses GPT4FREE (https://github.com/xtekky/gpt4free) to gain free access to GPT3.5 and GPT4.  
Currently ImmoGPT only has access to the german real estate market through ImmoScout24.  
Since the ImmoScout24 API is unfortunately very expensive (at least the last time I requested a key) ImmoGPT crawls the site using a conventional web crawler.


## 🚀 Quickstart
1. run  ``` pip install -r requirements.txt ```
2. Create a RapidAPI Account to get an API key which is needed to acces the GeoDB Cities API
3. Set the RapidAPI API key as environment variable  
 Windows: ``` setx X_RapidAPI_Key 'yourkey' ```  
 Linux / MacOS: ```echo "export X_RapidAPI_Key='yourkey'" >> ~/.zshrc```
4. extract the cookie "reese84" from your browser, which is used to scrap https://www.immobilienscout24.de/
5. paste the cookie in the following file ```./tools/ImmoScoutScraper.py``` as attribute ```self.reese84```



## ✅ TODOs
- [ ] find free and good embedding models for similarity search  
- [ ] add milvus support
- [ ] elaborate execution flow
1. First task
2. start agent to create plan and add bullet points to task list
3. loop through task list
4. start agent to execute first task (should add short term task (to short term task list) if needed to achieve its main goal)
5. back to 2. until main task list is empty
6. present final answer to the user
- [ ] edit / create prompts
- [ ] find best way to create context
- [ ] finish tools
 
