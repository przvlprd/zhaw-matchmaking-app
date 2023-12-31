<div align="center">

# ZHAW MatchMaking

</div>

A simple chatbot which takes a user query as input and suggests people to 
collaborate with based on the context of their profile data from the 
<a href='https://www.zhaw.ch' target='_blank'>ZHAW Homepage</a>.<br><br>


Interact with it via a user-friendly frontend made with Panel or as a REST 
API. The backend is powered by GPT-4 Turbo with LangChain as a wrapper and 
Pinecone as a hosted vector database.

<div align="center">

#### <a href='https://zhaw-matchmaking-app--przvlprd.repl.co/app' target='_blank'>Try it out</a>

</div>
<div align="center">
  <img src="img.png" width="400"/>
</div>

## Contents

- [Hosted on Replit](#hosted-on-replit)
- [Local Setup](#local-setup)
  - [Prerequisites](#prerequisites)
  - [Panel App](#panel-app)
  - [REST API](#server--rest-api)
    - [Request Templates](#request-templates)
- [TBD](#tbd)

## Hosted on Replit

- <a href='https://zhaw-matchmaking-app--przvlprd.repl.co/app' target='_blank'>Panel App</a>
- <a href='https://zhaw-matchmaking-api--przvlprd.repl.co/' target= '_blank'>REST API</a>
  - send your request to either (see [below](#request-templates) for 
    instructions): </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query/` </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query-stream/` </br>

*(it may take up to 30s to get the Replit repos running)*

<div align="center">
<a href="demo.png" target="_blank">
  <img src="demo.png" alt="Demo" width="300"/>
</a>
</div>
<div align="center">
Demo of the Panel App
</div>



## Local Setup
Follow the notebook `Guide from Scratch.ipynb` to reproduce the steps 
needed to run the bot locally or deploy it.

### Prerequisites
- create & activate virtual environment
```shell
# PowerShell
python -m venv env
.\env\Scripts\activate

# Linux / WSL
virtualenv --python python3.11 venv
source venv/bin/activate
```

- install requirements
```shell
pip install -r requirements.txt
```

- replace environment variables in `.env`:
  - `OPENAI_API_KEY` 
  - `PINECONE_API_KEY`
  - `PINECONE_ENVIRONMENT`
  - `PINECONE_INDEX`

### Panel App

```shell
panel serve app.py --autoreload --show
```

### Server / REST API

- run the uvicorn server
```shell
python server.py
```

#### Request Templates
- send a POST request to `http://localhost:8000/query/` with
  - **neccessary**
    - `user_query` - the search query or user input
  - **optional**
    - `search_type` - the search type performed on the vectordb
      - `"sim"` similarity search *(default)*
      - `"mmr"` maximum marginal relevance search
    - `num_chunks` - number of retrieved chunks from vectordb
      - `3` *(default)*, int 1 - 50
    - `full_context` - switch between shorter version of user profile for 
      context *(default = false)* or full version for higher accuracy but 
      slower response generation *(true)*
- returns **JSON**
```shell
curl -X POST -H "Content-Type: application/json" -d '{
    "user_query": "your search query",
    "search_type": "sim",
    "num_chunks": 3,
    "full_context": false
}' http://localhost:8000/query/
```

##### Streaming

- as above, but send a POST request to `http://localhost:8000/query-stream/`
- returns **streamed text**
```shell
curl -X POST -H "Content-Type: application/json" -d '{
    "user_query": "your search query",
    "search_type": "sim",
    "num_chunks": 3,
    "full_context": false
}' http://localhost:8000/query-stream/
```

##### Example
- running the <a href='https://zhaw-matchmaking-api--przvlprd.repl.co/' target= '_blank'>REST API</a>
on Replit (make sure the repo is running first):
```
curl -X POST -H "Content-Type: application/json" -d '{
    "user_query": "ich möchte virtual reality in der schule einsetzen"
}' https://zhaw-matchmaking-api--przvlprd.repl.co/query/
```

## TBD
This project serves as a first *proof-of-concept* as part of an internship. 
Things which could be done 
include:
- [ ] thorough debugging and testing
  - error handling & unit tests
  - add logging for user queries and generated responses
    - currently only the deployed version uses `LangSmith` to log llm calls
- [ ] refactor to OOP
- [ ] add interactive chatbot capabilities (and memory)
  - only use retrieval when necessary
  - be able to converse with the user
- [ ] use keyword extraction from the user query (instead of  the whole 
  query for retrieval)
- [ ] get more varied results
  - e.g. random selection from retrieved sources
- [ ] get rid of possibly bloated *LangChain* implementation
  - use custom logic (see point below)
- [ ] take advantage of GPT-4 Turbo's increased context window size (up to 
  128k tokens) for analyzing the relevant profile documents
- [ ] automate scraping the website & updating the vectordb for removed, 
  newly added, and changed profiles
  - catch invalid profiles instead of letting LLM generate reply based on 
    missing context
- [ ] add multilingual support
  - detect the user input language and use it for response generation 
    (currently forced to reply in German)
- [ ] add working frontend (e.g. with React) other than the current Panel 
  template
- possibly more...

**Feel free to reach out in case something is broken!**

## Author

**Maximilian Krupop**
- [GitHub](https://github.com/przvlprd)
- [LinkedIn](https://www.linkedin.com/in/maximilian-krupop/)
