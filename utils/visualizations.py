import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc
from plotly.subplots import make_subplots

# ------------------------------------------------------------------ #
# ---------------------- General Functions ------------------------- #
# ------------------------------------------------------------------ #

def get_updatemenus(x_pos=0.0, fr_duration=50):
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
                 pad={"r": -100, "t": 0},
                 xanchor="right",
                 yanchor="top",
                 font=dict(family="Arial", size=12, color="black"),
                 bgcolor="lightgray",
                 bordercolor="gray",
                 borderwidth=1
                 )
            ]


# ------------------------------------------------------------------ #
# ------------------------ Fleet Viewer ---------------------------- #
# ------------------------------------------------------------------ #

# ------------------------ Fleet Viewer ---------------------------- #
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
                     go.Scatter(x=[drone_data['x_coord'].iloc[[0, 19]]], y=[drone_data['y_coord'].iloc[[0, 19]]],
                                mode="markers",
                                text=[drone_data['drone_id'].iloc[[0, 19]]],
                                marker=dict(size=8, symbol="x-thin",
                                            line=dict(width=2, color="white")),
                                name='scatter')])
    fig.update_layout(yaxis_range=[-100, 100],
                      xaxis_range=[-100, 100],
                      autosize=True,
                      width=500,
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