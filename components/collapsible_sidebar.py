from dash import html, callback, Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from utils import text
from components.Parameters import map, rai, environment, model, chatgpt


# Map Parameters
map_icon = html.I(className="bi bi-globe-asia-australia")
map_params_button = dbc.Button(
                        children=[map_icon],
                        id="tools-menu-map-button",
                        className="collapsed-sidebar-button",
                        n_clicks=0)
map_params_menu = dbc.Offcanvas(id="tools-menu-map-menu",
                                className="collapsed-sidebar-element",
                                title= text.tools_menu_map_params_title,
                                children=[map.menu],
                                scrollable=True,
                                is_open=False)


# Responsibility Parameters
rai_icon = html.I(className="bi bi-cone-striped")
rai_params_button = dbc.Button(
                        children=[rai_icon],
                        id="tools-menu-rai-button",
                        className="collapsed-sidebar-button",
                        n_clicks=0)
rai_params_menu = dbc.Offcanvas(id="tools-menu-rai-menu",
                                className="collapsed-sidebar-element",
                                title= text.tools_menu_rai_params_title,
                                children=[rai.menu],
                                scrollable=True,
                                is_open=False)
# Swarm Parameters
swarm_icon = html.I(className="bi bi-bezier")
swarm_params_button = dbc.Button(
                        children=[swarm_icon],
                        id="tools-menu-swarm-button",
                        className="collapsed-sidebar-button",
                        n_clicks=0)
swarm_params_menu = dbc.Offcanvas(id="tools-menu-swarm-menu",
                                className="collapsed-sidebar-element",
                                title= text.tools_menu_swarm_params_title,
                                children=[environment.menu],
                                scrollable=True,
                                is_open=False)

# DRL Parameters
drl_icon = html.I(className="bi bi-tools")
drl_params_button = dbc.Button(
                        children=[drl_icon],
                        className="collapsed-sidebar-button",
                        id="tools-menu-drl-button",
                        n_clicks=0)
drl_params_menu = dbc.Offcanvas(id="tools-menu-drl-menu",
                                className="collapsed-sidebar-element",
                                title= text.tools_menu_drl_params_title,
                                children=[model.menu],
                                scrollable=True,
                                is_open=False)

# ChatGPT Parameters
chat_icon = html.I(className="bi bi-chat-left-text")
chat_params_button = dbc.Button(
                        children=[chat_icon],
                        className="collapsed-sidebar-button",
                        id="tools-menu-chat-button",
                        n_clicks=0)
chat_params_menu = dbc.Offcanvas(id="tools-menu-chat-menu",
                                className="collapsed-sidebar-element",
                                title= text.tools_menu_chat_params_title,
                                children=[chatgpt.menu],
                                scrollable=True,
                                is_open=False)


collapsible_sidebar_layout = html.Div(
    id="run-page-collapsible-sidebar",
    className="collapsed-sidebar",
    children=[map_params_button,
              map_params_menu,
              rai_params_button,
              rai_params_menu,
              swarm_params_button,
              swarm_params_menu,
              drl_params_button,
              drl_params_menu,
              chat_params_button,
              chat_params_menu])


@callback(
    Output("tools-menu-map-menu", "is_open"),
    Input("tools-menu-map-button", "n_clicks"),
    State("tools-menu-map-menu", "is_open"),
)
def toggle_map_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("tools-menu-rai-menu", "is_open"),
    Input("tools-menu-rai-button", "n_clicks"),
    State("tools-menu-rai-menu", "is_open"),
)
def toggle_rai_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("tools-menu-swarm-menu", "is_open"),
    Input("tools-menu-swarm-button", "n_clicks"),
    State("tools-menu-swarm-menu", "is_open"),
)
def toggle_swarm_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@callback(
    Output("tools-menu-drl-menu", "is_open"),
    Input("tools-menu-drl-button", "n_clicks"),
    State("tools-menu-drl-menu", "is_open"),
)
def toggle_drl_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("tools-menu-chat-menu", "is_open"),
    Input("tools-menu-chat-button", "n_clicks"),
    State("tools-menu-chat-menu", "is_open"),
)
def toggle_chat_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open