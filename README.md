# ZHAW MatchMaking

## Hosted on Replit

- [Panel App](https://zhaw-matchmaking-app--przvlprd.repl.co/app)
- REST API: [Docs](https://zhaw-matchmaking-api--przvlprd.repl.co/docs)
  - send your request to either (see [below](#requests) for 
    instructions): </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query/` </br>
  `https://zhaw-matchmaking-api--przvlprd.repl.co/query-stream/`

## Local Setup

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

