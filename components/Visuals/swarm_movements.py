import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import base64
import pandas as pd
import numpy as np
from dash import dcc,html


def swarm_scatterplot(df, map_df):

    # Basic Heatmap
    map = map_df.groupby(["y_coord", "x_coord"], as_index=False).agg({"obstacle_id": "nunique"})
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
            marker=dict(color="white", symbol="arrow-wide"),
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


def swarm_scatterplot_with_obstacles(df, obstacles):
    def get_marker_line(df_subset):
        return dict(
            color=["red" if collision > 0 else "black" for collision in df_subset['drone_collisions']],
            width=2
        )

    # Prepare obstacle colors and dynamic opacity for obstacles
    obstacle_colors = ["rgb" + str(col.replace("[", "(").replace("]", ")")) for col in obstacles['obstacle_color']]
    obstacle_opacity = [
        0.0 if (row["obstacle"] == "fires" and row["point_type"] == "interior" or row["point_type"] == "midpoint") else 0.8
        for i, row in obstacles.iterrows()
    ]

    # Static obstacle trace
    obstacle_trace = go.Scatter(
        x=obstacles['x_coord'],
        y=obstacles['y_coord'],
        mode="markers",
        marker=dict(size=8, color=obstacle_colors, opacity=obstacle_opacity),
        name="Obstacles",
        hoverinfo='text',
        text=obstacles.apply(lambda row: f"<b>Obstacle ID</b>: {row['obstacle_id']}<br>"
                                         f"<b>Obstacle Type</b>: {row['obstacle']}<br>"
                                         f"<b>X-Coord</b>: {row['x_coord']}<br>"
                                         f"<b>Y-Coord</b>: {row['y_coord']}<br>"
                                         f"<b>Obstacle Risk</b>: {row['obstacle_risk']}", axis=1)
    )

    # Initial frame for drones
    initial_frame_data = go.Scatter(
        x=df[df["episode_id"] == 0]["x_coord"],
        y=df[df["episode_id"] == 0]["y_coord"],
        mode="markers",
        marker=dict(color="white", symbol="arrow-wide", size=20, line=get_marker_line(df[df["episode_id"] == 0])),
        text=df[df['episode_id'] == 0].apply(lambda
                                                 row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f},<br> <b>Improvement Multiplier</b>: {row['improvement_multiplier']:.2f}",
                                             axis=1),
        hoverinfo='text',
        name="Drones"
    )

    # Define figure layout with the obstacles trace
    fig = go.Figure(
        data=[obstacle_trace, initial_frame_data],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
        )
    )

    # Animation frames for each episode
    frames = []
    max_episode = df['episode_id'].max()
    for i in range(max_episode + 1):
        frame_df = df[df["episode_id"] == i]
        frame_data = go.Scatter(
            x=frame_df["x_coord"],
            y=frame_df["y_coord"],
            mode="markers",
            marker=dict(
                color="white",
                symbol="arrow-wide",
                size=20,
                line=get_marker_line(frame_df)  # Adjust line colors dynamically
            ),
            text=frame_df.apply(lambda
                                    row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f},<br> <b>Improvement Multiplier</b>: {row['improvement_multiplier']:.2f}",
                                axis=1),
            hoverinfo='text',
            name="Drones"
        )
        frames.append(go.Frame(data=[obstacle_trace, frame_data], name=str(i)))
    fig.frames = frames
    # Custom animation controls
    fig.update_layout(
        hoverdistance=10,

        showlegend=False,
        updatemenus=[{
            'x': 0.15,
            'y': -0.1,
            'direction': "left",
            'pad': {"r": 0, "t": 0},
            'xanchor': "right",
            'yanchor': "top",
            'font': dict(family="Arial", size=12, color="white"),
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
            'tickcolor': "white",  # Tick mark color
            'font': {'color':"white", 'size':8},
            'steps': [{
                'args': [[str(i)], {
                    'frame': {'duration': 200, 'redraw': True},
                    'mode': 'immediate'
                }],
                'label': str(i),
                'method': 'animate'
            } for i in range(max_episode + 1)],
            'currentvalue': {'prefix': 'Episode: ',
                "font": {"size": 10, "color": "white"}},
            'x': 0.20,
            'y': 0
        }]
    )

    return fig


