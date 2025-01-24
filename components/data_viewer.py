# import plotly.express as px
# import pandas as pd
# from dash import dcc, dash_table
# from utils import make_map, visualizations as viz
#
# # ------------------------------------------------------------------ #
# # ---------------------- Read in Data ------------------------------ #
# # ------------------------------------------------------------------ #
# data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1sFl9BFVxdnqn_vFexMKbebO6s4bSG_wtBrM_vSvTR6I/export?format=csv",
#                    index_col=0)
# reward_data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1Wj3qF2QS9H6228AiqBEdZcWD7glf1_rmo0jSqsnu8i0/export?format=csv",
#                           index_col=0)
# # ------------------------------------------------------------------ #
# # ------------------------ Set Up Map ------------------------------ #
# # ------------------------------------------------------------------ #
# amap = make_map.Map()
# amap.initialize(10)
# plot_range = [i for i in range(amap.axis_values[0], amap.axis_values[1])]
#
# # ------------------------------------------------------------------ #
# # ------------------------ Set Up Plots ---------------------------- #
# # ------------------------------------------------------------------ #
# basic_swarm_view = viz.basic_swarm_viewer(data)
# fleet_map = viz.swarm_scatterplot(data)
#
# reward_trend = viz.reward_trend_viewer(reward_data)
#
# details = dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns],
#                             style_table={'backgroundColor':'rgb(0,0,0,0)',
#                                          'overflowX': 'auto'},
#                             fixed_rows={'headers': True},
#                                 style_cell={
#                                     'font_size': '8px',
#                                     'color':'#adadad',
#                                     'padding': '2px',
#                                     'virtualization':'True',
#                                     'backgroundColor':'rgb(0,0,0,0)'
#                                 },
#                                 filter_action='native',
#                                 sort_action='native',
#                                style_as_list_view=True)
#
# # ------------------------------------------------------------------ #
# # -------------------- Create Dash Components ---------------------- #
# # ------------------------------------------------------------------ #
# swarm_view = dcc.Graph(figure=fleet_map, className="graph-object")
# reward_view = dcc.Graph(figure=reward_trend, className="graph-object")
