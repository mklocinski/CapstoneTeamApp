import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc
import time
import requests


def make_status_icon(status):
    if status == "idle":
        return html.Div(children=[html.I(id='idle',
                                         className="bi bi-question-octagon-fill",
                                         style={'color': 'gray',
                                                'font-size': '20px'}),
                                  dbc.Popover(
                                      "Idle",
                                      target="idle",
                                      body=True,
                                      trigger="hover")],
                        style={'margin': 'auto'}), {"run-status": "off"}
    elif status == "initializing":
        return html.Div(children=[html.I(id='initializing',
                                         className="bi bi-list-check",
                                         style={'color': 'yellow',
                                                'font-size': '20px'}),
                                  dbc.Popover(
                                      "Initializing...",
                                      target="initializing",
                                      body=True,
                                      trigger="hover")]), {"run-status": "running"}
    elif status == "running":
        return html.Div(children=[html.I(id='running',
                                         className="bi bi-exclamation-circle-fill",
                                         style={'color': '#fec036',
                                                'font-size': '20px'}),
                                  dbc.Popover(
                                      "Running...",
                                      target="running",
                                      body=True,
                                      trigger="hover")]), {"run-status": "running"}
    elif status == "pause":
        return html.Div(children=[html.I(id='paused',
                                         className="bi bi-stopwatch-fill",
                                         style={'color': 'gray',
                                                'font-size': '20px'}),
                                  dbc.Popover(
                                      "Model paused",
                                      target="paused",
                                      body=True,
                                      trigger="hover")]), {"run-status": "running"}
    elif status == "complete":
        return html.Div(children=[html.I(id='complete',
                                         className="bi bi-check-circle-fill",
                                         style={'color': 'green',
                                                'font-size': '20px'}),
                                  dbc.Popover(
                                      "Model run complete",
                                      target="complete",
                                      body=True,
                                      trigger="hover")]), {"run-status": "off"}


run_model = dbc.Button('Run Model', id='standard-run', n_clicks=0,
                               color="secondary", className="me-1",
                       size="sm", style={'font-size':'1em',
                                         'width':'100%',
                                         'height':'100%'}
                       )

standard_run_status = html.Div(children=[
                        html.Div(id="run-progress-text",
                               className='model-loading-div'),
                            dcc.Interval(
                                    id="status-interval",
                                    interval=4*1000,
                                    n_intervals=0,
                                    disabled=True
                                )])


current_episode = html.Div(children=[
                            html.Div("Current Episode",
                                     className="kpi-name"),
                            html.Div("--",
                                     id="current-episode-value",
                                     className="kpi-value"),
                            dcc.Interval(
                                    id="episode-interval",
                                    interval=2*1000,
                                    n_intervals=0,
                                    disabled=True
                                )
                            ],
                           className="kpi-box")

damaged_drones = html.Div(children=[
                            html.Div("# Drones Damaged", className="kpi-name"),
                            html.Div("--", className="kpi-value", id='damaged-drone-count')
                            ],
                           className="kpi-box")

total_damage = html.Div(children=[
                            html.Div("Total Damage", className="kpi-name"),
                            html.Div("--", className="kpi-value", id='total-damage-sum')
                            ],
                           className="kpi-box")

refresh_trigger = dcc.Location(id="refresh-trigger")
make_navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(run_model,
                        width=1),
                dbc.Col(children=[
                        refresh_trigger,
                        html.Div(children=[
                            dbc.Button(
                                n_clicks=0,
                                children=["▶"],
                                className="player-buttons",
                                id="play-model-button"),
                            dbc.Button(
                                n_clicks=0,
                                children=["▐▐"],
                                className="player-buttons",
                                id="pause-model-button"),
                            dbc.Button(
                                n_clicks=0,
                                children=["■"],
                                className="player-buttons",
                                id="stop-model-button")])
                    ], width=1),
                    dbc.Col(children=[
                        html.Div(children=[
                         standard_run_status,
                        html.Div(id="output-helper"),
                        html.Div(id="output-helper2"),
                        html.Div(id="output-helper3"),
                        html.Div(id="run-progress-placeholder"),
                        html.Div(id="db-poller"),
                        dcc.Interval(
                                    id="db-interval",
                                    interval=1000,
                                    n_intervals=0,
                                    disabled=True
                                )
                        ],
                                 className='play-button-group')
                    ],
                        width=1,
                        align='center'),
                dbc.Col(width=1,
                        children=[current_episode]),
                dbc.Col(width=1,
                        children=[damaged_drones]),
                dbc.Col(width=1,
                        children=[total_damage]),
                dbc.Col(width=True,
                        children=[html.Div(children=["lol"])]),
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



@callback(Output("episode-interval", "disabled"),
     Output("db-interval", "disabled"),
    Output("status-interval", "disabled",
           allow_duplicate=True),
          Input("model-run-status", "data"),
          prevent_initial_call=True)
def start_polling(status):
    if status["run-status"] == "running":
        return False, False, False
    else:
        return True, True, True

