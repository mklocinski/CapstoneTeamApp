from dash import html, callback, Input, Output, State, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
import requests
import pandas as pd


table_dropdown = dcc.Dropdown(id='data_tbl_drop_down_comp',
                              className="dropdown",
                              options=[
                                  {'label': 'Local State Data', 'value':'tbl_local_state'},
                                  {'label': 'Global State Data', 'value':'tbl_global_state'},
                                  {'label': 'Reward Data', 'value':'tbl_rewards'},
                                  {'label': 'Drone Action Data', 'value':'tbl_drone_actions'},
                                  {'label': 'Model Run Parameters', 'value':'tbl_model_run_params'},
                                  {'label': 'Model Runs', 'value':'tbl_model_runs'}
                              ],
                              placeholder='Select model output table'
                              )
load_table_button = html.Button('Load Data', id='data-load-button', n_clicks=0)
download_button = html.Button('Download CSV', id='download-button')
download_component = dcc.Download(id="download-data")
table = dcc.Loading(
        id='loading-2',
        type='default',
        children=[
            dash_table.DataTable(
                id='data_page_table',
                columns=[],
                data=[],
                page_size=150,  # Number of rows per page
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_header={'backgroundColor': '#000000', 'color':'white'},
                style_cell={'backgroundColor': '#454545', 'color':'white', 'fontSize':'0.75em'},
                style_as_list_view=True
            )
        ]
    )
layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([table_dropdown]),
        dbc.Col([load_table_button])
    ]),
    dbc.Row([
            table
    ]),
    html.Button('Download Data', id='download-button'),
    download_component
])

dash.register_page("View Data", layout=layout, path="/view-data", order=2)


# Callbacks
@callback(
    Output('data_page_table', 'columns'),
    Output('data_page_table', 'data'),
    Input('data-load-button','n_clicks'),
    State('data_tbl_drop_down_comp', 'value')
)
def load_table(n_clicks, value):
    if n_clicks > 0 and value:
        url = f'https://xraiapi-ba66c372be3f.herokuapp.com/database/last_run/{value}'
        response = requests.get(url)
        if response.status_code == 200:
            print("Data successfully fetched from API")
            data = response.json()
            df = pd.DataFrame(data)
            print(f"Fetched {len(df)} rows from the database")
            columns = [{'name': col, 'id': col} for col in df.columns]
            data = df.to_dict('records')
            return columns, data
        else:
            print(f"API call failed with status code: {response.status_code}")
            return [], []
    return [], []

@callback(
    Output("download-data", "data"),
    Input("download-button", "n_clicks"),
    State('data_page_table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, table_data):
    if n_clicks > 0 and table_data:
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_csv, "table_data.csv", index=False)
    return None