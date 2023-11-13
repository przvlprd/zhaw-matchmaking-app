# ZHAW MatchMaking

A simple chatbot which takes a user query as input and suggests people to 
collaborate with based on the context of their profile data.

## Hosted on Replit

- [Panel App](https://zhaw-matchmaking-app--przvlprd.repl.co/app)
- REST API: [Docs](https://zhaw-matchmaking-api--przvlprd.repl.co/docs)
  - send your request to either (see [below](#requests) for 
    instructions): </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query/` </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query-stream/` </br>

*(it can take up to 30s to get the replit repos running)*
## Local Setup
You need (access to) a vector database which contains the different user 
profiles. You can see the [background material repo](https://github.com/przvlprd/zhaw-matchmaking-material) on how this was created.
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

#### Requests
- send a POST request to `http://localhost:8000/query/` with
  - `user_input` - the search query - **necessary**
  - `search` - the search type *(optional)*
    - `"sim"` similarity search *(default)*
    - `"mmr"` maximum marginal relevance search
  - `k` - number of retrieved documents *(optional)*
    - `4` *(default)*, int 1 - 50
- returns **JSON**
```shell
curl -X POST -H "Content-Type: application/json" -d '{
    "user_input": "your search query",
    "search": "sim",
    "k": 4
}' http://localhost:8000/query/
```

##### Streaming

- as above, but send a POST request to `http://localhost:8000/query-stream/`
- returns **streamed text**
```shell
curl -X POST -H "Content-Type: application/json" -d '{
    "user_input": "your search query",
    "search": "sim",
    "k": 4
}' http://localhost:8000/query-stream/
```

### TBD
This project serves as a first *proof-of-concept*. Things which could be done 
include:
- thorough debugging and testing
- adding interactive chatbot capabilities & memory
  - only using retrieval when necessary
  - would also include keyword extraction from the query, instead of 
    using the whole query for retrieval
- getting more varied results
  - e.g. random selection from retrieved chunks
- taking advantage of GPT-4 Turbo's increased context window size (up to 
  128k tokens) for analyzing the relevant profile documents
  - using the retrieved chunks as context instead of scraping & analyzing 
    the whole profile data each time
- automatically scraping the website & updating the vectordb for removed, 
  newly added, and changed profiles
- multilingual support
  - detecting the input language and using it for response generation
- getting rid of possibly bloated *LangChain* implementation
- working frontend (e.g. with React) other than the current Panel app
- ...