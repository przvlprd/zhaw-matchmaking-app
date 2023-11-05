from fastapi import FastAPI
from pydantic import BaseModel, conint
from enum import Enum
from retrieve import get_relevant_results
from chain import get_context


class SearchOptions(str, Enum):
    sim = "sim"  # similarity search, default
    mmr = "mmr"  # maximum marginal relevance


class UserInputRequest(BaseModel):
    user_input: str
    search: SearchOptions = SearchOptions.sim
    k: conint(ge=1, lt=50) = 4  # number of documents returned by retriever


app = FastAPI()


@app.post("/query/")
def query(user_input_request: UserInputRequest):
    user_input = user_input_request.user_input
    search = user_input_request.search
    k = user_input_request.k

    results = get_relevant_results(user_input, search, k)

    message = "Folgende Mitarbeiter könnten interessant für dich sein:\n"

    for name, url in zip(results[0], results[1]):
        message += f"\n{name}\n{url}\n"
        context = get_context(name, url, user_input)
        message += context

    response_data = {'output': message}

    return response_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
