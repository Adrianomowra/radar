from app import *
from dash import html, dcc
from pages import sidebar, dashboard, extra
from dash.dependencies import Input, Output

#carregar o conteudo da pagina solicitada  na coluna da pagina 
pagina = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dbc.Row([
        #coluna da sidebar ocupando 2 de 12
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md= 2),
        #coluna e estrutura onnde sera apresentada o conteudo das paginas ocupando 10 de 12
        dbc.Col([
            pagina
        ],md=10)
    ])
],fluid=True,style={'height':'100vh'})

# callbacks pora mudança de paginas 
@app.callback(Output('page-content', 'children'),
              [Input('url','pathname')])

def render_page(pathname):
    if pathname == '/' or pathname == '/dashboard':
        return dashboard.layout

    if pathname == '/extra':
        return extra.layout


# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)