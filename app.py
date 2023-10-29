import panel as pn
from retrieve import get_relevant_sources
from context_chain import get_context


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    sources = get_relevant_sources(contents)
    urls = []

    message = "Folgende Mitarbeiter könnten interessant für dich sein:"
    for source in sources:
        url = f"https://www.zhaw.ch/de/ueber-uns/person/{source}"
        urls.append(url)
        message += f"\n{url}"
    send_message(message)

    for url in urls:
        context = get_context(url, contents)
        send_message(context)

    # return message


chat_interface = pn.chat.ChatInterface(
    callback=callback, callback_user="MatchMaking Bot"
)

chat_interface.send(
    value="Wen suchst du?",
    user="MatchMaking Bot",
    respond=False
)

chat_interface.servable()


def send_message(message: str):
    chat_interface.send(
        value=message,
        user="MatchMaking Bot",
        respond=False
    )
