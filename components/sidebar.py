from dash import html, callback, Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from utils import text

sidebar_title = html.H2(
    id="sidebar_title", children=[text.run_page_sidebar_title]
)
sidebar_description = html.P(
    id="sidebar_description", children=[text.run_page_sidebar_description]
)


map_dropdown = dcc.Dropdown(
    ["Map 1", "Map 2", "Map 3"],
    'Map 2',
    id="run_page_map_dropdown_comp",
    className="dropdown"
)
agent_slider = dcc.Slider(id="run_page_agent_slider_comp",
                        #className="slider",
                          min=0,
                          max=50,
                          step=10,
                          value=20)

obs_mode_dropdown = dcc.Dropdown(
    text.run_page_obs_mode_dropdown,
    'sum_obs_acc',
    id="run_page_obs_mode_dropdown_comp",
    className="dropdown"
)

comm_radius_slider = dcc.Slider(id="run_page_comm_radius_slider_comp",
                        #className="slider",
                          min=0,
                          max=100,
                          step=20,
                          value=100)

world_size_slider = dcc.Slider(id="run_page_world_size_slider_comp",
                            #className="slider",
                          min=0,
                          max=100,
                          step=20,
                          value=100)

run_model_button = html.Button(id='run_page_run_button',
                               className="",
                               n_clicks=0,
                               children=["Run"])


sidebar_layout = html.Div(
    id="run_page_sidebar",
    className="sidebar",
    children=[
        sidebar_title,
        sidebar_description,
        html.Div(id="run_page_sidebar_input_menu",
                 className="outline-emphasis",
                 children=[
        html.Div(className="run-option-div",
                 children=[
            html.H4(text.run_page_map_text),
             map_dropdown
                 ]
                 ),
        html.Div(
            className="run-option-div",
            children=[
            html.H4(text.run_page_agent_slider_text),
             agent_slider]
        ),
        html.Div(
            className="run-option-div",
            children=[html.H4(text.run_page_obs_mode_text),
                obs_mode_dropdown]
        ),
        html.Div(
            className="run-option-div",
            children=[html.H4(text.run_page_world_size_text),
             world_size_slider]
        ),
        html.Div(dcc.Checklist(
    className="run-option-checklist-div",
    options=['Avoid Collisions', 'Avoid Buffer Zones',
     'Avoid All Damage', 'Avoid Maximum Allowable Damage'],
    value=['Avoid Collisions'],
    inline=True
)),
        html.Div(dbc.Row([
                dbc.Col(run_model_button),
                dbc.Col([html.Div(id="model_status"),
                         dcc.Loading(
                             id="loading-1",
                             className='model-loading-div',
                             type="default",
                             children=html.Div(id="model_status")
                         )
                         ]
                        )
            ]))
        ])

    ]
)



@callback(
    Output('model_status', 'children'),
    Input('run_page_run_button', 'n_clicks')
)
def run_model(n_clicks):
    if n_clicks:
        # Send a POST request to the Flask API
        response = requests.post('https://xraiapi-ba66c372be3f.herokuapp.com/model/standard/run_xrai')
        if response.status_code == 200:
            data = response.json()
            return f"Model Output: {data['model_output']}"
        else:
            return f"Error: {response.content.decode()}"
    return ""