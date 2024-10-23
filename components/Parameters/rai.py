from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text


rai_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-rai-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
# Collisions
## Basic Collision Avoidance
rai_1 = html.Div(
                 children=[
                        dbc.Checklist(id="rai_1",
                                options=[
                                     {"label": "Avoid Collisions", "value": True},
                                 ],
                                 value=[True],
                                 switch=True)
                 ])
rai_2 = html.Div(
                 children=[
                     html.P("Set Collision Penalty", className="p_dark"),
                     dbc.Input(id="rai_2",
                               type="number",
                               min=0,
                               max=10,
                               step=1,
                               placeholder=10)
                 ])
## Advanced Collision Avoidance
rai_3 = html.Div(
                 children=[
                        dbc.Checklist(id="rai_3",
                                 options=[
                                     {"label": "Avoid Buffer Zones", "value": False},
                                 ],
                                 value=[True],
                                 switch=True)
                 ])
rai_4 = html.Div(
                 children=[
                    html.P("Set Buffer Entry Penalty", className="p_dark"),
                    dbc.Input(id="rai_4",
                              type="number",
                             min=0,
                             max=10,
                             step=1,
                             placeholder=10)
                 ])
# Damage
## Basic Damage Avoidance
rai_5 = html.Div(
                 children=[
                            dbc.Checklist(id="rai_5",
                                options=[
                                     {"label": "Avoid Damage", "value": True},
                                 ],
                                 value=[True],
                                 switch=True)
                 ])

params = dbc.Accordion(
        [
            dbc.AccordionItem(
                    title="Collisions",
                    children=[
                                html.H6("Basic Collision Avoidance", className="h6_dark"),
                                rai_1,
                                rai_2,
                                html.H6("Advanced Collision Avoidance", className="h6_dark"),
                                rai_3,
                                rai_4
                    ]
                ),
            dbc.AccordionItem(title="Damage",
                              children=[
                                html.H6("Basic Damage Avoidance", className="h6_dark"),
                                rai_5

                              ])
            ])



menu = html.Div(id="rai-menu",
                children=[
                    params,
                    rai_params_submit_button
                ])


@callback(
    [Output(component_id="rai_1", component_property="value"),
    Output(component_id="rai_2", component_property="value"),
    Output(component_id="rai_3", component_property="value"),
    Output(component_id="rai_4", component_property="value"),
    Output(component_id="rai_5", component_property="value")],
    Input(component_id="rai_parameters", component_property="data")
)
def populate_default_rai_params(inputs):
     rai1 = inputs["basic_collision_avoidance"]
     rai2 = inputs["basic_collision_penalty"]
     rai3 = inputs["advanced_collision_avoidance"]
     rai4 = inputs["advanced_collision_penalty"]
     rai5 = inputs["basic_damage_avoidance"]
     return rai1, rai2, rai3, rai4, rai5

@callback(
    Output(component_id="rai_parameters", component_property="data"),
    Input(component_id="tools-menu-submit-rai-button", component_property="n_clicks"),
    [State(component_id="rai_parameters", component_property="data"),
     State(component_id="rai_1", component_property="value"),
     State(component_id="rai_2", component_property="value"),
     State(component_id="rai_3", component_property="value"),
     State(component_id="rai_4", component_property="value"),
     State(component_id="rai_5", component_property="value")],
           allow_duplicate=True, prevent_initial_call=True
)
def update_rai_parameters(click, parameters, rai1, rai2, rai3, rai4, rai5):
    if click:
        parameters["basic_collision_avoidance"] = rai1
        parameters["basic_collision_penalty"] = rai2
        parameters["advanced_collision_avoidance"] = rai3
        parameters["advanced_collision_penalty"] = rai4
        parameters["basic_damage_avoidance"] = rai5

    return parameters
