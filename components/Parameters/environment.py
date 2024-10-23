from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text


environment_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-environment-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)
environment_1 = html.Div(
                 children=[
                    html.P("Set Environment", className="p_dark"),
                        dcc.Dropdown(id="environment_1",
                                 options=[
                                     "Rendezvous",
                                     "Pursuit-Evasion"
                                 ],
                                 value="Rendezvous")
                 ])
environment_2 = html.Div(
                 children=[
                     html.P("Select environment Size", className="p_dark"),
                     dbc.Input(id="environment_2",
                               type="number",
                               min=0,
                               max=50,
                               step=1,
                               placeholder=20)
                 ])


environment_3 = html.Div(
                 children=[
                        html.P("Set Observation Mode", className="p_dark"),
                        dcc.Dropdown(id="environment_3",
                                options=[
                                    {'label':'2d_rbf_acc', 'value':'2d_rbf_acc'},
                                    {'label':'3d_rbf', 'value':'3d_rbf'},
                                    {'label':'2d_rbf_acc_limited', 'value':'2d_rbf_acc_limited'},
                                    {'label':'2d_rbf_limited', 'value':'2d_rbf_limited'},
                                    {'label':'sum_obs_acc', 'value':'sum_obs_acc'},
                                    {'label':'sum_obs_acc_full', 'value':'sum_obs_acc_full'},
                                    {'label':'sum_obs_acc_no_vel', 'value':'sum_obs_acc_no_vel'},
                                    {'label':'sum_obs_acc_limited', 'value':'sum_obs_acc_limited'},
                                    {'label':'sum_obs', 'value':'sum_obs'},
                                    {'label':'sum_obs_limited', 'value':'sum_obs_limited'},
                                    {'label':'fix_acc', 'value':'fix_acc'}
                                 ],
                                 value='sum_obs_acc')
                 ])

environment_4 = html.Div(
                 children=[
                     html.P("Set Communication Radius", className="p_dark"),
                     dbc.Input(id="environment_4",
                               type="number",
                               min=0,
                               max=10,
                               step=1,
                               placeholder=2)
                 ])

environment_5 = html.Div(
                 children=[
                     html.P("Set World Size", className="p_dark"),
                     dbc.Input(id="environment_5",
                               type="number",
                               min=50,
                               max=200,
                               step=1,
                               placeholder=100)
                 ])
environment_6 = html.Div(
                 children=[
                     html.P("Set Distance Bins", className="p_dark"),
                     dbc.Input(id="environment_6",
                               type="number",
                               min=4,
                               max=16,
                               step=1,
                               placeholder=8)
                 ])

environment_7 = html.Div(
                 children=[
                     html.P("Set Bearing Bins", className="p_dark"),
                     dbc.Input(id="environment_7",
                               type="number",
                               min=4,
                               max=16,
                               step=1,
                               placeholder=8)
                 ])

environment_8 = html.Div(
                 children=[
                        dbc.Checklist(id="environment_8",
                                options=[
                                     {"label": "Torus", "value": False},
                                 ],
                                 value=[False],
                                 switch=True)
                 ])

environment_9 = html.Div(
                 children=[
                    html.P("Set Environment Dynamics", className="p_dark"),
                        dcc.Dropdown(id="environment_9",
                                 options=[
                                     {
                                         'label': 'Unicycle (can move forward or backward, can change orientation)',
                                         'value': 'unicycle'},
                                     {
                                         'label': 'Unicyle with acceleration',
                                         'value': 'unicycle_acc'},
                                     {
                                         'label': 'Point (simple movement)',
                                         'value': 'point'},
                                     {'label': 'Box-2D (realistic physics)',
                                      'value': 'box2d'}
                                 ],
                                 value="unicycle_acc")
                 ])

params = dbc.Accordion(
        [
            dbc.AccordionItem(
                    title="Standard Parameters",
                    children=[
                                environment_1,
                                environment_2,
                                environment_3,
                                environment_4,
                                environment_5,
                                environment_6,
                                environment_7,
                                environment_8,
                                environment_9
                    ]
                )
            ])



menu = html.Div(id="environment-menu",
                children=[
                    params,
                    environment_params_submit_button
                ])


@callback(
    [Output(component_id="environment_1", component_property="value"),
    Output(component_id="environment_2", component_property="value"),
    Output(component_id="environment_3", component_property="value"),
    Output(component_id="environment_4", component_property="value"),
    Output(component_id="environment_5", component_property="value"),
     Output(component_id="environment_6", component_property="value"),
     Output(component_id="environment_7", component_property="value"),
     Output(component_id="environment_8", component_property="value"),
     Output(component_id="environment_9", component_property="value"),],
    Input(component_id="environment_parameters", component_property="data")
)
def populate_default_environment_params(inputs):
     environment1 = inputs["environment_id"]
     environment2 = inputs["nr_agents"]
     environment3 = inputs["obs_mode"]
     environment4 = inputs["comm_radius"]
     environment5 = inputs["world_size"]
     environment6 = inputs["distance_bins"]
     environment7 = inputs["bearing_bins"]
     environment8 = inputs["torus"]
     environment9 = inputs["dynamics"]
     return environment1, environment2, environment3, environment4, environment5, environment6, environment7, environment8, environment9

@callback(
    Output(component_id="environment_parameters", component_property="data"),
    Input(component_id="tools-menu-submit-environment-button", component_property="n_clicks"),
    [State(component_id="environment_parameters", component_property="data"),
     State(component_id="environment_1", component_property="value"),
     State(component_id="environment_2", component_property="value"),
     State(component_id="environment_3", component_property="value"),
     State(component_id="environment_4", component_property="value"),
     State(component_id="environment_5", component_property="value"),
     State(component_id="environment_6", component_property="value"),
     State(component_id="environment_7", component_property="value"),
     State(component_id="environment_8", component_property="value"),
     State(component_id="environment_9", component_property="value")],
    allow_duplicate=True, prevent_initial_call=True
)
def update_environment_parameters(click, parameters, environment1, environment2, environment3, environment4, environment5,
                            environment6, environment7, environment8, environment9):
    if click:
        parameters["environment_id"] = environment1
        parameters["nr_agents"] = environment2
        parameters["obs_mode"] = environment3
        parameters["comm_radius"] = environment4
        parameters["world_size"] = environment5
        parameters["distance_bins"] = environment6
        parameters["bearing_bins"] = environment7
        parameters["torus"] = environment8
        parameters["dynamics"] = environment9
    return parameters


