from dash import html, dash, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.dependencies import ALL
from utils import app_utils

rai_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-rai-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
# Collisions
## Basic Collision Avoidance
elements = app_utils.create_user_inputs("RAI")["elements"]
callback_list = [item for sublist in elements.values() for item in sublist]
element_values = app_utils.create_user_inputs("RAI")["values"]

params = dbc.Accordion(
        [dbc.AccordionItem( title=key,children=val) for key, val in elements.items()]
    )

menu = html.Div(id="rai-menu",
                children=[
                    params,
                    rai_params_submit_button
                ])

def adj_bool(item):
    if item == [1] or item == [0]:
        if item[0] == 1:
            return True
        else:
            return False
    else:
        return item

input_values = {key:Input(component_id=key, component_property="value") for key, val in element_values.items()}
@callback(
    Output(component_id="rai_parameters", component_property="data"),
    [Input(component_id="tools-menu-submit-rai-button", component_property="n_clicks")],
    [State({"type": "RAI", "index": ALL}, "value"),
    State({"type": "RAI", "index": ALL}, "id")],
           allow_duplicate=True, prevent_initial_call=True
)
def update_rai_parameters(click, values, ids):
    if click:
        param_keys = list(element_values.keys())
        print(param_keys)
        values = [adj_bool(val) for val in values]
        parameters = {key: (False if val == [] else val) for key, val in zip(param_keys, values)}
        print(parameters) # for debugging
        return parameters
    return dash.no_update
