import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def layout_volumetriaclientes(Graficovolumetria):
    return dbc.Col(
            html.Div(
                dcc.Graph(
                    id='Graficovolumetria',
                    figure=Graficovolumetria,
                ),
                style={'margin-left':'-130px', 'margin-top':'80px', 'width': '130%', 'height': '60vh', 'borderRadius': '20px'},  # Ajuste a largura e a altura conforme necessário
            ),
            width=6,
        )