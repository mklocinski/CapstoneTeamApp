import plotly.express as px
import pandas as pd
from dash import dcc, dash_table
from utils import make_map, visualizations as viz

# ------------------------------------------------------------------ #
# ---------------------- Read in Data ------------------------------ #
# ------------------------------------------------------------------ #
data = pd.read_csv(r'pages\tbl_local_state.csv')
reward_data = pd.read_csv(r'pages\tbl_rewards.csv')
print(data.head(40))
# ------------------------------------------------------------------ #
# ------------------------ Set Up Map ------------------------------ #
# ------------------------------------------------------------------ #
amap = make_map.Map()
amap.initialize(10)
plot_range = [i for i in range(amap.axis_values[0], amap.axis_values[1])]

# ------------------------------------------------------------------ #
# ------------------------ Set Up Plots ---------------------------- #
# ------------------------------------------------------------------ #
fleet_map = viz.create_fleet_viewer(data,
                        amap.position_matrix,
                        plot_range)

reward_trend = px.line(reward_data, x='episode_id', y='reward')
reward_trend.update_layout(yaxis_range=[min(reward_data['reward']), max(reward_data['reward'])],
                      xaxis_range=[0, max(reward_data['episode_id'])],
                      paper_bgcolor='rgb(0,0,0,0)',
                    plot_bgcolor='rgb(0,0,0,0)',
                    margin=dict(l=20, r=10, t=20, b=20),
                    autosize = False,
                    #width = 600,
                     height = 200,
                           yaxis_title=None,
                           xaxis_title=None,
                           xaxis=dict(title_font=dict(size=10),
                                      showgrid=False),
                           yaxis=dict(title_font=dict(size=10),
                                      showgrid=False),
                           font=dict(size=10, color='white'),
                           title='Reward Trends'
                           )

details = dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns],
                            style_table={'backgroundColor':'rgb(0,0,0,0)',
                                         'overflowX': 'auto',
                                         'margin': '10px',
                                         'height':'175px'},
                            fixed_rows={'headers': True},
                                style_cell={
                                    'font_size': '8px',
                                    'color':'#adadad',
                                    'padding': '2px',
                                    'virtualization':'True',
                                    'backgroundColor':'rgb(0,0,0,0)'
                                },
                                filter_action='native',
                                sort_action='native',
                               style_as_list_view=True)

# ------------------------------------------------------------------ #
# -------------------- Create Dash Components ---------------------- #
# ------------------------------------------------------------------ #
fleet_view = dcc.Graph(figure=fleet_map)
reward_view = dcc.Graph(figure=reward_trend)
