import panel as pn
from retrieve import get_relevant_results
from chain import get_context
pn.extension()


k_slider = pn.widgets.IntSlider(
    name="Number of Relevant Chunks", start=1, end=15, step=1, value=4
)
search_select = pn.widgets.RadioButtonGroup(
    name="Search type", options=["sim", "mmr"],
    description="Search type for vectordb"
)


def callback(user_input: str, user: str, instance: pn.chat.ChatInterface):
    results = get_relevant_results(
        query=user_input,
        k=k_slider.value,
        search=search_select.value
    )

    message = "Folgende Mitarbeiter könnten interessant für dich sein:\n"

    for name, url in zip(results[0], results[1]):
        message += f"\n{name}\n{url}\n"
    send_message(message)

    for name, url in zip(results[0], results[1]):
        context = get_context(name, url, user_input)
        send_message(context)


def send_message(message: str):
    chat_interface.send(
        value=message,
        user="MatchMaking Bot",
        respond=False
    )


chat_interface = pn.chat.ChatInterface(
    callback=callback, callback_user="MatchMaking Bot"
)

chat_interface.send(
    value="Wen suchst du?",
    user="MatchMaking Bot",
    respond=False
)

template = pn.template.BootstrapTemplate(
  title="ZHAW MatchMaking App",
  sidebar=[k_slider, search_select],
  main=[chat_interface]
)
template.servable()
