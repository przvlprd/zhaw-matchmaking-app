from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.question_answering import load_qa_chain
from ingest.preprocess_profile_data import preprocess_profile

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
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

    question = f"Answer in German. Find a connection to why this person was \
                 found as a fitting match to the user query. Start your \
                 response with the person's name. If you are not sure, find \
                 something about the person the user could be interested in. \
                 Query: {query} \
                 Helpful Answer: {name}"

    return qa_document_chain.run(
        input_document=input_document,
        question=question
    )
