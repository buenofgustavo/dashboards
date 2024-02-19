import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc


def comparativovolumetria():
    #Inicio gerar grafico dash
    #Leitura do arquivo gerado
    caminho_sqltop5clientes = 'src\main\Consultas\sqltop5clientessemanal.csv'
    comparacaovolumetria = 'src\main\Consultas\comparacaovolumetria.csv'
    df = pd.read_csv(caminho_sqltop5clientes)
    df2 = pd.read_csv(comparacaovolumetria)

    #Pegou o pagador csv 1
    leitura = df["PAGADOR"]
    pagador = leitura.values
    #Pegou o pagador csv 2
    leitura2 = df2["Pagador"]
    pagador2 = leitura2.values
    #Pegou qtd docs csv1
    leitura = df["total_codcon"]
    qtddocs = leitura.values
    #Pegou qtd docs csv1
    leitura2 = df2["total_codcon"]
    qtddocs2 = leitura2.values


    assert len(pagador) == len(pagador2) == len(qtddocs) == len(qtddocs2)

    pagador1_modificado = [f"{nome}_2024" for nome in pagador2]
    pagador2_modificado = [f"{nome}_2023" for nome in pagador2]

# Em seguida, crie listas intercaladas para x e y
    x_intercalado = [val for pair in zip(pagador1_modificado, pagador2_modificado) for val in pair]
    y_intercalado = [val for pair in zip(qtddocs, qtddocs2) for val in pair]

# Agora, crie uma lista de cores, alternando entre as duas cores
    cores = ['#4285F4' if i % 2 == 0 else '#BE360C' for i in range(len(x_intercalado))]

# Finalmente, crie o gráfico
    comparativovolumetria = go.Figure(
    data=[
        go.Bar(
            x=x_intercalado,
            y=y_intercalado,
            marker=dict(color=cores),
            text=y_intercalado,
        )
    ]
)
    comparativovolumetria.update_layout(
    title='Comparativo volumetria 2024 x 2023',
    title_font_size=20,
    title_x=0.5,
    title_y=0.9,
    barmode='group',
    xaxis=dict(
        tickfont=dict(
            size=8,
        )
    )
)

    return comparativovolumetria
    #final gerar grafico