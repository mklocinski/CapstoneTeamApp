import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc
from plotly.subplots import make_subplots

# ------------------------------------------------------------------ #
# ---------------------- General Functions ------------------------- #
# ------------------------------------------------------------------ #

def get_updatemenus(x_pos=0.15, fr_duration=50):
    return [dict(x=x_pos,
                 y=-0.1,
                 type='buttons',
                 showactive=False,
                 buttons=[dict(label='▶',
                               method='animate',
                               args=[None,
                                     dict(mode='immediate',
                                          transition={'duration': 0, 'easing':'linear'},
                                          fromcurrent=True,
                                          frame=dict(redraw=True, duration=fr_duration)
                                          )
                                     ]
                               ),
                          dict(label='▐▐',
                               method='animate',
                               args=[[None],
                                     dict(mode='immediate',
                                          transition={'duration': 0, 'easing':'linear'},
                                          frame=dict(redraw=True, duration=0)
                                          )
                                     ]
                               )
                          ],
                 direction="left",
                 pad={"r": 0, "t": 0},
                 xanchor="right",
                 yanchor="top",
                 font=dict(family="Arial", size=12, color="black"),
                 bgcolor="#3b3b3b",
                 bordercolor="gray",
                 borderwidth=1
                 )
            ]


# ------------------------------------------------------------------ #
# ------------------------ Swarm Viewer ---------------------------- #
# ------------------------------------------------------------------ #

# ------------------------ Swarm Viewer ---------------------------- #
def basic_swarm_viewer(drone_data):
    fig = go.Figure([go.Scatter(x=[drone_data['x_coord'].iloc[[0, 19]]],
                       y=[drone_data['y_coord'].iloc[[0, 19]]],
                 mode="markers",
                 text=[drone_data['drone_id'].iloc[[0, 19]]],
                 marker=dict(size=8, symbol="x-thin",
                             line=dict(width=2, color="white")),
                 name='scatter')])
    fig.update_layout(yaxis_range=[-100, 100],
                      xaxis_range=[-100, 100],
                      # autosize=True,
                      # width=500,
                      paper_bgcolor='rgb(34,34,34)',
                      plot_bgcolor='rgb(34,34,34)',
                      margin=dict(l=0, r=0, t=0, b=0),
                      yaxis=dict(tickfont=dict(size=5, color='white'),
                                 ticklabelposition='inside',
                                 automargin=False),
                      xaxis=dict(tickfont=dict(size=5, color='white'),
                                 ticklabelposition='inside',
                                 showgrid=False)
                      )
    n_frames = list(drone_data['episode_id'].unique())
    frames = []
    for n in n_frames:
        df = drone_data[drone_data['episode_id'] == n]
        frames.append(go.Frame(data=[
            go.Scatter(x=list(df['x_coord']),
                       y=list(df['y_coord']),
                       mode='markers',
                       text=list(df['drone_id']),
                       customdata=df,
                       marker=dict(size=8, symbol="x-thin",
                                   line=dict(width=1, color="white")),
                       hovertemplate="<b>Drone %{text}</b><br>X: %{x} <br>Y: %{y}<br>Orientation: %{customdata[4]}<br>Linear Velocity: %{customdata[6]}<br>Angular Velocity: %{customdata[7]}",
                       name='t=' + str(n))
        ],
            traces=[2],
            name='t=' + str(n)))
    sliders = [dict(steps=[dict(method='animate',
                                args=[['t=' + str(n)],
                                      dict(mode='e',
                                           frame=dict(duration=400, redraw=True),
                                           transition=dict(duration=0))
                                      ],
                                label=f'{n}'
                                ) for n in n_frames],
                    active=1,
                    transition=dict(duration=10),
                    x=0.20,  # slider starting position
                    y=0,
                    currentvalue=dict(font=dict(size=12),
                                      prefix='t = ',
                                      visible=True,
                                      xanchor='center'
                                      ),
                    len=0.80,
                    tickwidth=0,
                    ticklen=5,
                    pad=dict(b=5),
                    font=dict(size=10, color='white'))  # slider length
               ]

    fig.update_layout(updatemenus=get_updatemenus(),
                      sliders=sliders
                      )
    fig.update(frames=frames)

    return fig

