import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc


def volumetriaclientes():
    #Inicio gerar grafico dash
    #Leitura do arquivo gerado
    caminho_sqltop5clientes = 'src\main\Consultas\sqltop5clientessemanal.csv'
    df = pd.read_csv(caminho_sqltop5clientes)
    #Pegou o pagador
    leitura = df["PAGADOR"]
    pagador = leitura.values
    #Pegou qtd docs
    leitura = df["total_codcon"]
    qtddocs = leitura.values


    Graficovolumetria = go.Figure(
            data=[
                go.Bar(
                    x=pagador,
                    y=qtddocs,
                    name='Volumetria clientes',  # Nome colunas
                    opacity=1,
                    text = qtddocs,
                    marker=dict(color='#4285F4')
                )
            ]
        )

    Graficovolumetria.update_layout(
            title='Volumetria últimos 7 dias (TOP 5)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário

            xaxis=dict(
                tickfont=dict(
                    size=8,
                )
            )
        )
    return Graficovolumetria
    #final gerar grafico 