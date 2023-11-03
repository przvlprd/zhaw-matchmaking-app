# ZHAW MatchMaking App

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

### Panel App (wip)

```shell
panel serve app.py --autoreload --show
```

### Server / REST API (tbd)
- not working yet
```shell
uvicorn.run(app, host="0.0.0.0", port=8000)
```
