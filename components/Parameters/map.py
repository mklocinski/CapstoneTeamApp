from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text


map_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-map-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
# Collisions
## Basic Collision Avoidance
map_1 = html.Div(
                 children=[
                     html.P("Set number of generic obstacles_1", className="p_dark"),
                     dbc.Input(id="map_1",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])
map_2 = html.Div(
                 children=[
                     html.P("Set number of generic obstacles2:", className="p_dark"),
                     dbc.Input(id="map_2",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])
map_3 = html.Div(
                 children=[
                     html.P("Set number of no-fly zones:", className="p_dark"),
                     dbc.Input(id="map_3",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])
map_4 = html.Div(
                 children=[
                     html.P("Set number of humans:", className="p_dark"),
                     dbc.Input(id="map_4",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])
map_5 = html.Div(
                 children=[
                     html.P("Set number of buildings:", className="p_dark"),
                     dbc.Input(id="map_5",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])

map_6 = html.Div(
                 children=[
                     html.P("Set number of trees:", className="p_dark"),
                     dbc.Input(id="map_6",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])

map_7 = html.Div(
                 children=[
                     html.P("Set number of animals:", className="p_dark"),
                     dbc.Input(id="map_7",
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               placeholder=10)
                 ])

params = dbc.Accordion(
        [
            dbc.AccordionItem(
                    title="Phase 1",
                    children=[

                                map_1,
                                map_2,
                                map_3,
                                map_4,
                                map_5,
                                map_6,
                                map_7
                    ]
                ),
            dbc.AccordionItem(title="Phase 2",
                              children=[
                              ])
            ])



menu = html.Div(id="map-menu",
                children=[
                    params,
                    map_params_submit_button
                ])

#
# @callback(
#     [Output(component_id="map_1", component_property="value"),
#     Output(component_id="map_2", component_property="value"),
#     Output(component_id="map_3", component_property="value"),
#     Output(component_id="map_4", component_property="value"),
#     Output(component_id="map_5", component_property="value")],
#     Input(component_id="map_parameters", component_property="data")
# )
# def populate_default_map_params(inputs):
#      map1 = inputs["basic_collision_avoidance"]
#      map2 = inputs["basic_collision_penalty"]
#      map3 = inputs["advanced_collision_avoidance"]
#      map4 = inputs["advanced_collision_penalty"]
#      map5 = inputs["basic_damage_avoidance"]
#      return map1, map2, map3, map4, map5
#
# @callback(
#     Output(component_id="map_parameters", component_property="data"),
#     Input(component_id="tools-menu-submit-map-button", component_property="n_clicks"),
#     [State(component_id="map_parameters", component_property="data"),
#      State(component_id="map_1", component_property="value"),
#      State(component_id="map_2", component_property="value"),
#      State(component_id="map_3", component_property="value"),
#      State(component_id="map_4", component_property="value"),
#      State(component_id="map_5", component_property="value")],
#            allow_duplicate=True, prevent_initial_call=True
# )
# def update_map_parameters(click, parameters, map1, map2, map3, map4, map5):
#     if click:
#         parameters["basic_collision_avoidance"] = map1
#         parameters["basic_collision_penalty"] = map2
#         parameters["advanced_collision_avoidance"] = map3
#         parameters["advanced_collision_penalty"] = map4
#         parameters["basic_damage_avoidance"] = map5
#
#     return parameters
