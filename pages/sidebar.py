import dash_bootstrap_components as dbc
from dash import html

layout = dbc.Card([
    html.H1("RADAR", className="text-primary"),
    html.P("Controle", className="text-info"),
    dbc.Button(children=[html.Img(src="/assets/radar.png", style={'width':'100px', 'height':'auto'})],
            style={'background-color': 'transparent', 'border-color':'transparent'}),

dbc.Nav([
    dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
    dbc.NavLink("Extra", href="/extra", active="exact"),
], vertical=True, pills=True , style={"margin-bottom":"5px"}),
html.Hr(),
#continuar os conteudos aqui abaixo com DIV's

],color="dark", inverse=True, style={'height': '100vh'})



 