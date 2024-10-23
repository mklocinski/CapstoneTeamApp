import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc
from dash import html, callback, Input, Output, State

def reward_trend_viewer(reward_data):
    fig = px.line(reward_data, x='episode_id', y='reward')
    fig.update_layout(yaxis_range=[min(reward_data['reward']),
                                   max(reward_data['reward'])],
                      xaxis_range=[0, max(reward_data['episode_id'])],
                      paper_bgcolor='rgb(0,0,0,0)',
                    plot_bgcolor='rgb(0,0,0,0)',
                    margin=dict(l=20, r=10, t=20, b=20),
                           xaxis=dict(title_font=dict(size=10),
                                      showgrid=False),
                           yaxis=dict(title_font=dict(size=10),
                                      showgrid=False),
                           font=dict(size=10, color='white'),
                           )
    return fig


def reward_view(df):
    div = html.Div(children=[
        dcc.Loading(
            id="loading-rewards-plot",
            children=[
                dcc.Graph(figure=reward_trend_viewer(df), className="graph-object")
    ])])
    return div


