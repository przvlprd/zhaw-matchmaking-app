#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import panel as pn
from retrieve import get_relevant_results
from chain import get_context

pn.extension()

# Define widgets to control parameters in the sidebar
num_relevant_chunks_slider = pn.widgets.IntSlider(
    name="Chunks retrieved from vectordb",
    start=1, end=15, step=1, value=4,
)
search_type_select = pn.widgets.RadioButtonGroup(
    name="Search type",
    options={"Similarity Search": "sim",
             "Maximum Marginal Relevance": "mmr"},
    description="Search type for vectordb"
)


def callback(user_input: str, user: str, instance: pn.chat.ChatInterface):
    """
    Callback function for handling user input in a Panel chat interface.

    Parameters:
    - user_input (str): The input provided by the user.
    - user (str): The username associated with the user.
    - instance (pn.chat.ChatInterface): The Panel chat interface instance.

    Returns:
    None

    This function retrieves relevant results based on the user's input,
    formats the results, and sends them as a message to the chat interface.
    Additionally, retrieves and sends contextual information for each result.
    """
    # Retrieve relevant results
    results = get_relevant_results(
        query=user_input,
        k=num_relevant_chunks_slider.value,
        search=search_type_select.value
    )

    # Format and send results as a message
    message = "Folgende Mitarbeiter könnten interessant für dich sein:\n"
    for name, url in zip(results[0], results[1]):
        message += f"<br><a href='{url}' target='_blank'>{name}</a><br>"
    send_message(message, instance)

    # Retrieve and send contextual information for each result
    for name, url in zip(results[0], results[1]):
        context = get_context(name, url, user_input)
        context += f"<br><a href='{url}' target='_blank'>Zum Profil</a><br>"
        send_message(context, instance)


def send_message(message: str, instance: pn.chat.ChatInterface):
    """
    Send a message to the chat interface.

    Parameters:
    - message (str): The message to be sent.
    - instance (pn.chat.ChatInterface): The Panel chat interface instance.

    Returns:
    None

    This function sends the specified message to the chat interface.
    The message is sent on behalf of the "MatchMaking Bot" user,
    and the response is set to not trigger a response from other users.
    """
    instance.send(
        value=message,
        user="MatchMaking Bot",
        respond=False
    )


# Initialize chat interface
chat_interface = pn.chat.ChatInterface(
    callback=callback, callback_user="MatchMaking Bot"
)

# Initial message
send_message("Wen suchst du? Beschreibe z.B. was du machst und in "
             "welchem Bereich du gern kollaborieren würdest.", chat_interface)

# Create the template
template = pn.template.BootstrapTemplate(
  title="ZHAW MatchMaking App",
  sidebar=[num_relevant_chunks_slider, search_type_select],
  main=[chat_interface]
)

# Serve the template
template.servable()
