import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc
from utils import text
import requests


run_model = dbc.Button('Run Model', id='standard-run', n_clicks=0,
                               color="secondary", className="me-1",
                       size="sm", style={'font-size':'0.75em',
                                         'width':'100%',
                                         'height':'100%'}
                       )

standard_run_status = html.Div(children=[
                        html.Div(id="run-progress-text",
                               className='model-loading-div'),
                            dcc.Interval(
                                    id="status-interval",
                                    interval=2*1000,
                                    n_intervals=0
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
                                    n_intervals=0
                                )
                            ],
                           className="kpi-box")

expected_completion = html.Div(children=[
                            html.Div("Expected Completion", className="kpi-name"),
                            html.Div("--", className="kpi-value")
                            ],
                           className="kpi-box")

damage = html.Div(children=[
                            html.Div("Total Damage", className="kpi-name"),
                            html.Div("--", className="kpi-value")
                            ],
                           className="kpi-box")

make_navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(run_model,
                        width=1),
                dbc.Col(children=[
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
                                id="pause-model-button")])
                    ], width=1),
                    dbc.Col(children=[
                        html.Div(children=[
                         standard_run_status,
                        html.Div(id="output-helper"),
                        html.Div(id="output-helper2"),
                        html.Div(id="run-progress-placeholder"),
                        html.Div(id="db-poller"),
                        dcc.Interval(
                                    id="db-interval",
                                    interval=2*1000,
                                    n_intervals=0
                                )
                        ],
                                 className='play-button-group')
                    ],
                        width=1,
                        align='center'),
                dbc.Col(width=1,
                        children=[current_episode]),
                dbc.Col(width=1,
                        children=[expected_completion]),
                dbc.Col(width=1,
                        children=[damage]),
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



@callback(
    [Output('run-progress-placeholder', 'children')],
    [Input('standard-run', 'n_clicks')],
    [State('environment_parameters', 'data'),
     State('model_parameters', 'data'),
     State('map_parameters', 'data'),
     State('rai_parameters', 'data'),
     State('api_url', 'data')]
)

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
        return [" "]
    else:
        return [" "]

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
    State("api_url", "data")  # Assuming your API URL is stored here
)
def update_current_step(n_intervals, url):
    response = requests.get(f"{url['api_url']}/model/current_episode")
    print(f"{url['api_url']}/model/current_episode")
    if response.status_code == 200:
        step = response.json().get("step")
        return f"{step}"
    else:
        return "--"


@callback(
    Output("db-poller", "children"),
    Input("db-interval", "n_intervals"),
    State("api_url", "data")  # Assuming your API URL is stored here
)
def commit_db(n_intervals, url):
    response = requests.get(f"{url['api_url']}/database/commit")
    print(f"{url['api_url']}/database/commit")
    return ""


@callback(
    Output("run-progress-text", "children"),
    Input("status-interval", "n_intervals"),
    State("api_url", "data")  # Assuming your API URL is stored here
)
def update_current_status(n_intervals, url):
    response = requests.get(f"{url['api_url']}/model/status")
    print(f"{url['api_url']}/model/status")
    if response.status_code == 200:
        status = response.json().get("status")
        print(status)
        if status=="idle":
            return html.Div(children=[html.I(id='idle',
                                    className="bi bi-question-octagon-fill",
                                   style={'color':'gray',
                                          'font-size':'20px'}),
                                      dbc.Popover(
                                          "Idle",
                                          target="idle",
                                          body=True,
                                          trigger="hover")],
                            style={'margin':'auto'})
        elif status=="initializing":
            return html.Div(children=[html.I(id='initializing',
                                    className="bi bi-list-check",
                                   style={'color':'yellow',
                                          'font-size':'20px'}),
                                      dbc.Popover(
                                          "Initializing...",
                                          target="initializing",
                                          body=True,
                                          trigger="hover")])
        elif status=="running":
            return html.Div(children=[html.I(id='running',
                                    className="bi bi-exclamation-circle-fill",
                                   style={'color':'yellow',
                                          'font-size':'20px'}),
                                      dbc.Popover(
                                          "Running...",
                                          target="running",
                                          body=True,
                                          trigger="hover")])
        elif status=="pause":
            return html.Div(children=[html.I(id='paused',
                                    className="bi bi-stopwatch-fill",
                                   style={'color':'gray',
                                          'font-size':'20px'}),
                                      dbc.Popover(
                                          "Model paused",
                                          target="paused",
                                          body=True,
                                          trigger="hover")])
        elif status=="complete":
            return html.Div(children=[html.I(id='complete',
                                    className="bi bi-check-circle-fill",
                                   style={'color':'green',
                                          'font-size':'20px'}),
                                      dbc.Popover(
                                          "Model run complete",
                                          target="complete",
                                          body=True,
                                          trigger="hover")])
    else:
        return "--"

