from dash import html
import dash_bootstrap_components as dbc
from components import fleet_viewer

main_layout = html.Div(

        dbc.Container(children=[
            dbc.Row([
            dbc.Col([
                fleet_viewer.fleet_view
                ], width=6, class_name='standard-container')
            ,
            dbc.Col([
                fleet_viewer.reward_view,
                fleet_viewer.details
                ], width=6,  style={'width': '60%',
                                    'display': 'inline-block',
                                    'padding': '20px 0px 0px 0px'})
            ]),
            ], fluid=True)
)


