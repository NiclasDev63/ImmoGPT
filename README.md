# ImmoGPT: A Chatbot specified to Real Estate
ImmoGPT is an LLM based Chatbot which can be used to find a suitable property.  
It uses GPT4FREE (https://github.com/xtekky/gpt4free) to gain free access to GPT3.5 and GPT4.  
Currently ImmoGPT only has access to the german real estate market through ImmoScout24.  
Since the ImmoScout24 API is unfortunately very expensive (at least the last time I requested a key) ImmoGPT crawls the site using a conventional web crawler.


## 🚀 Quickstart
1. run  ``` pip install -r requirements.txt ```
2. Create a RapidAPI Account to get an API key which is needed to acces the GeoDB Cities API
3. Set the RapidAPI API key as environment variable  
 Windows: ``` set X_RapidAPI_Key='yourkey' ```  
 Linux / MacOS: ```echo "export X_RapidAPI_Key='yourkey'" >> ~/.zshrc```
4. extract the cookie "reese84" from your browser, which is used to scrap https://www.immobilienscout24.de/
5. paste the cookie in the following file ```./tools/ImmoScoutScraper.py``` as attribute ```self.reese84```



## ✅ TODOs
- [ ] (Add google search)  
- [ ] Add Immo calculator  
- [ ] Maybe add more Parameters to ImmoScout Scrapper  
- [ ] Search for useful APIs  
- [ ] Add loop and memory for chatbot  
- [ ] Add token counter if memory is used, so token limit does not get exceeded (can use OPENAI code to approximate tokens)

 
