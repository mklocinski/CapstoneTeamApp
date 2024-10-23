import requests
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
from components import collapsible_sidebar, viewer, chat_with_assistant

main_layout = html.Div(
                className="main-page",
                children=[
                           chat_with_assistant.layout,
                            viewer.tabs,
                            collapsible_sidebar.collapsible_sidebar_layout
                                ]
                        )
