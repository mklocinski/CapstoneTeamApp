from dash import Dash, dcc, html
import dash
import dash_bootstrap_components as dbc
from pages import main
from components import navbar
import config

# ------------------------------------------------------------------ #
# --------------------------- Styling ------------------------------ #
# ------------------------------------------------------------------ #

# App stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]


# ------------------------------------------------------------------ #
# --------------------------- App Setup ---------------------------- #
# ------------------------------------------------------------------ #
# Setup app
app = Dash(__name__,
            external_stylesheets=external_stylesheets,
            use_pages=True,
            pages_folder="pages",
            suppress_callback_exceptions=True,
            prevent_initial_callbacks='initial_duplicate')
server = app.server
from flask.helpers import get_root_path
print(get_root_path(__name__))
# Register first screen of app as 'Main'
dash.register_page("Main", layout=main.main_layout, path='/')

# Define first screen layout
map_data = config.map_params
rai_data = config.rai_params
swarm_data = config.environment_params
drl_data = config.model_params
chat_data = config.chat_params
app.layout = html.Div(
            children=[
            dcc.Store(id='drone-data'),
            dcc.Store(id='chat-messages'),
            dcc.Store(id='model-run-type',
                      data = config.model_run_status),
            dcc.Store(id='map_parameters',
                      data = map_data),
            dcc.Store(id='rai_parameters',
                      data = rai_data),
            dcc.Store(id='environment_parameters',
                      data = swarm_data),
            dcc.Store(id='model_parameters',
                      data = drl_data),
            dcc.Store(id='chat_parameters',
                      data = chat_data),
            dash.page_container,
            navbar.make_navbar
            ])



if __name__ == '__main__':
    app.run(debug=True)

