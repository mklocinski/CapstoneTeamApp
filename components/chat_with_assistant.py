from dash import html, callback, Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from utils import text
from openai import OpenAI, api_key
import time
import pickle
import os


# ------------------------------------------------------------------ #
# --------------------- Assistant Interaction ---------------------- #
# ------------------------------------------------------------------ #
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

class Assistant:
    def __init__(self, apikey, assistant_id, message_history):
        self.apikey = apikey
        self.assistant_id = assistant_id
        self.client = None
        self.thread_id = None

    def initialize_client(self):
        self.client = OpenAI(api_key=self.apikey)

    def generate_response(self, prompt):
        # If thread_id is None, create a new thread, otherwise add a message to the existing thread
        if self.thread_id is None:
            # Create a new chat thread with the user prompt
            chat = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,  # Use the user input from the UI here
                    }
                ]
            )
            self.thread_id = chat.id  # Save the thread_id for future prompts
            print(f" --> New thread created: {self.thread_id}")
        else:
            # Add the new prompt to the existing thread
            chat = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=prompt
            )
            print(f" --> Added message to existing thread: {self.thread_id}")

        # Run the assistant thread
        run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id)
        print(f" --> Run Created: {run.id}")

        # Wait for the assistant to complete the response
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)
            print(f" --> Run Status: {run.status}")
            time.sleep(0.5)

        print(f" --> Run Completed!")

        # Retrieve the assistant's response
        message_response = self.client.beta.threads.messages.list(thread_id=self.thread_id)
        messages = message_response.data

        # Find the assistant's response (the last message from the assistant)
        for message in messages:
            if message.role == 'assistant':  # Access the message.role using dot notation
                # Extract and return the actual response text
                # Handle list of content blocks
                response_text = ""
                for content_block in message.content:  # Iterate through the content blocks
                    if hasattr(content_block, 'text'):  # Check if it has a 'text' attribute
                        response_text += content_block.text.value + "\n"  # Append the text value

                return response_text.strip()  # Return the assistant's response content
            else:
                # If no assistant message is found, return an error message
                return "No response from assistant."



def chat_bubble(participant, message):
    if message:
        if participant == 'user':
            bubble = dbc.Card(className="chat-bubble-user",
                              children=[dbc.CardBody(
                                    [
                                        html.P(className="p_dark",
                                            children=[message]
                                        ),
                                    ]
                                )]
                              )
        elif participant == 'assistant':
            bubble = dbc.Card(className="chat-bubble-assistant",
                              children=[dbc.CardBody(
                                  [
                                      html.P(children=[message]
                                             ),
                                  ]
                              )]
                              )
        return bubble



dialog_area = html.Div(id="chat-dialog",
                       className="chat-assistant-dialog",
                       children=[

                       ])
user_query_box= dbc.Textarea(id="chat-user-query-box",
                       placeholder="Ask your assistant a question",
                        size="sm",
                       draggable=False,
                       className="chat-user-query-box")
about_your_assistant = html.Div(id="chat-about-assistant",
                                className="chat-assistant-description",
                                children=[html.P(text.chat_about_assistant)])
about_your_assistant_text = dbc.Popover(
            dbc.PopoverBody(text.chat_about_assistant_description),
            target="chat-about-assistant",
            trigger="click",
        )
submit_user_query = dbc.Button(
                        children=[html.I( className='bi bi-send')],
                        className="query-button",
                        id="chat-user-query-button",
                        n_clicks=0)


layout = html.Div(
        id='chat-area',
        className='assistant-chat-area',
        children=[
                dialog_area,
                html.Div(className="chat-user-query-area",
                        children=[
                            user_query_box,
                            submit_user_query
                            ]),
                html.Div(
                         children=[
                            about_your_assistant,
                            about_your_assistant_text
                         ])
                ]
            )




@callback([
            Output(component_id="chat-dialog", component_property="children"),
            Output(component_id="chat-messages", component_property="data"),
            Output(component_id="chat-user-query-box", component_property="value")
           ],
    Input( component_id="chat-user-query-button", component_property="n_clicks"),
    [State(component_id="chat-user-query-box", component_property="value"),
    State(component_id="chat-messages", component_property="data"),
     State(component_id="chat-dialog", component_property="children")]
        )
def ask_assistant(click, query, messages, dialog_area):
    if dialog_area is None:
        dialog_area = []
    if click == 0:
        return dialog_area, messages, query
    else:
        assistant = Assistant(openai_api_key, assistant_id, messages)
        assistant.initialize_client()
        if messages is None:
            messages = {"messages":[{"role": "system", "content": "hello"}]}
        messages["messages"].append({"role": "user", "content": query})
        assistant_response = assistant.generate_response(query)
        print("just messaged assistant")
        messages["messages"].append({"role": "assistant", "content": assistant_response})
        dialog_area.insert(0, chat_bubble("user", query))
        dialog_area.insert(0, chat_bubble("assistant", assistant_response))
        return dialog_area, messages, ""



