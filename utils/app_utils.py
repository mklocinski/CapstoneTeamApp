import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
import os


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

        if d_type == 'int':
            el = html.Div(
                children=[
                    html.P(title, className=class_name),
                    dbc.Input(id=p_id,
                              type=p_type,
                              min=json.loads(row["Valid Values"])[0],
                              max=json.loads(row["Valid Values"])[1],
                              step=row["Increment"],
                              value=row["Default Value"])
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
                                step=row["Increment"])
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'str':
            vals = parameter_values[parameter_values["Parameter"] == title]["Value"]
            el = html.Div(
                 children=[
                    html.P(title, className=class_name),
                    dcc.Dropdown(id=p_id,
                                 options=[{"label": val, "value": val} for val in vals],
                                 value=vals.iloc[0])
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

        elif d_type == 'bool':
            el = html.Div(
                 children=[
                        dbc.Checklist(id=p_id,
                                options=[{"label": title, "value": row["Default Value"]}],
                                 value=[row["Default Value"]],
                                 switch=True)
                 ])
            element_list[phase].append(el)
            value_list[row["Parameter Code"]] = row["Default Value"]

    return {'values': value_list, 'elements': element_list}

