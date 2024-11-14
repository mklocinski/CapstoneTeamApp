from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text
from openai import OpenAI
import time
import os
import requests
import pandas as pd
import base64
import io
from PIL import Image

# ------------------------------------------------------------------ #
# --------------------- Assistant Interaction ---------------------- #
# ------------------------------------------------------------------ #
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

class Assistant:
    def __init__(self, apikey, assistant_id, message_history, file_truncation=10):
        self.apikey = apikey
        self.assistant_id = assistant_id
        self.client = None
        self.thread_id = None
        self.file_id = None # --> from global file_id
        self.file_list = [] # --> from global file_list
        self.file_truncation = file_truncation # --> from row_counts
        self.image_list = []
        self.image_path_list = []

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

        # Add file as a new message if there's an updated file.
        if self.file_id:
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content="Please refer to this updated file.",
                attachments=[{"file_id": self.file_id, "tools": [{"type": "code_interpreter"}]}]
            )
            print(f"File with ID {self.file_id} attached to the thread.")

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
                image_ids = []
                for content_block in message.content:  # Iterate through the content blocks
                    if hasattr(content_block, 'text'):  # Check if it has a 'text' attribute
                        response_text += content_block.text.value + "\n"  # Append the text value
                    if hasattr(content_block, 'image_file'): # Changed for consistency
                        image_file_id = getattr(content_block.image_file, "file_id", None)
                        self.image_list.append(image_file_id)
                self.file_id = None
                self.save_and_return_images()
                return {'text': response_text.strip(),
                        'image': self.image_path_list}  # Return the assistant's response content
            else:
                self.file_id = None
                # If no assistant message is found, return an error message
                return {'text':"No response from assistant.", 'image': []}

    def save_and_return_images(self):  # Adjusted from "show" to "return", as chat_bubble() handles display
        directory_path = "assets/images/openai_images"
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        for image_file_id in self.image_list:
            image_file = self.client.files.content(image_file_id)
            image = Image.open(image_file)
            image_path = os.path.join(directory_path, f"{image_file_id}.png")
            image.save(image_path)
            self.image_path_list.append(image_path)
            return self.image_path_list

    def update_file(self, input_df):
        # global file_id --> both global vars are now class attributes
        # global file_list  # Use the global file_list variable to track the files created
        #
        # # Generate the truncated CSV file
        # input_file = 'tbl_local_state.csv' --> now an input parameter

        if not isinstance(input_df, pd.DataFrame):
            raise ValueError("The input must be a DataFrame.")
        output_file = 'updated_file.csv'
        truncated_df = input_df.head(self.file_truncation) # --> parse_csv(input_file, output_file, row_count)
        truncated_df.to_csv(output_file, index=False)

        # Upload the new truncated file to OpenAI and store the new file ID
        new_file = self.client.files.create(file=open(output_file, "rb"), purpose="assistants")
        self.file_id = new_file.id  # Update the global file ID
        self.file_list.append(self.file_id)  # Add the newly created file to the file list
        os.remove(output_file)
        print(f"Updated file uploaded with file ID: {self.file_id}")

    def purge_files(self):
        # Cleans up OpenAI Storage by deleting updated CSVs
        for file in self.file_list:
            self.client.files.delete(file)

    def purge_image_paths(self):
        # The images from the current session remain saved to the app, but the assistant instance's
        # self.image_path_list is purged to prevent redundant image returns
        self.image_path_list = []

    def purge_session_images(self):
        # Removes all images saved to the app at close of user session
        if len(self.image_path_list) > 0:
            for i_path in self.image_path_list:
                if os.path.isfile(i_path):
                    os.remove(i_path)
                    print(f"Removed file: {i_path}")
                else:
                    print(f"Skipped non-file: {i_path}")






def chat_bubble(participant, message):
    bubble = None
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
                                        html.P(children=[message['text']]),
                                         # html.A(
                                              html.Img(src=message['image'], style={'cursor': 'pointer'})
                                        #      href=message['image'],
                                        #      target="_blank"
                                        #  )

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



file_upload = html.Div(
    id='upload-attachment',
    className="chat-upload-attachment",
    children=[dcc.Upload(
        id='attachment',
        children=html.Div([
            html.I( className='bi bi-paperclip'),
        ]),
        accept=".csv")]
)
submit_user_query = dbc.DropdownMenu(
    id="chat-user-query-button",
    className="m-2",
    label=html.I( className='bi bi-send'),
    children=[
        html.P("Attach most recent run data:"),
        dcc.Checklist(
            id="chat-option-attachments",
            className="attachment-drop-down",
            labelClassName="attachment-drop-down-text",
            options=[
                {'label': 'Local State Data', 'value': 'tbl_local_state'},
                {'label': 'Global State Data', 'value': 'tbl_global_state'},
                {'label': 'Reward Data', 'value': 'tbl_rewards'},
                {'label': 'Drone Action Data', 'value': 'tbl_drone_actions'},
                {'label': 'Model Run Parameters', 'value': 'tbl_model_run_params'},
                {'label': 'Model Runs', 'value': 'tbl_model_runs'}
            ],
            value=[],
            labelStyle={'font-size':'0.75em'}
        ),
    dbc.Button('Submit', id='chat-submit-button', n_clicks=0,
                               color="secondary", className="me-1",
                size="sm", style={"margin-left":"50%"})
    ],
    align_end=False,
)

