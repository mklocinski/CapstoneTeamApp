import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import base64
import pandas as pd
import numpy as np
from dash import dcc,html


def swarm_scatterplot(df, map_df):

    # Basic Heatmap
    map = map_df.pivot(index="y_coord",
                       columns="x_coord",
                       values="obstacle").to_numpy()
    heatmap = go.Heatmap(z=map, showscale=False)
    heatmap_fig = go.Figure(
        data=[heatmap]
    )
    heatmap_fig.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            visible=False,
            domain=[0, 1]  # Full plot width
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            visible=False,
            domain=[0, 1]  # Full plot height
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # No margins
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot background
    )
    heatmap_img_bytes  = pio.to_image(heatmap_fig, format='png')
    heatmap_img_base64 = base64.b64encode(heatmap_img_bytes).decode('utf-8')
    heatmap_img = f"data:image/png;base64,{heatmap_img_base64}"

    # Basic Scatter
    scatter = go.Scatter(
            x=df[df["episode_id"]==0]["x_coord"],
            y=df[df["episode_id"] == 0]["y_coord"],
            mode="markers",
            marker=dict(color="white"),
        text=df[df['episode_id'] == 0].apply(lambda row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f}", axis=1),
        hoverinfo='text'
        )

    fig = go.Figure(
        data=[scatter],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
            images=[{'source': heatmap_img,  # Using the base64 image
            'xref': 'paper',  # Reference to the entire plot area
            'yref': 'paper',
            'x': 0,  # Positioning the heatmap image in the plot area
            'y': 1,
            'sizex': 1,  # Set the image to cover the whole plot area (adjust as needed)
            'sizey': 1,
            'sizing': 'stretch',
            'layer': 'below'  # Ensure it stays in the background
                     }
            ]
    )
    )

    # Animation
    frames = []
    for i in range(max(df['episode_id'])):
        frame_data = go.Scatter(
            x=df[df['episode_id'] == i]['x_coord'],
            y=df[df['episode_id'] == i]['y_coord'],
            mode="markers",
            marker=dict(color="white"),
            text=df[df['episode_id'] == i].apply(lambda
                                                row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f}",
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
            'direction': "left",
            'pad': {"r": 0, "t": 0},
            'xanchor': "right",
            'yanchor': "top",
            'font': dict(family="Arial", size=12, color="black"),
            'bgcolor': "#3b3b3b",
            'bordercolor': "gray",
            'borderwidth': 1,
        'type': 'buttons',
        'showactive': False,
        'buttons': [
            {
                'label': '▶',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 100, 'redraw': False},
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
        'currentvalue': {'prefix': 'Episode: '},
        'x': 0.20,
        'y': 0
    }
    ]
    )
    return fig

def swarm_view(df, map_df):
    div = html.Div(children=[
        dcc.Loading(
            id="loading-swarm-movement-plot",
            children=[
                dcc.Graph(figure=swarm_scatterplot(df, map_df), className="graph-object")
    ])])
    return div
