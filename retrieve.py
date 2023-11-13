#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

_ = load_dotenv(find_dotenv())

# Check for required environment variables
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "PINECONE_API_KEY",
                     "PINECONE_ENVIRONMENT", "PINECONE_INDEX"]
for env_var in REQUIRED_ENV_VARS:
    if os.environ.get(env_var, None) is None:
        raise Exception(f"Missing `{env_var}` environment variable.")

# Initialize vector database
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX")
vectordb = Pinecone.from_existing_index(
    PINECONE_INDEX_NAME, OpenAIEmbeddings()
)


def get_relevant_results(query: str, search: str = "sim", k: int = 4) \
        -> list[list[str], list[str]]:
    """
    Perform a search on the vector database using the user input as a query.
    Return the unique names and sources of the retrieved chunks (no
    duplicates).

    Options:
    - `query` (str): The user input.
    - `search` (str, optional): The type of search. Use 'sim' for similarity
        search (default) or 'mmr' for maximum marginal relevance search.
    - `k` (int, optional): The number of results retrieved.

    Returns:
    - list[list[str], list[str]]: Nested list of str, the first list with the
        full names of the retrieved sources, the second list with the URLs
        to the sources.
    """
    if search == "sim":
        retrieved_chunks = vectordb.similarity_search(query, k=k)
    else:
        retrieved_chunks = vectordb.max_marginal_relevance_search(query, k=k)

    sources = []
    names = []
    for result in retrieved_chunks:
        handle = result.metadata['source']
        name = result.metadata['name'].encode('latin-1').decode('utf-8')
        if name not in names:
            sources.append(f"https://www.zhaw.ch/de/ueber-uns/person/{handle}")
            names.append(name)

    return [names, sources]
