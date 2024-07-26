import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from app import app 

# Carregar a planilha Excel
file_path = 'assets/indicadores de velocidade.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M')

# Função para filtrar o DataFrame pelo nome do motorista, placa do veículo e intervalo de datas
def filter_df(df, driver_name=None, plate=None, start_date=None, end_date=None):
    if driver_name:
        df = df[df['Motorista'].str.contains(driver_name, case=False, na=False)]
    if plate:
        df = df[df['Placa'].str.contains(plate, case=False, na=False)]
    if start_date and end_date:
        df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]
    return df

# Configuração inicial dos gráficos
def create_figures(df):
    # Gráfico de barras
    bar_fig = px.bar(df, x='Motorista', y='Média/Inicial', title='Média de Velocidade por Motorista')
    bar_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        title=dict(text='Média de Velocidade por Motorista', font=dict(size=10))
    )
    bar_fig.update_traces(marker_line_color='white', marker_line_width=1.5)

    # Gráfico de dispersão
    scatter_fig = px.scatter(df, x='Long', y='Lat', hover_name='Motorista', 
                             title='Localização dos Incidentes', labels={'Long': 'Longitude', 'Lat': 'Latitude'})
    scatter_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    scatter_fig.update_traces(marker=dict(line=dict(width=1.5, color='white')))

    # Gráfico de linhas
    line_fig = px.line(df, x='Data', y='Média/Inicial', title='Velocidade Média ao Longo do Tempo', markers=True)
    line_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    # Gráfico de pizza
    pie_fig = px.pie(df, names='Infração', title='Distribuição das Infrações')
    pie_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10)
    )

    # Mapa
    map_fig = px.scatter_mapbox(df, lat='Lat', lon='Long', hover_name='Motorista', 
                                title='Mapa de Localização dos Incidentes',
                                mapbox_style='carto-darkmatter', zoom=10)
    map_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10)
    )

    return bar_fig, scatter_fig, line_fig, pie_fig, map_fig

# Criação inicial dos gráficos
bar_fig, scatter_fig, line_fig, pie_fig, map_fig = create_figures(df)

#--------------------------------- Layout da página com gráficos 
layout = dbc.Container(children=[
    dbc.Row([
        dbc.Row([
            dbc.Card([
                html.H1("Estrutura básica com páginas e sidebar"),
                html.H1("PÁGINA 1 DASHBOARD")
            ],color="dark", inverse=True, style={'margin': '0px -10px -10px 0px'}), 
        ], className="g-0 my-auto mt-1 mb-1"),
        # -----------------------------------------------------------------Linha de busca
        dbc.Row([
            dbc.Col([
                dbc.Input(id='input-nome', placeholder='Digite o nome do motorista...', type='text'),
            ], width=3),
            dbc.Col([
                dbc.Input(id='input-placa', placeholder='Digite a placa do veículo...', type='text'),
            ], width=3),
            dbc.Col([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df['Data'].min().date(),
                    end_date=df['Data'].max().date(),
                    display_format='DD/MM/YYYY',style={
                        'font-size': '5px',  
                        'display': 'inline-block',              
                        'height': '10px'
                    }
                )
            ], width=3),
        ], style={'margin-top':'20px','margin-botton':'20px'}),
        dbc.Row([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='bar-fig', figure=bar_fig)  # Gráfico de barras
                        ], width=2),
                        dbc.Col([
                            dcc.Graph(id='line-fig', figure=line_fig)  # Gráfico de linhas
                        ], width=6),
                        dbc.Col([
                            dcc.Graph(id='pie-fig', figure=pie_fig)  # Gráfico de pizza
                        ], width=4),
                    ])
                ])
            ],color="dark", inverse=True, style={'margin': '0px 0px 0px 0px'}),
        ], style={'margin-top':'20px','margin-botton':'20px'}),
        dbc.Row([
            dcc.Graph(id='scatter-fig', figure=scatter_fig)  # Gráfico de dispersão
        ]),
        dbc.Row([
            dcc.Graph(id='map-fig', figure=map_fig)  # Mapa
        ]),
    ])
], fluid=True, style={'height': '100vh'})

@app.callback(
    [Output('bar-fig', 'figure'),
     Output('scatter-fig', 'figure'),
     Output('line-fig', 'figure'),
     Output('pie-fig', 'figure'),
     Output('map-fig', 'figure')],
    [Input('input-nome', 'value'),
     Input('input-placa', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(driver_name, plate, start_date, end_date):
    filtered_df = filter_df(df, driver_name, plate, start_date, end_date)
    return create_figures(filtered_df)

