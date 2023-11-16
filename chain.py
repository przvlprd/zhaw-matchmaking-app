#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv, find_dotenv
from ingest.preprocess_profile_data import preprocess_profile

from langchain.chat_models import ChatOpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.question_answering import load_qa_chain


_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)


def get_context(name: str, url: str, query: str, full: bool = False) -> str:
    """
    Get context about a person by scraping their profile page and
    running a question-answering chain. Choose whether to get the full profile
    text with publications (can lead to very high latency!) or a shorter
    version which helps generate replies much faster. However, important
    context may get lost and diminish the quality of the generated responses.

    Parameters:
    - name (str): The name of the person.
    - url (str): The URL of the person's profile page.
    - query (str): The user's query.
    - full (bool): Choose whether to get the full profile text with
                   publications or a shorter version. Default: False (shorter)

    Returns:
    str: Contextual information about the person.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile = soup.find('div', class_='zhaw-person')

    if full:
        cleaned_profile = preprocess_profile(profile.get_text())
    else:
        # Check if there is a publications header and discard the content
        publication_header = soup.find('h2', string='Publikationen')
        if publication_header:
            index_pub_header = profile.get_text().find(
                publication_header.get_text())

            # Extract content before the index
            cleaned_profile = preprocess_profile(
                profile.get_text()[:index_pub_header]
            )
        else:
            # If the header is not found, use the entire profile
            cleaned_profile = preprocess_profile(
                profile.get_text()
            )

    return run_qa_document_chain(name, cleaned_profile, query)


def run_qa_document_chain(name: str, input_document: str, query: str) -> str:
    """
    Run a question-answering document chain.

    Parameters:
    - name (str): The name of the person.
    - input_document (str): The preprocessed profile data.
    - query (str): The user's query.

    Returns:
    str: The result of the question-answering chain.
    """
    question = (
        f"Answer in German. Find a connection to why this person was "
        f"found as a fitting match to the user query. Start your "
        f"response with the person's name. If you are not sure, find "
        f"something about the person the user could be interested in. "
        f"Query: {query} "
        f"Helpful Answer: {name}"
    )

    return qa_document_chain.run(
        input_document=input_document,
        question=question
    )
