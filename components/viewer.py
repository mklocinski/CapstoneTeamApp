from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text
from plotly import graph_objects as go
from components.Visuals import swarm_movements, drone_trajectories, rewards, drone_health
import requests
import pandas as pd


tabs = html.Div(
            className= "swarm-viewer-tab-area",
            children=[
                dcc.Interval(id='tab-1-interval', interval=10000, n_intervals=0, disabled=False),
                dcc.Interval(id='tab-2-interval', interval=10000, n_intervals=0, disabled=False),
                # dcc.Interval(id='tab-3-interval', interval=5000, n_intervals=0, disabled=False),
                # dcc.Interval(id='tab-4-interval', interval=5000, n_intervals=0, disabled=False),
                dbc.Tabs([
                        dbc.Tab(label="Rewards", tab_id="tab-1", className="dash-tabs"),
                        dbc.Tab(label="Swarm View",tab_id='tab-2',className= "dash-tabs"),
                        dbc.Tab(label="Trajectories", tab_id="tab-3",className= "dash-tabs"),
                        dbc.Tab(label="Playback", tab_id="tab-4",className= "dash-tabs")
                    ],
                    id="tabs",
                    active_tab="tab-1"
                ),
                html.Div(id="tab-content")
            ]


)

@callback(
    [Output('tab-1-interval', 'disabled'),
     Output('tab-2-interval', 'disabled')],
    [Input("tabs", "active_tab"),
     Input("model-run-status", "data")]
)
def update_intervals(active_tab, model_status):
    if model_status["run-status"] == "running":
        return [
            active_tab != "tab-1",
            active_tab != "tab-2",

        ]
    else:
        return True, True


@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
    State('api_url', 'data')
)
def tab_content(tab, url):
    call = url['api_url']
    if tab == "tab-4":
        response1 = requests.get(f'{call}/database/last_run/tbl_local_state')
        response2 = requests.get(f'{call}/database/last_run/tbl_map_data')
        print(response1.status_code)
        print(response2.status_code)
        if response1.status_code == 200 and response2.status_code == 200:
            data = response1.json()
            df = pd.DataFrame(data)
            new_cols = [col[5:] for col in df.columns]
            df.columns = new_cols

            map_data = response2.json()
            map_df = pd.DataFrame(map_data)
            new_cols = [col[5:] for col in map_df.columns]
            map_df.columns = new_cols
            return swarm_movements.swarm_view(df, map_df)
        elif response1.status_code == 200 and response2.status_code != 200:
            data = response1.json()
            df = pd.DataFrame(data)
            new_cols = [col[5:] for col in df.columns]
            df.columns = new_cols
            map_df = None
            return swarm_movements.swarm_view(df, map_df)
        else:
            return f"Error"
    elif tab == "tab-2":
        return swarm_movements.no_playback_view()
    elif tab == "tab-1":
        return rewards.reward_view()
    elif tab == "tab-3":
        response = requests.get(f'{call}/database/last_run/tbl_local_state')
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            new_cols = [col[5:] for col in df.columns]
            df.columns = new_cols
            return drone_trajectories.trajectory_view(df)
        else:
            return f"Error: {response.content.decode()}"


@callback(Output("reward_viz", "figure"),
          Output("reward_viz", "style"),
          Input("tab-1-interval", "n_intervals"),
          State("api_url", "data"),
          State("model-run-status", "data"),
          State("current-episode-value", "children"))
def update_tab_1(n_interval, url, status, episode):
    print("Loading Rewards Graph")
    call = url['api_url']
    print(f'{call}/database/last_run/tbl_rewards')
    response = requests.get(f'{call}/database/last_run/tbl_rewards')
    print(f"Request Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        print(f"Number of rows in reward data: {len(df)}")
        new_cols = [col[5:] for col in df.columns]
        print(new_cols)
        df.columns = new_cols
        return rewards.reward_trend_viewer(df), {'display': 'inline'}
    else:
        return f"Error: {response.content.decode()}", {'display': 'none'}




@callback(
    Output(component_id="drone-traj-plot", component_property="figure"),
    Output("drone-traj-plot", "style"),
    Input(component_id="drone-traj-dropdown-filter", component_property="value"),
    #Input("tab-3-interval", "n_intervals"),
    State("api_url", "data"),
    State(component_id="hidden", component_property="children")
)
def update_tab_3(fltr, url, json_df):
    call = url['api_url']
    response = requests.get(f'{call}/database/last_run/tbl_local_state')
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        new_cols = [col[5:] for col in df.columns]
        df.columns = new_cols
        if fltr == 'all':
            df = pd.read_json(json_df, orient='split')
            fig = drone_trajectories.chart_drone_trajectories(df)
        else:
            df = pd.read_json(json_df, orient='split')
            filtered_df = df[df['drone_id'] == fltr]
            fig = drone_trajectories.chart_drone_trajectories(filtered_df)
        return fig, {'display' : 'inline'}
    else:
        return f"Error: {response.content.decode()}", {'display' : 'inline'}


@callback(Output("static-swarm-movement-plot", "figure"),
          Output("static-swarm-movement-plot", "style"),
          Input("tab-2-interval", "n_intervals"),
          State("api_url", "data"),
          State("model-run-status", "data"))
def update_tab_2(n_interval, url, status):
    call = url['api_url']
    response1 = requests.get(f'{call}/database/last_run/tbl_local_state')
    response2 = requests.get(f'{call}/database/last_run/tbl_map_data')
    print(f"Local Data: {response1.status_code}, Map Data: {response2.status_code}")
    if response1.status_code == 200 and response2.status_code == 200:
        data = response1.json()
        df = pd.DataFrame(data)
        new_cols = [col[5:] for col in df.columns]
        df.columns = new_cols
        map_data = response2.json()
        map_df = pd.DataFrame(map_data)
        new_cols = [col[5:] for col in map_df.columns]
        map_df.columns = new_cols
        return swarm_movements.static_scatterplot(df, map_df), {'display' : 'inline'}
    elif response1.status_code == 200 and response2.status_code != 200:
        data = response1.json()
        df = pd.DataFrame(data)
        new_cols = [col[5:] for col in df.columns]
        df.columns = new_cols
        map_df = None
        return swarm_movements.static_scatterplot(df, map_df), {'display' : 'inline'}
    else:
        return f"Error: {response1.content.decode()}", {'display' : 'inline'}