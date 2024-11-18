import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc
from dash import html, callback, Input, Output, State

def chart_drone_trajectories(df):

    fig = px.scatter(df,
            x="x_coord",
            y="y_coord",
            color="episode_id",
            custom_data=["drone_id", "episode_id"],
            color_continuous_scale="Cividis")

    fig.update_traces(hovertemplate='<b>Drone ID</b>: %{customdata[0]}<br> <b>Episode</b>: %{customdata[1]}')
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig.update_coloraxes(
        colorbar_title="Episode",
        colorbar_title_font=dict(size=10, color="white"),  # Title font size and color
        colorbar_tickfont=dict(size=7, color="white")  # Tick font size and color
    )
    fig.update_layout(
        paper_bgcolor='rgb(34,34,34,0)',
        plot_bgcolor='rgb(34,34,34,0)',
        margin=dict(l=0, r=0, t=0, b=0))
    fig.update_yaxes(title='', visible=False, showticklabels=False, showgrid=False)
    fig.update_xaxes(title='', visible=False, showticklabels=False, showgrid=False)

    return fig

def trajectory_view(df):
    div = html.Div([
                dcc.Dropdown(
                    id='drone-traj-dropdown-filter',
                    className="dropdown",
                    options=[{'label': 'All', 'value':'all'}]+[{'label': "Drone "+str(i), 'value': i} for i in df['drone_id'].unique()],
                    value="all"
                ),
                html.Div(id='hidden', children=df.to_json(orient='split'), hidden=True),
            dcc.Graph(id="drone-traj-plot",
                          className="graph-object",
                      style={'display' : 'none'})])

    return div


