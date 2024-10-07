from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc

make_navbar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id='home-nav', class_name='navlink'),
                dbc.NavLink("Upload Datasets", href="/view-datasets", id='update-datasets-nav', class_name='navlink'),
                dbc.NavLink("Ask Questions", href="/ask-questions", id='ask-questions-nav', class_name='navlink')
                #dbc.NavLink("Resources", href="/resources", id='resources-nav', class_name='navlink'),
            ], horizontal='end',
        class_name='navbar'),
        html.Br(),
    ]
)



