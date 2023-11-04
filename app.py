import panel as pn
from retrieve import get_relevant_results
from chain import get_context


def callback(user_input: str, user: str, instance: pn.chat.ChatInterface):
    results = get_relevant_results(user_input)

    message = "Folgende Mitarbeiter könnten interessant für dich sein:\n"

    for name, url in zip(results[0], results[1]):
        message += f"\n{name}\n{url}\n"
    send_message(message)

    for name, url in zip(results[0], results[1]):
        context = get_context(name, url, user_input)
        send_message(context)

    # ToDo: update method to send messages (asynchronous?)
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