def create_fleet_viewer(drone_data,
                        obstacle_position_matrix,
                        obstacle_matrix_range):
    fig = go.Figure([go.Heatmap(),
                     go.Heatmap(z=obstacle_position_matrix,
                                x=obstacle_matrix_range,
                                y=obstacle_matrix_range,
                                colorscale='Inferno',
                                showlegend=False,
                                showscale=False,
                                hovertemplate="<br>X: %{x} <br>Y: %{y}<br>Obstacle? %{z}",
                                name='Obstacle Map'),
                     go.Scattergl(x=[drone_data['x_coord'].iloc[[0, 19]]], y=[drone_data['y_coord'].iloc[[0, 19]]],
                                mode="markers",
                                text=[drone_data['drone_id'].iloc[[0, 19]]],
                                marker=dict(size=8, symbol="x-thin",
                                            line=dict(width=2, color="white")),
                                name='scatter')])
    fig.update_layout(yaxis_range=[-100, 100],
                      xaxis_range=[-100, 100],
                      paper_bgcolor='#454545',
                      plot_bgcolor='rgb(34,34,34)',
                      margin=dict(l=0, r=0, t=0, b=0),
                      yaxis=dict(tickfont=dict(size=5, color='white'),
                                 ticklabelposition='inside'
                                 #automargin=True
                                 #scaleanchor='x',
                                 #scaleratio=1
                                 ),
                      xaxis=dict(tickfont=dict(size=5, color='white'),
                                 ticklabelposition='inside',
                                # automargin=True,
                                 showgrid=False)
                      )
    n_frames = list(drone_data['episode_id'].unique())
    frames = []
    for n in n_frames:
        df = drone_data[drone_data['episode_id'] == n]
        frames.append(go.Frame(data=[
            go.Scatter(x=list(df['x_coord']),
                       y=list(df['y_coord']),
                       mode='markers',
                       text=list(df['drone_id']),
                       customdata = df,
                       marker=dict(size=8, symbol="x-thin",
                                   line=dict(width=1, color="white")),
                       hovertemplate="<b>Drone %{text}</b><br>X: %{x} <br>Y: %{y}<br>Orientation: %{customdata[4]}<br>Linear Velocity: %{customdata[6]}<br>Angular Velocity: %{customdata[7]}",
                       name='t=' + str(n))
        ],
            traces=[2],
            name='t=' + str(n)))
    sliders = [dict(steps=[dict(method='animate',
                                args=[['t=' + str(n)],
                                      dict(mode='e',
                                           frame=dict(duration=400, redraw=True),
                                           transition=dict(duration=0))
                                      ],
                                label=f'{n}'
                                ) for n in n_frames],
                    active=1,
                    transition=dict(duration=10),
                    x=0.20,  # slider starting position
                    y=0,
                    currentvalue=dict(font=dict(size=12),
                                      prefix='t = ',
                                      visible=True,
                                      xanchor='center'
                                      ),
                    len=0.80,
                    tickwidth=0,
                    ticklen=5,
                    pad=dict(b=5),
                    font=dict(size=10, color='white'))  # slider length
               ]

    fig.update_layout(updatemenus=get_updatemenus(),
                      sliders=sliders
                      )
    fig.update(frames=frames)
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=-100,
        y1=100,
        line=dict(color="white", width=1)
    )

    fig.add_shape(
        type="line",
        x0=-100,
        x1=100,
        y0=0,
        y1=0,
        line=dict(color="white", width=1)
    )
    return fig

# ------------------------ Reward Trends ---------------------------- #

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




def swarm_scatterplot(df):

    # Basic Figure
    fig = go.Figure(
        data=go.Scattergl(
            x=df[df["episode_id"]==0]["x_coord"],
            y=df[df["episode_id"] == 0]["y_coord"],
            mode="markers",
            marker=dict(symbol="x-thin",
                        color="white"),
        text=df[df['episode_id'] == 0].apply(lambda row: f"x: {row['x_coord']:.2f},<br> y: {row['y_coord']:.2f},<br> orientation: {row['orientation']:.2f},<br> linear vel: {row['linear_velocity']:.2f},<br> angular vel: {row['angular_velocity']:.2f}", axis=1),
        hoverinfo='text'
        )
    )

    # Animation
    frames = []
    for i in range(max(df['episode_id'])):
        frame_data = go.Scatter(
            x=df[df['episode_id'] == i]['x_coord'],
            y=df[df['episode_id'] == i]['y_coord'],
            mode='markers',
            marker=dict(
                symbol='x-thin',  # Keep the marker type consistent for all frames
                color="white",
            ),
            text=df[df['episode_id'] == i].apply(lambda
                                                row: f"x: {row['x_coord']:.2f}, <br> y: {row['y_coord']:.2f}, <br> orientation: {row['orientation']:.2f}, <br> linear vel: {row['linear_velocity']:.2f}, <br> angular vel: {row['angular_velocity']:.2f}",
                                            axis=1),
            hoverinfo='text'
        )
        frames.append(go.Frame(data=[frame_data], name=str(i)))
    fig.frames = frames

    # Animation Controls
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig.update_layout(
        paper_bgcolor='rgb(34,34,34,0)',
        plot_bgcolor='rgb(34,34,34,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        updatemenus=[{
            'x': 0.15,
            'y': -0.1,
        'type': 'buttons',
        'showactive': False,
        'buttons': [
            {
                'label': '▶',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 200, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate'
                }]
            },
            {
                'label': '▐▐',
                'method': 'animate',
                'args': [[None], {
                    'frame': {'duration': 0, 'redraw': False},
                    'mode': 'immediate'
                }]
            }
        ]
    }],
    sliders=[{
        'steps': [{
            'args': [[str(i)], {
                'frame': {'duration': 200, 'redraw': True},
                'mode': 'immediate'
            }],
            'label': str(i),
            'method': 'animate'
        } for i in range(max(df['episode_id']))],
        'currentvalue': {'prefix': 'Episode: '}
    }]
    )
    return fig