def static_scatterplot(df, obstacles):
    # Prepare obstacle colors
    obstacle_colors = ["rgb" + str(col.replace("[", "(").replace("]", ")")) for col in obstacles['obstacle_color']]

    obstacle_opacity = [
        0.0 if (row["obstacle"] == "fires" and row["point_type"] == "interior" or row["point_type"] == "midpoint") else 0.8
        for i, row in obstacles.iterrows()
    ]
    # Static obstacle trace
    obstacle_trace = go.Scatter(
        x=obstacles['x_coord'],
        y=obstacles['y_coord'],
        mode="markers",
        marker=dict(size=8, color=obstacle_colors, opacity=obstacle_opacity),
        name="Obstacles",
        hoverinfo='text',
        text=obstacles.apply(lambda row: f"<b>Obstacle ID</b>: {row['obstacle_id']}<br>"
                                         f"<b>Obstacle Type</b>: {row['obstacle']}<br>"
                                         f"<b>X-Coord</b>: {row['x_coord']}<br>"
                                         f"<b>Y-Coord</b>: {row['y_coord']}<br>"
                                         f"<b>Obstacle Risk</b>: {row['obstacle_risk']}", axis=1)
    )

    # Function to dynamically set marker borders
    def get_marker_line(df_subset):
        return dict(
            color=["red" if collision > 0 else "black" for collision in df_subset['drone_collisions']],
            width=2  # Border width
        )

    # Display drone positions for the final episode
    final_episode = df['episode_id'].max()
    final_df = df[df["episode_id"] == final_episode]

    drone_trace = go.Scatter(
        x=final_df["x_coord"],
        y=final_df["y_coord"],
        mode="markers",
        marker=dict(
            color="white",
            symbol="arrow-wide",
            size=20,
            line=get_marker_line(final_df)  # Adjust line color dynamically
        ),
        text=final_df.apply(lambda
                                row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f},<br> <b>Improvement Multiplier</b>: {row['improvement_multiplier']:.2f}",
                            axis=1),
        hoverinfo='text',
        name="Drones"
    )

    # Create the figure
    fig = go.Figure(
        data=[obstacle_trace, drone_trace],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
            hoverdistance=10,
            showlegend=False
        )
    )

    return fig


def swarm_scatterplot_with_obstacles2(df, obstacle_df):
    # Initialize figure
    fig = go.Figure()

    # Add obstacle shapes
    for obstacle_id, group in obstacle_df.groupby("obstacle_id"):
        # Get color for this obstacle (converting from list format)
        color = obstacle_df.loc[obstacle_df['obstacle_id'] == obstacle_id, 'obstacle_color'].iloc[0]
        color_rgb = "rgb" + color.replace("[", "(").replace("]", ")")

        # Get coordinates for the current obstacle
        x_coords = group['x_coord'].tolist()
        y_coords = group['y_coord'].tolist()

        # Create the shape as a closed polygon
        fig.add_shape(
            type="path",
            path=f'M {x_coords[0]},{y_coords[0]} ' + ' '.join(f'L {x},{y}' for x, y in zip(x_coords, y_coords)) + ' Z',
            fillcolor=color_rgb,
            opacity=0.5,
            line=dict(width=0)
        )

    # Add drones as animated points
    max_episode = df['episode_id'].max()
    frames = []
    for i in range(max_episode + 1):
        frame_data = go.Scatter(
            x=df[df["episode_id"] == i]["x_coord"],
            y=df[df["episode_id"] == i]["y_coord"],
            mode="markers",
            marker=dict(color="white", symbol="arrow-wide", size=20),
            text=df[df['episode_id'] == i].apply(lambda row: f"<b>Drone ID</b>: {row['drone_id']}", axis=1),
            hoverinfo='text',
            name="Drones"
        )
        frames.append(go.Frame(data=[frame_data], name=str(i)))

    fig.frames = frames
    fig.update_layout(
        sliders=[{
            'steps': [{'args': [[str(i)], {'frame': {'duration': 200, 'redraw': True}, 'mode': 'immediate'}],
                       'label': str(i), 'method': 'animate'} for i in range(max_episode + 1)],
            'currentvalue': {'prefix': 'Episode: '},
        }],
        updatemenus=[{'type': 'buttons', 'showactive': False,
                      'buttons': [{'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 100}}]},
                                  {'label': 'Pause', 'method': 'animate', 'args': [[None], {'mode': 'immediate'}]}]}]
    )

    return fig

def swarm_view(df, map_df):
    div = html.Div(children=[
        dcc.Loading(
            id="loading-swarm-movement-plot",
            children=[
                dcc.Graph(figure=swarm_scatterplot_with_obstacles(df, map_df), className="graph-object")
    ])])
    return div


def no_playback(df, map_df):
    div = html.Div(children=[
        dcc.Loading(
            id="static-swarm-movement-plot",
            children=[
                dcc.Graph(figure=static_scatterplot(df, map_df), className="graph-object")
    ])])
    return div

def no_playback_view():
    div = html.Div(children=[

                dcc.Graph(id="static-swarm-movement-plot", className="graph-object", style={'display':'none'})
    ])
    return div