@callback(
    [Output('run-progress-placeholder', 'children'),
     Output("status-interval", "disabled", allow_duplicate=True)],
    [Input('standard-run', 'n_clicks')],
    [State('environment_parameters', 'data'),
     State('model_parameters', 'data'),
     State('map_parameters', 'data'),
     State('rai_parameters', 'data'),
     State('api_url', 'data')],
prevent_initial_call=True)

def run_model(standard_clicked, env_p, mod_p, map_p, rai_p, url):
    if standard_clicked is None or standard_clicked == 0:
        raise dash.exceptions.PreventUpdate
    payload = {"environment_parameters": env_p,
               "model_parameters": mod_p,
               "map_parameters": map_p,
               "rai_parameters": rai_p}

    call = url['api_url']
    print(f'{call}/model/standard/run_xrai')
    response = requests.post(f'{call}/model/standard/run_xrai', json=payload)
    if response.status_code == 200:
        return [" "], False
    else:
        return [" "], True

# Callback to show the buttons dynamically when the live model is selected

@callback(
    Output(component_id="output-helper", component_property='children'),
    Input('pause-model-button', 'n_clicks'),
    State('api_url', 'data')
)
def pause_live_model(clicks, url):
    if clicks:
        print("Pause button clicked")
        call = url['api_url']
        print(f'{call}/model/pause')
        response = requests.get(f'{call}/model/pause')
        if response.status_code == 200:
            return ""


@callback(
    Output(component_id="output-helper3", component_property='children'),
    Input('stop-model-button', 'n_clicks'),
    State('api_url', 'data')
)
def play_live_model(clicks, url):
    if clicks:
        print("Stop button clicked")
        call = url['api_url']
        print(f'{call}/model/stop')
        response = requests.get(f'{call}/model/stop')
        if response.status_code == 200:
            return ""

@callback(
    Output(component_id="output-helper2", component_property='children'),
    Input('play-model-button', 'n_clicks'),
    State('api_url', 'data')
)
def play_live_model(clicks, url):
    if clicks:
        print("Play button clicked")
        call = url['api_url']
        print(f'{call}/model/play')
        response = requests.get(f'{call}/model/play')
        if response.status_code == 200:
            return ""

@callback(
    Output("current-episode-value", "children"),
    Input("episode-interval", "n_intervals"),
    State("api_url", "data"),
    State("model-run-status", "data")# Assuming your API URL is stored here
)
def update_current_step(n_intervals, url, status):
    if status["run-status"] == "running":
        response = requests.get(f"{url['api_url']}/model/current_episode")
        print(f"{url['api_url']}/model/current_episode")
        if response.status_code == 200:
            step = response.json().get("step")
            print(f"success: {step}")
            return f"{step}"
        else:
            return "--"
    else:
            return "0"


@callback(
    [Output("db-poller", "children"),
     Output("damaged-drone-count", "children"),
     Output("total-damage-sum", "children")],
    Input("db-interval", "n_intervals"),
    State("api_url", "data"),
    State("model-run-status", "data")
)
def commit_db(n_intervals, url, status):
    response = requests.get(f"{url['api_url']}/database/commit")
    print(status)
    print(f"{url['api_url']}/database/commit")
    print(response)
    r_damage_count = requests.get(f"{url['api_url']}/database/last_run/drone_damage_count")
    r_total_damage = requests.get(f"{url['api_url']}/database/last_run/total_drone_damage")
    if status == "running":
        if r_damage_count.status_code == 200:
            damage_count = r_damage_count.json().get("unique_drones_with_damage")
        else:
            damage_count = "0"

        if r_total_damage.status_code == 200:
            total_damage = r_total_damage.json().get("total_drone_damage")

        else:
            total_damage = "0"

        return "", damage_count, total_damage
    else:
        return "", "0", "0"


@callback(
    Output("run-progress-text", "children"),
    Output("model-run-status", "data"),
    Input("status-interval", "n_intervals"),
    State("api_url", "data"),
prevent_initial_call=True
)
def update_current_status(n_intervals, url):
    response = requests.get(f"{url['api_url']}/model/status")
    print(f"{url['api_url']}/model/status")
    if response.status_code == 200:
        status = response.json().get("status")
        print(f"Status: {status}")
        return make_status_icon(status)
    else:
        return "--", {"run-status":"off"}


@callback(Output("run-progress-text", "children", allow_duplicate=True),
    Output("model-run-status", "data", allow_duplicate=True),
          Input("refresh-trigger", "href"),
            State("api_url", "data"),
prevent_initial_call=True)
def refresh_page(refresh, url):
    if refresh is None:
        raise dash.exceptions.PreventUpdate
    if refresh:
        response = requests.get(f"{url['api_url']}/model/status")
        print(f"{url['api_url']}/model/status")
        if response.status_code == 200:
            status = response.json().get("status")
            print(f"Startup Status: {status}")
            return make_status_icon(status)
