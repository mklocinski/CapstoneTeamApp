from dash import html, callback, Input, Output, dcc
import dash
import dash_bootstrap_components as dbc

layout = dbc.Container(children=[
    html.Button("Download Text", id="btn-download-txt"),
    dcc.Download(id="download-text")
])


dash.register_page("Resources", layout=layout, path="/resources", order=4)

@callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dict(filename="../components/tbl_local_state.csv")
