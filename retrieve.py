import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

vectordb = Chroma(
    persist_directory=r"D:\LLM\zhaw-matchmaking\chroma_db",
    embedding_function=OpenAIEmbeddings()
)


def get_relevant_sources(query: str, search: str = "similarity", k: int = 4):
    if search == "similarity":
        retrieved_chunks = vectordb.similarity_search(query, k=k)
    else:
        retrieved_chunks = vectordb.max_marginal_relevance_search(query, k=k)

    sources = set()
    for result in retrieved_chunks:
        sources.add(result.metadata["source"])

    return sources
