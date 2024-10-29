import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils import text
import requests

run_model_button = dbc.Button(
    children=["Run Model"],
    className="run-model-button",
    id="run-model-button")

run_model_dropdown = dbc.DropdownMenu(
    id="run-model-dropdown",
    className="m-2",
    label="Run Model",
    children=[
        dbc.DropdownMenuItem(children=["Standard Run"], id="standard-run"),
        dbc.DropdownMenuItem(children=["Live Run"], id="live-run", disabled=True)
    ],
    align_end=False,
)
standard_run_status = dcc.Loading(id="standard-model-run-loading",
                         className='model-loading-div',
                         type="default",
                         children=[html.Div(id="standard-model-run-status")])
live_run_status = dcc.Loading(id="live-model-run-loading",
                         className='model-loading-div',
                         type="default",
                         children=[html.Div(id="live-model-run-status")])
make_navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="d-flex align-items-center",
                        children=[
                            #run_model_button,
                            run_model_dropdown,
                            standard_run_status
                        ]
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div(
                        className="d-flex align-items-center",
                        children=[
                        html.Div(id="hidden-buttons"),
                        html.Div(id="output-helper"),
                        ]),
                    width=2),
                dbc.Col(
                    children=[
                        live_run_status
                    ],
                    width=1),
                dbc.Col(width=True),
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.DropdownMenu(
                                label="Menu",
                                children=[
                                    dbc.DropdownMenuItem("Home", href="/", id='home-nav', class_name='navlink'),
                                    dbc.DropdownMenuItem("View Data", href="/view-data", id='view-data-nav',
                                                         class_name='navlink'),
                                    dbc.DropdownMenuItem("About", href="/about", id='about-nav', class_name='navlink'),
                                ],
                                nav=True,
                                in_navbar=True,
                                align_end=True
                            ),
                        ],
                        className="ms-auto"
                    ),
                    width="auto"
                ),
            ],
            className="w-100",
            align="center"
        ),
        fluid=True
    ),
    color="dark",
    dark=True,
    className="navbar"
)



@callback(
    [Output('standard-model-run-loading', 'children'),
     Output('model-run-type', 'data')],
    [Input('standard-run', 'n_clicks'),
     Input('live-run', 'n_clicks')],
    [State('environment_parameters', 'data'),
     State('model_parameters', 'data'),
     State('map_parameters', 'data'),
     State('rai_parameters', 'data')]
)
def run_model(standard_clicked, live_clicked, env_p, mod_p, map_p, rai_p):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", {"run-status": "off"}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    payload = {"environment_parameters": env_p,
               "model_parameters": mod_p,
               "map_parameters": map_p,
               "rai_parameters": rai_p}

    # Handle standard run
    if button_id == 'standard-run' and standard_clicked:
        response = requests.post('https://xraiapi-ba66c372be3f.herokuapp.com/model/standard/run_xrai', json=payload)
        if response.status_code == 200:
            success = html.I(id="model-run-success-icon",
                             className="bi bi-check-circle-fill",
                             style={'color': '#4d6b53'})
            result_hover = dbc.Popover(
                dbc.PopoverBody("Model ran successfully!"),
                target="model-run-success-icon",
                trigger="hover",
            )
            return [success, result_hover], {"run-status": "standard"}
        else:
            failure = html.I(id="model-run-fail-icon",
                             className="bi bi-exclamation-circle-fill",
                             style={'color': '#FF0000'})
            result_hover = dbc.Popover(
                dbc.PopoverBody(response.text),
                target="model-run-fail-icon",
                trigger="hover",
            )
            return [failure, result_hover], {"run-status": "standard"}

    # Handle live run
    elif button_id == 'live-run' and live_clicked:
        return "", {"run-status": "live"}

    return "", {"run-status": "off"}


# Callback to show the buttons dynamically when the live model is selected
@callback(
    Output("hidden-buttons", "children"),
    Input("model-run-type", "data")
)
def show_player_buttons(run_type):
    if run_type["run-status"] == "live":
        return html.Div(className="player-button-group",
                        children=[
                            dbc.Button(
                                children=["Play"],
                                className="player-buttons",
                                id="play-model-button"),
                            dbc.Button(
                                children=["Pause"],
                                className="player-buttons",
                                id="pause-model-button")
                        ])
    return ""  # Return nothing if not in "live" mode


# Callback to handle the play button in live mode
@callback(
    Output('live-model-run-loading', 'children'),
    Input('play-model-button', 'n_clicks'),
    [State('environment_parameters', 'data'),
     State('model_parameters', 'data'),
     State('map_parameters', 'data'),
     State('rai_parameters', 'data')]
)
def run_live_model(clicks, env_p, mod_p, map_p, rai_p):
    if clicks:
        payload = {"environment_parameters": env_p,
                   "model_parameters": mod_p,
                   "map_parameters": map_p,
                   "rai_parameters": rai_p}

        response = requests.post('https://xraiapi-ba66c372be3f.herokuapp.com/model/live/run_xrai', json=payload)

        if response.status_code == 200:
            success = html.I(id="model-run-success-icon",
                             className="bi bi-check-circle-fill",
                             style={'color': '#4d6b53'})
            result_hover = dbc.Popover(
                dbc.PopoverBody("Model ran successfully!"),
                target="model-run-success-icon",
                trigger="hover",
            )
            return [success, result_hover]
        else:
            failure = html.I(id="model-run-fail-icon",
                             className="bi bi-exclamation-circle-fill",
                             style={'color': '#FF0000'})
            result_hover = dbc.Popover(
                dbc.PopoverBody(response.text),
                target="model-run-fail-icon",
                trigger="hover",
            )
            return [failure, result_hover]
    return ""

@callback(
    Output(component_id="output-helper", component_property='children'),
    Input('pause-model-button', 'n_clicks')
)
def pause_live_model(clicks):
    if clicks:

        response = requests.post('https://xraiapi-ba66c372be3f.herokuapp.com/model/pause')

        if response.status_code == 200:

            return ""
        else:

            return ""
    return ""

