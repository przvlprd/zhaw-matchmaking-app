#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from pydantic import BaseModel, conint

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from chain import get_context
from retrieve import get_relevant_results


class SearchOptions(str, Enum):
    """
    Enumeration for specifying search options.

    Options:
    - `sim`: Similarity search (default).
    - `mmr`: Maximum marginal relevance.
    """
    sim = "sim"
    mmr = "mmr"


class UserInputRequest(BaseModel):
    """
    Model for representing user input request.

    Attributes:
    - `user_query` (str): The input / search query provided by the user.
    - `search_type` (SearchOptions): The search option,
                                     default is `SearchOptions.sim`.
    - `num_chunks` (int): The number of chunks returned by the retriever
                          (between 1 and 50), default is 3.
    - `full_context`(bool): Switch between full profile retrieved as context
                            (slow, higher accuracy) or shorter version without
                            a person's publications (faster, less accurate),
                            default is false.
    """
    user_query: str
    search_type: SearchOptions = SearchOptions.sim
    num_chunks: conint(ge=1, lt=51) = 3
    full_context: bool = False


app = FastAPI()


@app.get("/")
def read_root():
    """
    Get information about the root endpoint.

    Returns:
        dict: JSON - Response with information about the API
              documentation at /docs and the link to the GitHub repository.
    """
    return {
        "See /docs or /redoc for the API documentation or visit the Github "
        "repository for request templates: "
        "https://github.com/przvlprd/zhaw-matchmaking-app#request-templates"
    }


@app.post("/query/")
def query(user_input_request: UserInputRequest):
    """
    Endpoint for handling user queries.

    Parameters:
    - user_input_request (UserInputRequest): Request object containing user
                                             input details.

    Returns:
    dict: JSON - Response containing the formatted message.
    """
    user_query = user_input_request.user_query
    search_type = user_input_request.search_type
    num_chunks = user_input_request.num_chunks
    full_context = user_input_request.full_context

    results = get_relevant_results(user_query, search_type, num_chunks)
    message = "Folgende Mitarbeiter könnten interessant für dich sein:"

    for name, url in zip(results[0], results[1]):
        message += f"\n\n{name}\n{url}\n\n"
        context = get_context(name, url, user_query, full_context)
        message += context

    return {'output': message}


@app.post("/query-stream/")
async def query_stream(user_input_request: UserInputRequest):
    """
    Endpoint for handling user queries with streaming response.

    Parameters:
    - user_input_request (UserInputRequest): Request object containing user
                                             input details.

    Returns:
    StreamingResponse: Streaming response containing the formatted message.
    """
    user_query = user_input_request.user_query
    search_type = user_input_request.search_type
    num_chunks = user_input_request.num_chunks
    full_context = user_input_request.full_context

    results = get_relevant_results(user_query, search_type, num_chunks)

    def generate_response():
        yield "Folgende Mitarbeiter könnten interessant für dich sein:"

        for name, url in zip(results[0], results[1]):
            new_message = f"\n\n{name}\n{url}\n\n"
            context = get_context(name, url, user_query, full_context)
            new_message += context
            yield new_message

    return StreamingResponse(content=generate_response())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
