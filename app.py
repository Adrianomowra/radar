import dash
import dash_bootstrap_components as dbc

#iniciar o dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.config.suppress_callback_exceptions = True