layout = html.Div(
        id='chat-area',
        className='assistant-chat-area',
        children=[
                dialog_area,
                html.Div(className="chat-user-query-area",
                        children=[
                            user_query_box,
                            file_upload,
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
            # Updates chat area (i.e. bubbles) in the app with new chat bubbles
            # for the user query and assistant resposne
            Output(component_id="chat-dialog", component_property="children"),
            # Updates in-app chat message store with user query and assistant response
            Output(component_id="chat-messages", component_property="data"),
            # Clears query box
            Output(component_id="chat-user-query-box", component_property="value")
           ],
    # Direct input/trigger: "Submit" button click
    Input( component_id="chat-submit-button", component_property="n_clicks"),
    # Indirect input: user query that was entered into query box
    [State(component_id="chat-user-query-box", component_property="value"),
     # Indirect input: attachments selected in attachment options dropdown
     State(component_id="chat-option-attachments", component_property="value"),
     # Indirect input: user-uploaded attachments
    State(component_id="attachment", component_property="contents"),
     # Indirect input: in-app chat message store (old queries/responses for session)
    State(component_id="chat-messages", component_property="data"),
     # Indirect input: chat area (i.e. bubbles)
     State(component_id="chat-dialog", component_property="children"),
     # Indirect input: environment's API url
     State('api_url', 'data')]
        )
def ask_assistant(click, query, opt_attachments, user_attachments, messages, chat_dialog, api_url):
    # Check if there is an existing conversation *in the app*
    if chat_dialog is None:
        chat_dialog = []
    # Check if the user has clicked "Submit"
    if click == 0:
        # If not, return an empty dialog area, existing messages thread, and query box contents
        return chat_dialog, messages, query
    else:
        print("button clicked") # for debugging
        # Initialize Assistant (see class definition above) ------------------------------------
        assistant = Assistant(openai_api_key, assistant_id, messages)
        assistant.initialize_client()
        # If there are no messages in in-app message memory, create initial dictionary
        if messages is None:
            messages = {"messages":[{"role": "system", "content": "hello"}]}
        # If there are messages, append query
        messages["messages"].append({"role": "user", "content": query})
        # Check for user-added attachments (paperclip)------------------------------------------
        ## Initialize empty list to store multiple attachments
        user_attachs = []
        ## If user attachments exists:
        if user_attachments is not None:
            ### Read in file and add formatted dfs to user_attachs
            type, string = user_attachments.split(',')
            decodes = base64.b64decode(string)
            ### Currently working on simple 1-file upload, so df is not appended but replaces contents
            user_attachs = [pd.read_csv(io.StringIO(decodes.decode('utf-8')))]
        print(user_attachs)  # for debugging
        for attach in user_attachs:
            assistant.update_file(attach)
        # Check for optional attachments (checkbox) ----------------------------------------------
        ## Make API call to get most recent data for the selected table/data group
        api_call = api_url['api_url']
        print(opt_attachments)
        attachment_calls = [f'{api_call}/database/last_run/{attach}' for attach in opt_attachments]
        ## Initialize empty list to store attachments
        opt_attachs = []
        for call in attachment_calls:
            response = requests.get(call)
            ## Check if call was successful
            if response.status_code == 200:
                print("Data successfully fetched from API")
                ### Read in file and append formatted dfs to opt_attachs
                data = response.json()
                df = pd.DataFrame(data)
                new_cols = [col[5:] for col in df.columns]
                df.columns = new_cols
                opt_attachs.append(df)
            print(opt_attachs)  # for debugging
            for attach in opt_attachs:
                assistant.update_file(attach)
        # Submit and receive assistant response
        assistant_response = assistant.generate_response(query)
        # [Add in error handling]
        print("just messaged assistant")  # for debugging
        # Append response to in-app message store
        messages["messages"].append({"role": "assistant", "content": assistant_response})
        # Create and add user query bubble (white,right-hand side bubble) to dialog area
        chat_dialog.insert(0, chat_bubble("user", query))
        # Create and add assistant response bubble (blue, left-hand side bubble) to dialog area
        chat_dialog.insert(0, chat_bubble("assistant", assistant_response))
        # Purge assistant instance's image_list; images are still saved to assets\images\openai_images
        assistant.purge_image_paths()
        # Return dialog area updated with chat bubbles; in-app message store updated with
        # recent query and response; and an empty string to the query box (to clear out last query)
        return chat_dialog, messages, ""

#Purges previous Assistant session as well as any in-app files saved during the previous session
@callback(
    # Output: N/a; A dummy html div is supplied since each callback needs some sort of output
    Output("page-load-trigger-output", "children"),
    Input("page-load-trigger", "data")
)
def on_page_load(data):
    if not data["is_loaded"]:
        # Modify the data to mark it as loaded
        data["is_loaded"] = True
        assistant = Assistant(openai_api_key, assistant_id, None)
        assistant.initialize_client()
        #assistant.purge_files()
        assistant.purge_session_images()
        return "Page loaded or refreshed!"
    return "Page already loaded!"
