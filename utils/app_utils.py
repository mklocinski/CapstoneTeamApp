import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
import os

data_dict_path = os.path.join("assets", "DRL Data Dictionary.xlsx")
tbl_data = pd.read_excel(data_dict_path, sheet_name=None)

def reorder_tbl(tbl_name):
    right_order = [col for col in tbl_data[tbl_name]["DB Label"]]
    return right_order

def get_tbl_col_def(tbl_name):
    tooltips = {r["DB Label"]:r["Description"] for i, r in tbl_data[tbl_name].iterrows()}
    return tooltips


def dt_data_type(col_name):
    prefix = col_name[:4]
    type_map = {
        "cint": "numeric",
        "cflt": "numeric",
        "cstr": "text",
        "cbln": "text",
        "cdtm": "datetime",
        "id": "text"}

    return type_map[prefix]


param_path = os.path.join("assets", "XRAI System - User Parameters.xlsx")
parameters = pd.read_excel(param_path,  sheet_name="Parameters")
parameter_values = pd.read_excel(param_path, sheet_name="Parameter Values")

def create_user_inputs(param_type,
                       parameter_df=parameters,
                       parameter_values=parameter_values,
                       title_class="p_dark"):
    df = parameter_df[parameter_df["Parameter Type"] == param_type]
    element_list = {phase: [] for phase in df["Phase"].unique()}
    value_list = {}

    for i, row in df.iterrows():
        title = row["Parameter"]
        class_name = title_class
        p_id = {"type": "param_input", "index": row["Parameter Code"]}
        p_type = row["Input Type"]
        d_type = row["Data Type"]
        phase = row["Phase"]
        disabled = row["Disabled"]

        if d_type == 'int':
            el = html.Div(
                children=[
                    html.P(title, className=class_name),
                    dbc.Input(id=p_id,
                              type=p_type,
                              min=json.loads(row["Valid Values"])[0],
                              max=json.loads(row["Valid Values"])[1],
                              step=row["Increment"],
                              value=row["Default Value"],
                              disabled=disabled)
                ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'flt':
            el = html.Div(
                 children=[
                     html.P(title, className=class_name),
                     dcc.Slider(id=p_id,
                                value=row["Default Value"],
                                min=json.loads(row["Valid Values"])[0],
                                max=json.loads(row["Valid Values"])[1],
                                step=row["Increment"],
                              disabled=disabled)
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'str':
            vals = row["Valid Values"]
            print(vals)
            el = html.Div(
                 children=[
                    html.P(title, className=class_name),
                    dcc.Dropdown(id=p_id,
                                 options=[{"label": val, "value": val} for val in vals],
                                 value=vals.iloc[0] if "[" in vals else vals,
                              disabled=disabled)
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'bool':
            if row["Disabled"]:
                opts = [{"label": title, "value": row["Default Value"], 'disabled':True}]
            else:
                opts = [{"label": title, "value": row["Default Value"]}]
            el = html.Div(
                 children=[
                        dbc.Checklist(id=p_id['index'],
                                options=opts,
                                 value=[row["Default Value"]],
                                 switch=True,
                              )
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

    return {'values': value_list, 'elements': element_list}

