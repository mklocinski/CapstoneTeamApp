from dash import html, callback, Input, Output, State, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from utils.app_utils import reorder_tbl, dt_data_type, get_tbl_col_def

table_dropdown = dcc.Dropdown(id='data_tbl_drop_down_comp',
                              className="dropdown",
                              options=[
                                  {'label': 'Local State Data', 'value':'tbl_local_state'},
                                  {'label': 'Global State Data', 'value':'tbl_global_state'},
                                  {'label': 'Reward Data', 'value':'tbl_rewards'},
                                  {'label': 'Drone Action Data', 'value':'tbl_drone_actions'},
                                  {'label': 'Map Data', 'value':'tbl_map_data'},
                                  {'label': 'RAI Data', 'value':'tbl_rai'},
                                  {'label': 'Model Run Parameters', 'value':'tbl_model_run_params'},
                                  {'label': 'Model Runs', 'value':'tbl_model_runs'}
                              ],
                              placeholder='Select model output table'
                              )
load_table_button = dbc.Button('Load Data', id='data-load-button', n_clicks=0,
                               color="secondary", className="me-1")
download_button = dbc.Button('Download CSV', id='download-button',
                             color="secondary", className="me-1")
download_component = dcc.Download(id="download-data")
message = html.Div(html.P("Hover over column names for definitions."))
table = dcc.Loading(
        id='loading-2',
        type='default',
        children=[
            dash_table.DataTable(
                id='data_page_table',
                columns=[],
                data=[],
                tooltip_header={},
                page_size=150,  # Number of rows per page
                style_table={'height': '375px', 'overflowY': 'auto'},
                style_header={'backgroundColor': '#000000', 'color':'white'},
                style_cell={'backgroundColor': '#454545', 'color':'white', 'fontSize':'0.75em'},
                style_as_list_view=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                filter_options={
                           'placeholder_text': 'Type filter...',
                           'case': 'insensitive'
                        },
                style_filter={
                            'backgroundColor': '#919191',
                            'color': 'black',
                        }
            )
        ]
    )
layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([table_dropdown]),
        dbc.Col([load_table_button])
    ]),
    dbc.Row([
            message,
            table
    ]),
    download_button,
    download_component
])

dash.register_page("View Data", layout=layout, path="/view-data", order=2)


# Callbacks
@callback(
    Output('data_page_table', 'columns'),
    Output('data_page_table', 'data'),
    Output('data_page_table', 'tooltip_header'),
    Input('data-load-button','n_clicks'),
    [State('data_tbl_drop_down_comp', 'value'),
    State('api_url', 'data')]
)
def load_table(n_clicks, value, url):
    if n_clicks > 0 and value:
        call = url['api_url']
        url = f'{call}/database/last_run/{value}'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            print("Data successfully fetched from API")
            data = response.json()
            df = pd.DataFrame(data)
            df = df[reorder_tbl(value)]
            if "cint_episode_id" in df.columns:
                df = df.sort_values(by="cint_episode_id")
            dtypes = [dt_data_type(col) for col in df.columns]
            unprefix = [col[5:] if col != "id" else col for col in df.columns]
            formatted = [col.replace("_"," ").title() for col in unprefix]
            old_new = {old:new for old,new in zip(df.columns, formatted)}
            descriptions = {old_new[old]:desc for old, desc in get_tbl_col_def(value).items()}
            df.columns = formatted
            print(f"Fetched {len(df)} rows from the database")

            columns = []
            for i, x in enumerate(df.columns):
                columns.append({'name': formatted[i],
                                'id': df.columns[i],
                                'type':dtypes[i]})
            data = df.to_dict('records')
            return columns, data, descriptions
        else:
            print(f"API call failed with status code: {response.status_code}")
            return [], [], {}
    return [], [], {}

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