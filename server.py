from enum import Enum
from pydantic import BaseModel, conint

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from chain import get_context
from retrieve import get_relevant_results


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
        message += context[1:] + "\n"

    return {'output': message}


@app.post("/query-stream/")
async def query_stream(user_input_request: UserInputRequest):
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
