from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text
from components import data_viewer
from components.Visuals import swarm_movements, drone_trajectories, rewards, drone_health
import requests
import pandas as pd


tabs = html.Div(
            className= "swarm-viewer-tab-area",
            children=[
                    dbc.Tabs([
                        #dbc.Tab(label="Drone Health", tab_id="tab-1", className="dash-tabs"),
                        dbc.Tab(label="Rewards", tab_id="tab-2", className="dash-tabs"),
                        dbc.Tab(label="Swarm View",tab_id='tab-3',className= "dash-tabs"),
                        dbc.Tab(label="Trajectories", tab_id="tab-4",className= "dash-tabs")
                    ],
                    id="tabs",
                    active_tab="tab-2"
                ),
                html.Div(id="tab-content")
            ]


)


@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
    State('api_url', 'data')
)
def tab_content(tab, url):
    call = url['api_url']
    #if tab == "tab-1":
        #response = requests.get(f'{call}/database/last_run/tbl_rewards')
        #if response.status_code == 200:
            #data = response.json()
            #df = pd.DataFrame(data)
            #new_cols = [col[5:] for col in df.columns]
            #df.columns = new_cols
        #return drone_health.health_viewer()
    if tab == "tab-3":
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
        else:
            return f"Error"
    elif tab == "tab-2":
        response = requests.get(f'{call}/database/last_run/tbl_rewards')
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            new_cols = [col[5:] for col in df.columns]
            df.columns = new_cols
            return rewards.reward_view(df)
    elif tab == "tab-4":
        response = requests.get(f'{call}/database/last_run/tbl_local_state')
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            new_cols = [col[5:] for col in df.columns]
            df.columns = new_cols
            return drone_trajectories.trajectory_view(df)
        else:
            return f"Error: {response.content.decode()}"


