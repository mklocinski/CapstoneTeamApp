# import pandas as pd
# from dash import dcc, dash_table, html
# from scipy.stats import zscore
# import numpy as np
#
# data = pd.read_csv("C:/Users/mkloc/Downloads/table_data (2).csv")
# sort = data.sort_values(by=['Drone Id', 'Episode Id'])
# print(data["Drone Collisions"])
# def health_indicator(d_id, z_score, collisions):
#     fid= str(int(d_id))
#     space= " ".join(np.repeat(" ", 5-len(fid)))
#     identifier = space+fid
#     if z_score > 2.:
#         return str("🔴"+identifier)
#     if z_score > 1.:
#         return str("🟠"+identifier)
#     if z_score >= 0.:
#         if collisions > 0.:
#             return str("🟡"+identifier)
#         else:
#             return str(str(d_id))
#     else:
#         return str("🟢"+identifier)
#
#
#
# aggregate = sort.groupby('Drone Id').agg(
#     most_recent_episode=('Episode Id', 'max'),
#     total_collisions=('Drone Collisions', 'sum')).reset_index()
#
# sort['Change in Linear Velocity'] = sort.groupby('Drone Id')['Linear Velocity'].diff().fillna(0)
# sort['Change in Angular Velocity'] = sort.groupby('Drone Id')['Angular Velocity'].diff().fillna(0)
#
# velocity_changes = sort.groupby('Drone Id').tail(1)[
#     ['Drone Id', 'Change in Linear Velocity', 'Change in Angular Velocity']
# ]
#
# result_df = pd.merge(aggregate, velocity_changes, on='Drone Id').sort_values(by="total_collisions", ascending=False)
# result_df['damage_zscore'] = zscore(result_df["total_collisions"].to_numpy())
# result_df['test'] = [1 if i > 2 else 0 for i in result_df['damage_zscore']]
#
# result_df["Drone Id"] = [health_indicator(row["Drone Id"], row["damage_zscore"], row["total_collisions"]) for i, row in result_df.iterrows()]
#
# df = result_df.astype('str').to_dict('records')
# table = dcc.Loading(
#         id='loading-2',
#         type='default',
#         children=[
#             dash_table.DataTable(
#                 id='test_table',
#                 columns=[{"name": i, "id": i} for i in result_df.columns],
#                 data=df,
#                 page_size=150,  # Number of rows per page
#                 style_table={'height': '400px', 'overflowY': 'auto'},
#                 style_header={'backgroundColor': '#000000', 'color':'white', 'fontSize':'0.5em'},
#                 style_cell={'backgroundColor': '#454545', 'color':'white',
#                             'fontSize':'0.75em', 'border': '0px #454545'},
#                 style_as_list_view=True,
#             )
#         ]
#     )
# def health_viewer():
#     return html.Div(children=[
#             table])