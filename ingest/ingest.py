#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from load_profile_data import loader

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())


def check_environment_variables():
    """
    Check for the presence of required environment variables.

    Raises:
        Exception: If any of the required environment variables are missing.
    """
    required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY",
                     "PINECONE_ENVIRONMENT", "PINECONE_INDEX"]
    for var in required_vars:
        if os.environ.get(var, None) is None:
            raise Exception(f"Missing `{var}` environment variable.")


def main():
    """
    Main function for processing and indexing profile data.

    - Load profile data.
    - Split text into chunks.
    - Add chunks to Pinecone vector database with OpenAI embeddings.
    """
    # Load profile data
    data = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    # Add chunks to Pinecone vector database
    Pinecone.from_documents(
        documents=all_splits,
        embedding=OpenAIEmbeddings(show_progress_bar=True),
        index_name=os.environ.get("PINECONE_INDEX")
    )
    print("Done.")


if __name__ == "__main__":
    # Check for required environment variables
    check_environment_variables()
    # Execute main function
    main()
