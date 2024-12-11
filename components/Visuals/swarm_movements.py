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

    # Create the figure
    fig = go.Figure(layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
        ))
    print("Swarm Visualization")
    trace_list = []

    print("Swarm Visualization")
    # Plot static obstacles
    if obstacles is not None and not obstacles.empty and isinstance(obstacles, pd.DataFrame):
        obstacles = obstacles.drop('', axis=1).drop_duplicates()
        for _, row in obstacles.iterrows():
            color = f"rgb{row['obstacle_color'].replace('[', '(').replace(']', ')')}"
            print(f"Processed Color: {color} for Obstacle: {row['obstacle_shape']}")
            shape_type = row['obstacle_shape']
            x_center = row['midpoint_x_coord']
            y_center = row['midpoint_y_coord']


            if shape_type == 'point':
                trace_list.append(
                    go.Scatter(
                        x=[x_center],
                        y=[y_center],
                        mode="markers",
                        marker=dict(color="white", symbol="x", size=20),
                        name=row["obstacle"].title(),
                    )
                )
            elif shape_type == 'rect':
                bottom_left = eval(row['bottom_left'])
                top_right = eval(row['top_right'])

                x0, y0 = bottom_left
                x1, y1 = top_right

                if row["obstacle"] == "no-fly":
                    trace_list.append(
                        go.Scatter(
                            x=[x0, x1, x1, x0, x0],
                            y=[y0, y0, y1, y1, y0],
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.1,
                            name=row["obstacle"].title(),
                        )
                    )
                else:
                    trace_list.append(
                        go.Scatter(
                            x=[x0, x1, x1, x0, x0],
                            y=[y0, y0, y1, y1, y0],
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.8,
                            name = row["obstacle"].title(),
                        )
                    )

            elif shape_type == 'circle':
                top_right = eval(row['top_right'])
                bottom_left = eval(row['bottom_left'])
                x0, y0 = bottom_left
                x1, y1 = top_right

                radius = (x1 - x0)/2

                # Circle traces need to be approximated using Scatter
                circle_x = [x_center + radius * np.cos(theta) for theta in np.linspace(0, 2 * np.pi, 100)]
                circle_y = [y_center + radius * np.sin(theta) for theta in np.linspace(0, 2 * np.pi, 100)]

                if row["obstacle"] == "fires":
                    trace_list.append(
                        go.Scatter(
                            x=circle_x,
                            y=circle_y,
                            line=dict(color=color, width=2, dash="dash"),
                            mode="lines",
                            opacity=0.8,
                            name=row["obstacle"].title(),
                        )
                    )
                else:
                    trace_list.append(
                        go.Scatter(
                            x=circle_x,
                            y=circle_y,
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.8,
                            name=row["obstacle"].title(),
                        )
                    )


            elif shape_type == 'polygon':
                bottom_left = eval(row['bottom_left'])
                bottom_right = eval(row['bottom_right'])
                mid_top = eval(row['mid_top'])

                x_coords = [bottom_left[0], bottom_right[0], mid_top[0], bottom_left[0]]
                y_coords = [bottom_left[1], bottom_right[1], mid_top[1], bottom_left[1]]

                trace_list.append(
                    go.Scatter(
                        x=x_coords,
                        y=y_coords,
                        fill="toself",
                        fillcolor=color,
                        line=dict(color=color, width=2),
                        mode="lines",
                        opacity=0.8,
                        name=row["obstacle"].title(),
                    )
                )

    # Add initial drone positions
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
        data=[*trace_list, initial_frame_data],  # Unpack trace_list and add initial drone positions
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
            font_color="white",
            font_size=14
        )
    )
    # Add animation frames
    frames = []
    max_episode = df['episode_id'].max()
    for i in range(max_episode + 1):
        frame_df = df[df["episode_id"] == i]
        frame_data = go.Scatter(
            x=frame_df["x_coord"],
            y=frame_df["y_coord"],
            mode="markers",
            marker=dict(color="white",
                        symbol="arrow-wide",
                        size=20,
                        line=get_marker_line(frame_df)
                        ),
            text=frame_df.apply(lambda
                                    row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f},<br> <b>Improvement Multiplier</b>: {row['improvement_multiplier']:.2f}",
                                axis=1),
            hoverinfo='text',
            name="Drones"
        )
        frames.append(go.Frame(data=[*trace_list, frame_data], name=str(i)))

    fig.frames = frames

    # Add play/pause controls
    fig.update_layout(
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
                {'label': '▶', 'method': 'animate', 'args': [None, {'frame': {'duration': 200, 'redraw': True}}]},
                {'label': '▐▐', 'method': 'animate', 'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate'
                    }]}  # Fix
            ]
        }],
        sliders=[{
            'tickcolor': "white",  # Tick mark color
            'font': {'color': "white", 'size': 8},
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
    def get_marker_line(df_subset):
        return dict(
            color=["red" if collision > 0 else "black" for collision in df_subset['drone_collisions']],
            width=2
        )

    # Create the figure
    fig = go.Figure()
    print("Swarm Visualization")
    trace_list = []
    # Plot static obstacles
    if obstacles is not None and not obstacles.empty and isinstance(obstacles, pd.DataFrame):
        obstacles = obstacles.drop('', axis=1).drop_duplicates()
        for _, row in obstacles.iterrows():
            color = f"rgb{row['obstacle_color'].replace('[', '(').replace(']', ')')}"
            print(f"Processed Color: {color} for Obstacle: {row['obstacle_shape']}")
            shape_type = row['obstacle_shape']
            x_center = row['midpoint_x_coord']
            y_center = row['midpoint_y_coord']


            if shape_type == 'point':
                trace_list.append(
                    go.Scatter(
                        x=[x_center],
                        y=[y_center],
                        mode="markers",
                        marker=dict(color="white", symbol="x", size=20),
                        name=row["obstacle"].title(),
                    )
                )
            elif shape_type == 'rect':
                bottom_left = eval(row['bottom_left'])
                top_right = eval(row['top_right'])

                x0, y0 = bottom_left
                x1, y1 = top_right

                if row["obstacle"] == "no-fly":
                    trace_list.append(
                        go.Scatter(
                            x=[x0, x1, x1, x0, x0],
                            y=[y0, y0, y1, y1, y0],
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.1,
                            name=row["obstacle"].title(),
                        )
                    )
                else:
                    trace_list.append(
                        go.Scatter(
                            x=[x0, x1, x1, x0, x0],
                            y=[y0, y0, y1, y1, y0],
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.8,
                            name=row["obstacle"].title(),
                        )
                    )

            elif shape_type == 'circle':
                top_right = eval(row['top_right'])
                bottom_left = eval(row['bottom_left'])
                x0, y0 = bottom_left
                x1, y1 = top_right

                radius = (x1 - x0)/2

                # Circle traces need to be approximated using Scatter
                circle_x = [x_center + radius * np.cos(theta) for theta in np.linspace(0, 2 * np.pi, 100)]
                circle_y = [y_center + radius * np.sin(theta) for theta in np.linspace(0, 2 * np.pi, 100)]

                if row["obstacle"] == "fires":
                    trace_list.append(
                        go.Scatter(
                            x=circle_x,
                            y=circle_y,
                            line=dict(color=color, width=2, dash="dash"),
                            mode="lines",
                            opacity=0.8,
                            name=row["obstacle"].title(),
                            showlegend=True,
                        )
                    )
                else:
                    trace_list.append(
                        go.Scatter(
                            x=circle_x,
                            y=circle_y,
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color, width=2),
                            mode="lines",
                            opacity=0.8,
                            name=row["obstacle"].title(),
                            showlegend=True,
                        )
                    )


            elif shape_type == 'polygon':
                bottom_left = eval(row['bottom_left'])
                bottom_right = eval(row['bottom_right'])
                mid_top = eval(row['mid_top'])

                x_coords = [bottom_left[0], bottom_right[0], mid_top[0], bottom_left[0]]
                y_coords = [bottom_left[1], bottom_right[1], mid_top[1], bottom_left[1]]

                trace_list.append(
                    go.Scatter(
                        x=x_coords,
                        y=y_coords,
                        fill="toself",
                        fillcolor=color,
                        line=dict(color=color, width=2),
                        mode="lines",
                        opacity=0.8,
                        name=row["obstacle"].title(),
                        showlegend=True,
                    )
                )
    # Plot drones for the final episode
    final_episode = df['episode_id'].max()
    final_df = df[df["episode_id"] == final_episode]

    drone_trace = go.Scatter(
        x=final_df["x_coord"],
        y=final_df["y_coord"],
        mode="markers",
        marker=dict(color="white", symbol="arrow-wide", size=20, line=get_marker_line(final_df)),
        hoverinfo='text',
        text=final_df.apply(lambda
                                                 row: f"<b>Drone ID</b>: {round(row['drone_id']):.2f},<br> <b>X</b>: {row['x_coord']:.2f},<br> <b>Y</b>: {row['y_coord']:.2f},<br> <b>Orientation</b>: {row['orientation']:.2f},<br> <b>Linear Velocity</b>: {row['linear_velocity']:.2f},<br> <b>Angular Velocity</b>: {row['angular_velocity']:.2f},<br> <b>Improvement Multiplier</b>: {row['improvement_multiplier']:.2f}",
                                             axis=1),
        name="Drones",
        showlegend=True,
    )
    # Define figure layout with the obstacles trace
    fig = go.Figure(
        data=[*trace_list, drone_trace],  # Unpack trace_list and add initial drone positions
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(scaleanchor='y', constrain='domain', visible=False),
            yaxis=dict(scaleanchor='x', constrain='domain', visible=False),
            font_color="white",
            font_size=14
        )
    )

    return fig


def swarm_scatterplot_with_obstacles2(df, obstacle_df):
    # Initialize figure
    fig = go.Figure()

    # Add obstacle shape
    obstacle_df.drop('id', axis=1, inplace=True)
    obstacle_df = obstacle_df.drop_duplicates()


    for obstacle_id, group in obstacle_df.groupby("obstacle_id"):
        obstacle_df = obstacle_df.drop('id', axis=1).drop_duplicates()
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