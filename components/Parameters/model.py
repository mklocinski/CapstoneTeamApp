from dash import html, dash, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.dependencies import ALL
from utils import app_utils

model_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-model-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
elements = app_utils.create_user_inputs("DRL")["elements"]
callback_list = [item for sublist in elements.values() for item in sublist]
element_values = app_utils.create_user_inputs("DRL")["values"]

params = dbc.Accordion(
        [dbc.AccordionItem( title=key,children=val) for key, val in elements.items()]
    )

menu = html.Div(id="model-menu",
                children=[
                    params,
                    model_params_submit_button
                ])


@callback(
    Output(component_id="model_parameters", component_property="data"),
    [Input(component_id="tools-menu-submit-model-button", component_property="n_clicks")],
    [State({"type": "DRL", "index": ALL}, "value"),
    State({"type": "DRL", "index": ALL}, "id")],
           allow_duplicate=True, prevent_initial_call=True
)
def update_model_parameters(click, values, ids):
    if click:
        param_keys = list(element_values.keys())
        print(values)
        print(ids)
        values = [val for val in values]
        parameters = {key: (False if val == [] else val) for key, val in zip(param_keys, values)}
        print(parameters) # for debugging
        return parameters
    return dash.no_update
