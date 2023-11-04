import os
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

_ = load_dotenv(find_dotenv())

if os.environ.get("OPENAI_API_KEY", None) is None:
    raise Exception("Missing `OPENAI_API_KEY` environment variable.")
if os.environ.get("PINECONE_API_KEY", None) is None:
    raise Exception("Missing `PINECONE_API_KEY` environment variable.")
if os.environ.get("PINECONE_ENVIRONMENT", None) is None:
    raise Exception("Missing `PINECONE_ENVIRONMENT` environment variable.")
if (PINECONE_INDEX_NAME := os.environ.get("PINECONE_INDEX")) is None:
    raise Exception("Missing `PINECONE_INDEX` environment variable.")

vectordb = Pinecone.from_existing_index(
    PINECONE_INDEX_NAME,
    OpenAIEmbeddings()
)


def get_relevant_results(query: str, search: str = "sim", k: int = 4) \
        -> list[list[str], list[str]]:
    """
    Perform a search on the vector database using the user input as query.
    Return a nested list of full names and corresponding urls to the
    retrieved sources. Only unique sources are returned (no duplicates).

    :param query: str
        the user input
    :param search: str
        the type of search, use "sim" for similarity search (default) or
        "mmr" for maximum marginal relevance search.
    :param k: int
        the number of results retrieved
    :return: list[list[str], list[str]]
        nested list of str, first list with the full names of the retrieved
        sources, the second list with the urls to the sources
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
