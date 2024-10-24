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
            color_continuous_scale="Cividis"
        )
    fig.update_traces(hovertemplate='<b>Drone ID</b>: %{customdata[0]}<br> <b>Episode</b>: %{customdata[1]}')
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig.update_layout(
        paper_bgcolor='rgb(34,34,34,0)',
        plot_bgcolor='rgb(34,34,34,0)',
        margin=dict(l=0, r=0, t=0, b=0))

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
            dcc.Loading(
                id="loading-drone-traj-plot",
                children=[dcc.Graph(id="drone-traj-plot",
                          className="graph-object")])
            ])
    return div


@callback(
    Output(component_id="drone-traj-plot", component_property="figure"),
    Input(component_id="drone-traj-dropdown-filter", component_property="value"),
    State(component_id="hidden", component_property="children")
)
def render_filtered_traj_graph(filter, json_df):
    if filter == 'all':
        df = pd.read_json(json_df, orient='split')
        fig = chart_drone_trajectories(df)
    else:
        df = pd.read_json(json_df, orient='split')
        filtered_df = df[df['drone_id']==filter]
        fig = chart_drone_trajectories(filtered_df)
    return fig