import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from src.main.Graficos.volumetriaclientes import volumetriaclientes
from src.main.Graficos.comparacaovolumetria import comparativovolumetria
from src.main.Layout_Graficos.Layout_volumetriaclientes import layout_volumetriaclientes
from src.main.Layout_Graficos.Layout_comparacaovolumetria import Layout_comparacaovolumetria


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.YETI])
#chama a função  do grafico
Graficovolumetria = volumetriaclientes()
Graficocomparativo = comparativovolumetria()

#layout da pagina
app.layout = dbc.Container([
    dbc.Row([
    layout_volumetriaclientes(Graficovolumetria),
    Layout_comparacaovolumetria(Graficocomparativo)
    ])
])



