from dash import dcc
from dash import html
from plotly.subplots import make_subplots
import plotly.express as px

def reward_trend_viewer(reward_data):
    # Identify improvement periods for shading
    rew_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["reward"] > reward_data["reward"][i-1]]
    dist_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["distance_reward"] > reward_data["distance_reward"][i-1]]
    act_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["action_penalty"] > reward_data["action_penalty"][i-1]]

    # Create a subplot figure
    # fig = make_subplots(rows=3, cols=1,
    #                     row_heights=[0.6, 0.2, 0.2],
    #                     vertical_spacing=0.1,
    #                     subplot_titles=["Total Rewards (including RAI, if selected)", "Distance Reward", "Action Penalty"])

    # Create and add traces for rewards
    fig = px.line(reward_data, x='episode_id', y='reward', color_discrete_sequence=["white"])
    # for trace in fig1.data:
    #     fig.add_trace(trace, row=1, col=1)
    for period in rew_improvements:
        fig.add_shape(
            type="rect",
            x0=period[0], x1=period[1],
            y0=min(reward_data['reward']), y1=max(reward_data['reward']),
            fillcolor="rgba(255, 255, 255, 0.1)",
            line_width=0,
            row=1, col=1
        )
    #
    # # Create and add traces for distance rewards
    # fig2 = px.line(reward_data, x='episode_id', y='distance_reward', color_discrete_sequence=["white"])
    # for trace in fig2.data:
    #     fig.add_trace(trace, row=2, col=1)
    # for period in dist_improvements:
    #     fig.add_shape(
    #         type="rect",
    #         x0=period[0], x1=period[1],
    #         y0=min(reward_data['distance_reward']), y1=max(reward_data['distance_reward']),
    #         fillcolor="rgba(255, 255, 255, 0.2)",
    #         line_width=0,
    #         row=2, col=1
    #     )
    #
    # # Create and add traces for action penalties
    # fig3 = px.line(reward_data, x='episode_id', y='action_penalty', color_discrete_sequence=["white"])
    # for trace in fig3.data:
    #     fig.add_trace(trace, row=3, col=1)
    # for period in act_improvements:
    #     fig.add_shape(
    #         type="rect",
    #         x0=period[0], x1=period[1],
    #         y0=min(reward_data['action_penalty']), y1=max(reward_data['action_penalty']),
    #         fillcolor="rgba(255, 255, 255, 0.2)",
    #         line_width=0,
    #         row=3, col=1
    #     )

    # Customize layout for the subplot figure
    fig.update_layout(
        paper_bgcolor='rgb(0,0,0,0)',
        plot_bgcolor='rgb(0,0,0,0)',
        font=dict(size=7, color='white'),
        margin=dict(l=20, r=10, t=40, b=20),
        xaxis_title="Episode",
        yaxis_title="Reward"
    )
    fig.update_annotations(font_size=10)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False, zeroline=False)

    return fig


def reward_view():
    div = html.Div(children=[

                dcc.Graph(id="reward_viz", className="graph-object")
    ])
    return div


