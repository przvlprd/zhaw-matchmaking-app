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
    - `user_input` (str): The input provided by the user.
    - `search` (SearchOptions): The search option,
                                default is `SearchOptions.sim`.
    - `k` (int): The number of documents returned by the retriever
                 (between 1 and 49), default is 4.
    """
    user_input: str
    search: SearchOptions = SearchOptions.sim
    k: conint(ge=1, lt=50) = 4


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
        "See /docs for more information or visit the Github repository for "
        "request templates: "
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
    user_input = user_input_request.user_input
    search = user_input_request.search
    k = user_input_request.k

    results = get_relevant_results(user_input, search, k)
    message = "Folgende Mitarbeiter könnten interessant für dich sein:\n"

    for name, url in zip(results[0], results[1]):
        message += f"\n{name}\n{url}\n"
        context = get_context(name, url, user_input)
        message += context[1:] + "\n"

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
    user_input = user_input_request.user_input
    search = user_input_request.search
    k = user_input_request.k

    results = get_relevant_results(user_input, search, k)

    def generate_response():
        yield "Folgende Mitarbeiter könnten interessant für dich sein:\n"

        for name, url in zip(results[0], results[1]):
            new_message = f"\n{name}\n{url}\n"
            context = get_context(name, url, user_input)
            new_message += context[1:] + "\n"
            yield new_message

    return StreamingResponse(content=generate_response())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
