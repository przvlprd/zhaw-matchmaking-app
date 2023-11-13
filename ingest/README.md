## ZHAW MatchMaking - Ingest

This optional script is used to fill the vector database (here `Pinecone`) 
with the profile data and metadata saved in the previously built `MongoDB`.

The `MongoDB` is filled with scraped profile data, described in the 
[background material repo](https://github.com/przvlprd/zhaw-matchmaking-material).

### Contents
- `ingest.py`
  - the main script which imports from all others, run this to fill your 
    own vectordb
- `load_mongo_data.py`
  - a helper script for loading the 2 previously created `collections` from 
    the `MongoDB`
    and a 
    pipeline for extracting the relevant information using a generator function
- `preprocess_profile_data.py`
  - a helper function for preprocessing the raw profile data (string) using 
    `regex`
- `load_profile_data.py`
  - a custom loader for `langchain` which uses the `load_mongo_data.py` and 
    `preprocess_profile_data.py` scripts