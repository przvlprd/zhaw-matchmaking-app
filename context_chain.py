import re
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.question_answering import load_qa_chain


llm = OpenAI(temperature=0)
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)


def get_context(url: str, query: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile = soup.find('div', class_='zhaw-person')
    raw_profile = profile.get_text()
    cleaned_profile = preprocess_profile(raw_profile)

    return run_qa_document_chain(cleaned_profile, query)


def preprocess_profile(raw_data: str):
    # Remove all obsolete whitespace
    cleaned_str = re.sub(r'\s+', ' ', raw_data)

    # Remove the final "Zurück" in every profile
    cleaned_str = cleaned_str.replace('Zurück', '')

    # Insert whitespace between numbers and letters
    pattern = r'([a-zA-Z])(\d)'
    cleaned_str = re.sub(pattern, r'\1 \2', cleaned_str)

    return cleaned_str


def run_qa_document_chain(input_document: str, query: str):

    question = (f"Antworte auf Deutsch und halte dich kurz. Beginne deine "
                f"Antwort nicht mit ja oder nein, sondern direkt mit einer "
                f"Begründung auf die folgende Frage: Wäre diese Person ein "
                f"geeigneter Partner für eine Kollaboration ausgehend von "
                f"dieser Frage: {query}. Bitte erläutere und verwende "
                f"wenn möglich Verweise auf den Text. Nenne "
                f"auch den Namen der Person in deinem Text.")

    return qa_document_chain.run(
        input_document=input_document,
        question=question
    )
