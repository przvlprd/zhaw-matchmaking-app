import os
from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from load_profile_data import loader

_ = load_dotenv(find_dotenv())

if os.environ.get("OPENAI_API_KEY", None) is None:
    raise Exception("Missing `OPENAI_API_KEY` environment variable.")
if os.environ.get("PINECONE_API_KEY", None) is None:
    raise Exception("Missing `PINECONE_API_KEY` environment variable.")
if os.environ.get("PINECONE_ENVIRONMENT", None) is None:
    raise Exception("Missing `PINECONE_ENVIRONMENT` environment variable.")
if (PINECONE_INDEX_NAME := os.environ.get("PINECONE_INDEX")) is None:
    raise Exception("Missing `PINECONE_INDEX` environment variable.")


if __name__ == "__main__":
    # Load
    data = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    # Add to vectorDB
    Pinecone.from_documents(
        documents=all_splits,
        embedding=OpenAIEmbeddings(show_progress_bar=True),
        index_name=PINECONE_INDEX_NAME
    )

    print("Done.")
