from dash import html, dash, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.dependencies import ALL
from utils import app_utils


map_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-map-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
# Maps
## Number of obstacles
elements = app_utils.create_user_inputs("Map")["elements"]
callback_list = [item for sublist in elements.values() for item in sublist]
element_values = app_utils.create_user_inputs("Map")["values"]

params = dbc.Accordion(
        [dbc.AccordionItem( title=key,children=val) for key, val in elements.items()]
    )

menu = html.Div(id="map-menu",
                children=[
                    params,
                    map_params_submit_button
                ])


#inputs = [Input(component_id=key, component_property="value") for key, val in values.items()]
input_values = {key:Input(component_id=key, component_property="value") for key, val in element_values.items()}


@callback(
    Output("map_parameters", "data"),
    Input("tools-menu-submit-map-button", "n_clicks"),
    State({"type": "Map", "index": ALL, "category": ALL}, "value"),
    State({"type": "Map", "index": ALL, "category": ALL}, "id"),
    prevent_initial_call=True
)
def update_map_parameters(click, values, ids):
    if click:
        # Create a dictionary mapping parameter codes to their user-input values
        parameters = {}
        for id, value in zip(ids, values):
            category = id.get("category")
            index = id["index"]
            if category not in parameters:
                parameters[category] = {}
            parameters[category][index] = value
        print(parameters) # For debugging
        modified_parameters = app_utils.map_param_conversion(parameters)
        print(modified_parameters)
        return modified_parameters  # This will return the parameters dictionary to "map_parameters" data
    return dash.no_update

