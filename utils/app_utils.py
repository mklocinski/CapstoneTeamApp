import pandas as pd
import numpy as np
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

def map_param_conversion(map_params):
    converted_dict = {}
    for key, values in map_params.items():
        if key not in converted_dict:
            converted_dict[key] = {}
        for param, val in map_params[key].items():
            if key == "target":
                converted_dict[key] = values
            elif "number_of_" in param:
                converted_dict[key]["count"] = val
            elif "random_" in param:
                converted_dict[key]["random"] = val
            elif "_midpoint" in param:
                converted_dict[key]["positions"] = [val]
            elif "_size" in param:
                converted_dict[key]["sizes"] = [val]
            elif "_damage" in param:
                converted_dict[key]["damage"] = val
    return converted_dict



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
        if not pd.isnull(row["Parameter Group"]):
            p_id = {"type": row["Parameter Type"], "index": row["Parameter Code"], "category": row["Parameter Group"]}
        else:
            p_id = {"type": row["Parameter Type"], "index": row["Parameter Code"]}

        p_type = row["Input Type"]
        d_type = row["Data Type"]
        phase = row["Phase"]
        disabled = True if row["Disabled"] == "TRUE" else False

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
            if not pd.isnull(row["Parameter Group"]):
                if row["Parameter Group"] not in value_list:
                    value_list[row["Parameter Group"]] = {}
                value_list[row["Parameter Group"]][row["Parameter Code"]] = row["Default Value"]
            else:
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
            if not pd.isnull(row["Parameter Group"]):
                if row["Parameter Group"] not in value_list:
                    value_list[row["Parameter Group"]] = {}
                value_list[row["Parameter Group"]][row["Parameter Code"]] = row["Default Value"]
            else:
                value_list[row["Parameter Code"]] = row["Default Value"]
        elif d_type == 'str':
            vals = row["Valid Values"]
            el = html.Div(
                 children=[
                    html.P(title, className=class_name),
                    dcc.Dropdown(id=p_id,
                                 options=[{"label": val, "value": val} for val in vals],
                                 value=vals.iloc[0] if "[" in vals else vals,
                              disabled=disabled)
                 ])
            element_list[phase].append(el)
            if not pd.isnull(row["Parameter Group"]):
                if row["Parameter Group"] not in value_list:
                    value_list[row["Parameter Group"]] = {}
                value_list[row["Parameter Group"]][row["Parameter Code"]] = row["Default Value"]
            else:
                value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'bool':
            if disabled:
                opts = [{"label": title, "value": row["Default Value"], 'disabled':True}]
            else:
                opts = [{"label": title, "value": row["Default Value"]}]
            el = html.Div(
                 children=[
                        dbc.Checklist(id=p_id,
                                options=opts,
                                 value=[row["Default Value"]],
                                 switch=True,
                              )
                 ])
            element_list[phase].append(el)
            if not pd.isnull(row["Parameter Group"]):
                if row["Parameter Group"] not in value_list:
                    value_list[row["Parameter Group"]] = {}
                value_list[row["Parameter Group"]][row["Parameter Code"]] = row["Default Value"]
            else:
                value_list[row["Parameter Code"]] = row["Default Value"]
    vals = value_list if row["Parameter Type"] != "Map" else map_param_conversion(value_list)
    print(vals)
    return {'values': vals, 'elements': element_list}

