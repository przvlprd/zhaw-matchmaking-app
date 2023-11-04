import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.question_answering import load_qa_chain
from ingest.preprocess_profile_data import preprocess_profile


llm = OpenAI(temperature=0)
qa_chain = load_qa_chain(llm, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)


def get_context(name: str, url: str, query: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile = soup.find('div', class_='zhaw-person')
    raw_profile = profile.get_text()
    cleaned_profile = preprocess_profile(raw_profile)

    return run_qa_document_chain(name, cleaned_profile, query)


def run_qa_document_chain(name: str, input_document: str, query: str):

    question = (f"Antworte auf Deutsch und halte dich kurz. Beginne deine "
                f"Antwort nicht mit ja oder nein, sondern direkt mit einer "
                f"Begründung auf die folgende Frage: Wäre diese Person ein "
                f"geeigneter Partner für eine Kollaboration ausgehend von "
                f"dieser Frage: {query}. Bitte erläutere und verwende "
                f"wenn möglich Verweise auf den Text. Nenne "
                f"auch den Namen der Person in deinem Text.")

    # versuche eine verbindung zu finden, wo die person helfen könnte
    # API implementieren / statt Panel

    # verwende Namen aus Variable

    # websocket / stream - statt request
    # bis alle nachrichten fertig gesendet wurden
    # Datenaustausch zwischen Modell und Frontend

    return qa_document_chain.run(
        input_document=input_document,
        question=question
    )
