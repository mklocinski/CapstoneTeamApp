from dash import dcc
from dash import html
from plotly.subplots import make_subplots
import plotly.express as px

def reward_trend_viewer(reward_data):
    reward_data = reward_data.sort_values(by='episode_id')
    # Identify improvement periods for shading
    #rew_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["reward"] > reward_data["reward"][i-1]]
    # dist_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["direction_reward"] > reward_data["direction_reward"][i-1]]
    # target_dist_improvements = [[reward_data["episode_id"][i-1], r["episode_id"]] for i, r in reward_data.iterrows() if i > 0 and r["target_distance_reward"] > reward_data["target_distance_reward"][i-1]]

    # Create a subplot figure
    fig = make_subplots(rows=2, cols=1,
                        row_heights=[0.6, 0.4],
                        vertical_spacing=0.1,
                        subplot_titles=["Total Rewards", "Collisions"])

    # Create and add traces for rewards
    fig1 = px.line(reward_data, x='episode_id', y='reward', color_discrete_sequence=["white"])
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    # for period in rew_improvements:
    #     fig.add_shape(
    #             type="rect",
    #             x0=period[0], x1=period[1],
    #             y0=min(reward_data['reward']), y1=max(reward_data['reward']),
    #             fillcolor="rgba(255, 255, 255, 0.2)",
    #             line_width=0,
    #             row=1, col=1
    #         )

    # Create and add traces for collisions
    fig2 = px.line(reward_data, x='episode_id', y='all_collisions', color_discrete_sequence=["white"])
    for trace in fig2.data:
        fig.add_trace(trace, row=2, col=1)

    # Create and add traces for direction rewards
    # fig3 = px.line(reward_data, x='episode_id', y='direction_reward', color_discrete_sequence=["white"])
    # for trace in fig3.data:
    #     fig.add_trace(trace, row=3, col=1)
    # for period in dist_improvements:
    #     fig.add_shape(
    #         type="rect",
    #         x0=period[0], x1=period[1],
    #         y0=min(reward_data['direction_reward']), y1=max(reward_data['direction_reward']),
    #         fillcolor="rgba(255, 255, 255, 0.2)",
    #         line_width=0,
    #         row=3, col=1
    #     )
    #
    # # Create and add traces for drone-target distance
    # fig4 = px.line(reward_data, x='episode_id', y='target_distance_reward', color_discrete_sequence=["white"])
    # for trace in fig4.data:
    #     fig.add_trace(trace, row=4, col=1)
    # for period in target_dist_improvements:
    #     fig.add_shape(
    #         type="rect",
    #         x0=period[0], x1=period[1],
    #         y0=min(reward_data['target_distance_reward']), y1=max(reward_data['target_distance_reward']),
    #         fillcolor="rgba(255, 255, 255, 0.2)",
    #         line_width=0,
    #         row=4, col=1
    #     )

    # Customize layout for the subplot figure
    fig.update_layout(
        paper_bgcolor='rgb(0,0,0,0)',
        plot_bgcolor='rgb(0,0,0,0)',
        font=dict(size=14, color='white'),
        margin=dict(l=20, r=10, t=40, b=20),
        height=1000,
        #xaxis_title="Episode",
        #yaxis_title="Reward",
    )
    fig.update_annotations(font_size=10)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False, zeroline=False)

    return fig


def reward_view():
    div = html.Div(children=[

                dcc.Graph(id="reward_viz", className="graph-object", style={'display': 'none'})
    ])
    return div


