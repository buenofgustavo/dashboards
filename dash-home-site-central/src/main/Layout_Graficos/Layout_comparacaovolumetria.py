import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def Layout_comparacaovolumetria(Graficocomparacao):
    return dbc.Col(
            html.Div(
                dcc.Graph(
                    id='Graficocomparacao',
                    figure=Graficocomparacao,
                ),
                style={'margin-left':'-85px', 'margin-top':'80px', 'width': '140%', 'height': '60vh', 'borderRadius': '20px'},  # Ajuste a largura e a altura conforme necessário
            ),
            width=6,
        )