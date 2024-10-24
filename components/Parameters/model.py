from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from utils import text


model_params_submit_button = dbc.Button(
                        children=["Submit"],
                        id="tools-menu-submit-model-button",
                        className="collapsed-sidebar-submit-button",
                        n_clicks=0)



model_1 = html.Div(
                 children=[
                     html.P("Timesteps per Batch", className="p_dark"),
                     dbc.Input(id="model_1",
                               type="number",
                               min=10,
                               max=100000,
                               step=10,
                               placeholder=10)
                 ])
model_2 = html.Div(
                 children=[
                     html.P("Set Max KL-Distance", className="p_dark"),
                     dcc.Slider(id='model_2',
                                value=0.01,
                                min=0,
                                max=0.1,
                                step=0.01
                                )
                 ])


model_3 = html.Div(
                 children=[
                     html.P("Set Number of Conjugate Gradient Descent Iterations", className="p_dark"),
                     dbc.Input(id="model_3",
                               type="number",
                               min=10,
                               max=100,
                               step=10,
                               placeholder=10)
                 ])
model_4 = html.Div(
                 children=[
                     html.P("Set Conjugate Gradient Descent Dampening", className="p_dark"),
                        dcc.Slider(id='model_4',
                                value=0.1,
                                min=0,
                                max=1,
                                step=0.1
                                )
                 ])

model_5 = html.Div(
                 children=[
                     html.P("Set Discount Factor", className="p_dark"),
                        dcc.Slider(id='model_5',
                                value=0.99,
                                min=0,
                                max=1,
                                step=0.1
                                )
                 ])

model_6 = html.Div(
                 children=[
                     html.P("Set L1 Penalty", className="p_dark"),
                     dcc.Slider(id='model_6',
                                value=0.98,
                                min=0.9,
                                max=1,
                                step=0.01
                                )
                 ])

model_7 = html.Div(
                 children=[
                     html.P("Set Number of Value Function Iterations", className="p_dark"),
                     dbc.Input(id="model_7",
                               type="number",
                               min=1,
                               max=100,
                               step=10,
                               placeholder=10)
                 ])

model_8 = html.Div(
                 children=[
                     html.P("Set Value Function Step Size", className="p_dark"),
                    dcc.Slider(id='model_8',
                                value=0.001,
                                min=0,
                                max=0.01,
                                step=0.001
                                )
                 ])

params = dbc.Accordion(
        [
            dbc.AccordionItem(
                    title="Standard Parameters",
                    children=[
                                model_1,
                                model_2,
                                model_3,
                                model_4,
                                model_5,
                                model_6,
                                model_7,
                                model_8
                    ]
                )
            ])



menu = html.Div(id="model-menu",
                children=[
                    params,
                    model_params_submit_button
                ])


@callback(
    [Output(component_id="model_1", component_property="value"),
    Output(component_id="model_2", component_property="value"),
    Output(component_id="model_3", component_property="value"),
    Output(component_id="model_4", component_property="value"),
    Output(component_id="model_5", component_property="value"),
     Output(component_id="model_6", component_property="value"),
     Output(component_id="model_7", component_property="value"),
     Output(component_id="model_8", component_property="value")
     ],
    Input(component_id="model_parameters", component_property="data")
)
def populate_default_model_params(inputs):
     model1 = inputs["timesteps_per_batch"]
     model2 = inputs["max_kl"]
     model3 = inputs["cg_iters"]
     model4 = inputs["cg_damping"]
     model5 = inputs["gamma"]
     model6 = inputs["lam"]
     model7 = inputs["vf_iters"]
     model8 = inputs["vf_stepsize"]
     return model1, model2, model3, model4, model5, model6, model7, model8

@callback(
    Output(component_id="model_parameters", component_property="data"),
    Input(component_id="tools-menu-submit-model-button", component_property="n_clicks"),
    [State(component_id="model_parameters", component_property="data"),
     State(component_id="model_1", component_property="value"),
     State(component_id="model_2", component_property="value"),
     State(component_id="model_3", component_property="value"),
     State(component_id="model_4", component_property="value"),
     State(component_id="model_5", component_property="value"),
     State(component_id="model_6", component_property="value"),
     State(component_id="model_7", component_property="value"),
     State(component_id="model_8", component_property="value")
     ],
           allow_duplicate=True, prevent_initial_call=True
)
def update_model_parameters(click, parameters, model1, model2, model3, model4, model5,
                          model6, model7, model8):
    if click:
        parameters["timesteps_per_batch"] = model1
        parameters["max_kl"] = model2
        parameters["cg_iters"] = model3
        parameters["cg_damping"] = model4
        parameters["gamma"] = model5
        parameters["lam"] = model6
        parameters["vf_iters"] = model7
        parameters["vf_stepsize"] = model8

    return parameters
