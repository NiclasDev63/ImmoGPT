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
3. Create a OpenAI Account to get an API key
4. Set the OpenAI API key as environment variable  
 Windows: ``` setx OPENAI_KEY 'yourkey' ```  
 Linux / MacOS: ```echo "export OPENAI_KEY='yourkey'" >> ~/.zshrc```
5. extract the cookie "reese84" from your browser, which is used to scrap https://www.immobilienscout24.de/
6. paste the cookie in the following file ```./tools/ImmoScoutScraper.py``` as attribute ```self.reese84```



## ✅ TODOs
- [ ] implement logger instead of using print for better understanding and logging the behaviour of AI
- [ ] find free and good embedding models for similarity search  
- [ ] add milvus support
- [ ] 
- [ ] finish tools
- [ ] make tools microservice ? 
- [ ] refactor code
- [ ] make code prettier
