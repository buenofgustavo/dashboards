# Layout da aplicação
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import html

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

df = pd.read_csv("resultados_query.csv", sep=";", decimal=",")

@app.callback(
    Output('grafico_fat_cli', 'figure'),
    [
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value'),
    ],
    allow_duplicate=True
)

def update_graf2(value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por nenhum input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'NENHUM':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'NENHUM':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_fil[
            tabela_filtrada_fil.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_fim.index)
        ]


        resultado_graf2 = tabela_filtrada_final.groupby('TOMADOR').size().reset_index(name='frequencia')
        resultado_graf2 = resultado_graf2.sort_values(by='frequencia', ascending=False).head(10)
        tomadores_graf2 = resultado_graf2['TOMADOR'].tolist()
        qtd_total_PC_cliente_graf2 = resultado_graf2['frequencia'].tolist()

        #print(f'Tomadores: {tomadores_graf2}')
        #print(f'Total PCs clientes: {qtd_total_PC_cliente_graf2}')

        PCs_baixadas_graf2 = []
        i=0

        while(i<len(tomadores_graf2)):
            tab_tomador_graf2 = tabela_filtrada_final.loc[tabela_filtrada_final['TOMADOR']== tomadores_graf2[i], :]
            PCs_baixadas_graf2.append(tab_tomador_graf2[tab_tomador_graf2['SITUAC'] == 'B'].shape[0])
            i+=1

        #print(f'PCs baixadas: {PCs_baixadas_graf2}')

        fat_cliente_graf2 = []

        for tomador in tomadores_graf2:
            tabela_filtrada_final.loc[:, 'TOTALFRETE'] = pd.to_numeric(tabela_filtrada_final['TOTALFRETE'], errors='coerce')
            totfre_total_graf2 = tabela_filtrada_final[tabela_filtrada_final['TOMADOR'] == tomador]['TOTALFRETE'].sum()
            fat_cliente_graf2.append(totfre_total_graf2)

        fat_cliente_graf2 = [round(valor, 2) for valor in fat_cliente_graf2]

        #print(fat_cliente_graf2)

        i=0
        media_cliente_graf2 = []
        faturamento_potencial_graf2 = []
        while(i<len(tomadores_graf2)):
            media_cli_graf2 = fat_cliente_graf2[i]/PCs_baixadas_graf2[i]
            media_cliente_graf2.append(media_cli_graf2)
            fat_pot_graf2 = (fat_cliente_graf2[i]/PCs_baixadas_graf2[i]) * qtd_total_PC_cliente_graf2[i]
            faturamento_potencial_graf2.append(fat_pot_graf2)
            i+=1

        media_cliente_graf2 = [round(valor, 2) for valor in media_cliente_graf2]
        faturamento_potencial_graf2 = [round(valor, 2) for valor in faturamento_potencial_graf2]

        #print(media_cliente_graf2)
        #print(faturamento_potencial_graf2)

        fig2 = go.Figure(
            data=[
                go.Bar(
                    x=tomadores_graf2,
                    y=faturamento_potencial_graf2,
                    name='Faturamento Potencial',  # Nome da primeira barra
                    opacity=0.7
                ),
                go.Scatter(
                    x=tomadores_graf2,
                    y=fat_cliente_graf2,
                    mode='markers+text',  # Adicionando texto aos pontos
                    marker=dict(color='blue', size=10),  # Definindo cor e tamanho do marcador
                    text=fat_cliente_graf2,  # Usando os valores como texto
                    textposition='top center',  # Posição do texto (no topo do ponto)
                    textfont=dict(size=12, color='black'),  # Estilo do texto
                    name='Faturamento Real'
                ),
                go.Scatter(
                    x=tomadores_graf2,
                    y=fat_cliente_graf2,
                    mode='lines',  # Somente linhas para os valores reais
                    line=dict(color='blue', width=2),
                    name='Faturamento Real'
                ),
            ]
        )

        fig2.update_layout(
            title='Faturamento',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )
        return fig2

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate