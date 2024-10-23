from dash import html, callback, Input, Output, dcc
import dash
import dash_bootstrap_components as dbc
from utils import text


project = html.H2(id="project", children=[text.about_page_project])
project_description = html.P(
    id="project_description", children=[text.about_page_project_description]
)
model = html.H2(id="model", children=[text.about_page_model])
model_description = html.P(
    id="model_description", children=[text.about_page_model_description]
)
layout = dbc.Container(children=[project,
                                project_description,
                                model,
                                model_description
])


dash.register_page("About", layout=layout, path="/about", order=3)
