from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text


chat_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-chat-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
# Collisions
## Basic Collision Avoidance
chat_1 = html.Div(
                 children=[
                    html.P("Set Response Temperature", className="p_dark"),
                     dcc.Slider(id='chat_1',
                                value=0.5,
                                min=0,
                                max=1,
                                step=0.1
                                )
                 ])

params = dbc.Accordion(
        [
            dbc.AccordionItem(
                    title="Standard Parameters",
                    children=[
                                chat_1
                    ]
                )
            ]
)



menu = html.Div(id="chat-menu",
                children=[
                    params,
                    chat_params_submit_button
                ])


@callback(
    Output(component_id="chat_1", component_property="value"),
    Input(component_id="chat_parameters", component_property="data")
)
def populate_default_chat_params(inputs):
     chat1 = inputs["temperature"]

     return chat1

@callback(
    Output(component_id="chat_parameters", component_property="data"),
    Input(component_id="tools-menu-submit-chat-button", component_property="n_clicks"),
    [State(component_id="chat_parameters", component_property="data"),
     State(component_id="chat_1", component_property="value")]
)
def update_chat_parameters(click, parameters, chat1):
    if click:
        parameters["temperature"] = chat1

    return parameters
