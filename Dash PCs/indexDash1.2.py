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
from datetime import datetime
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Se o código acima falhar, você pode tentar uma alternativa
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

df = pd.read_csv("tabela_view.csv", sep=";", decimal=",")

df['STATUS'] = df['STATUS'].str.strip().str.upper()

##################################################################################################################
# GRÁFICO 1

situacoes_CODLINLIN = np.array(['Atendido', 'Cadastradas', 'Em atendimento', 'CANCELADO - CLIENTE', 'DECLINADO - FALTA ATENDIMENTO', 'CARGA RECUSADA'])

quantidades_CODLINLIN = [
    df[df['SITUAC'] == 'B'].shape[0],
    df[df['SITUAC'] == 'D'].shape[0],
    df[df['SITUAC'] == 'M'].shape[0],
    df[df['CODMTC'] == 22].shape[0],
    df[df['CODMTC'] == 21].shape[0],
    df[df['CODMTC'] == 23].shape[0]
]


fig = px.pie(names=situacoes_CODLINLIN, values=quantidades_CODLINLIN, title='Distribuição das Situações')
fig.update_traces(
    textposition='auto', 
    textinfo='value', 
    outsidetextfont=dict(size=20), 
    insidetextfont=dict(size=30)
    )  # Define para mostrar os valores


opcoes_CODLINLIN = list(df['LINHA'].unique())
opcoes_CODLINLIN.insert(0, 'TODAS AS LINHAS')
##################################################################################################################
# GRÁFICO 2

resultado_graf2 = df.groupby('TOMADOR').size().reset_index(name='frequencia')
resultado_graf2 = resultado_graf2.sort_values(by='frequencia', ascending=False).head(10)
tomadores_graf2 = resultado_graf2['TOMADOR'].tolist()
qtd_total_PC_cliente_graf2 = resultado_graf2['frequencia'].tolist()

#print(f'Tomadores: {tomadores_graf2}')
#print(f'Total PCs clientes: {qtd_total_PC_cliente_graf2}')

PCs_baixadas_graf2 = []
i=0

while(i<len(tomadores_graf2)):
    tab_tomador_graf2 = df.loc[df['TOMADOR']== tomadores_graf2[i], :]
    PCs_baixadas_graf2.append(tab_tomador_graf2['TOTALFRETE'].notnull().sum())
    i+=1
PCs_baixadas_card1 = df['TOTALFRETE'].notnull().sum()

#print(f'PCs baixadas: {PCs_baixadas_graf2}')

fat_cliente_graf2 = []

for tomador in tomadores_graf2:
    df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
    totfre_total_graf2 = df[df['TOMADOR'] == tomador]['TOTALFRETE'].sum()
    fat_cliente_graf2.append(totfre_total_graf2)

fat_cliente_graf2 = [round(valor, 2) for valor in fat_cliente_graf2]

fat_cliente_graf2_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in fat_cliente_graf2]
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

faturamento_potencial_graf2_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in faturamento_potencial_graf2]



#print(media_cliente_graf2)
#print(faturamento_potencial_graf2)

fig2 = go.Figure(

    data=[
        go.Bar(
            x=tomadores_graf2,
            y=faturamento_potencial_graf2,
            name='Faturamento Potencial',  # Nome da primeira barra
            opacity=0.7,
            offsetgroup = 1,
            text=faturamento_potencial_graf2_formatado,  # Adicionando valores de texto acima das barras
            textposition='inside',  # Posição automática do texto
            textfont=dict(size=14),
        ),

        go.Bar(
            x=tomadores_graf2,
            y=fat_cliente_graf2,
            name='Faturamento Real',
            opacity=0.7,
            offsetgroup = 2,
            text=fat_cliente_graf2_formatado,  # Adicionando valores de texto acima das barras
            textposition='inside', 
            textfont=dict(size=14),
        ),
    ]

)

fig2.update_layout(
    title='Faturamento (TOP 10)',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)


#######################################################################################################################################
# Gráfico 3

status_desejados_graf3 = [21,22,23]
df_filtrado_graf3 = df[df['CODMTC'].isin(status_desejados_graf3)]

# Agrupar por TOMADOR e contar a ocorrência de cada STATUS
contagem_por_tomador_graf3 = df_filtrado_graf3.groupby('TOMADOR')["CODMTC"].value_counts().unstack(fill_value=0)

# Calcular o total de ocorrências para cada TOMADOR
contagem_por_tomador_graf3['TOTAL'] = contagem_por_tomador_graf3.sum(axis=1)

# Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
top_5_tomadores_graf3 = contagem_por_tomador_graf3.sort_values(by='TOTAL', ascending=False).head(5)

# Preencher valores ausentes com 0
top_5_tomadores_graf3 = top_5_tomadores_graf3.fillna(0)

tomadores_graf3 = top_5_tomadores_graf3.index.values


media_cliente_graf3 = media_cliente_graf2
tomadores_graf3 = tomadores_graf3

PCs_declinadas_graf3 = []
PCs_carga_recusada_graf3 = []
PCs_declinada_atendimento_graf3 = []
PCs_declinada_cliente_graf3 = []
i=0
while(i<len(tomadores_graf3)):
    tab_tomador_graf3 = df.loc[df['TOMADOR']== tomadores_graf3[i], :]
    PCs_carga_recusada_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 23].shape[0])
    PCs_declinada_cliente_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 22].shape[0])
    PCs_declinada_atendimento_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 21].shape[0])
    PCs_declinadas_graf3.append(PCs_carga_recusada_graf3[i] + PCs_declinada_cliente_graf3[i] + PCs_declinada_atendimento_graf3[i])
    i+=1

faturamento_potencial_perdido_graf3 = []
i=0
while(i<len(tomadores_graf3)):
    faturamento_potencial_perdido_graf3.append(media_cliente_graf3[i] * PCs_declinadas_graf3[i])
    i+=1

faturamento_potencial_perdido_graf3 = [round(valor, 2) for valor in faturamento_potencial_perdido_graf3]

faturamento_potencial_perdido_graf3_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in faturamento_potencial_perdido_graf3]


fig3 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf3,
            y=faturamento_potencial_perdido_graf3,
            name='Faturamento potencial perdido por cliente',  # Nome da primeira barra
            opacity=0.7,
            text = faturamento_potencial_perdido_graf3_formatado,
            textposition='inside', 
            textfont=dict(size=14),
        )
    ]
)

fig3.update_layout(
    title='Faturamento Potencial Perdido (TOP 5)',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)

#######################################################################################################################################
# Gráfico 4

resultado_graf4 = df.groupby('TOMADOR').size().reset_index(name='frequencia')
resultado_graf4 = resultado_graf4.sort_values(by='frequencia', ascending=False).head(1)
tomadores_graf4 = resultado_graf4['TOMADOR'].tolist()
qtd_total_PC_cliente_graf4 = resultado_graf4['frequencia'].tolist()

#print(f'Tomadores: {tomadores_graf4}')
#print(f'Total PCs clientes: {qtd_total_PC_cliente_graf4}')

PCs_baixadas_graf4 = []
i=0

while(i<len(tomadores_graf4)):
    tab_tomador_graf4 = df.loc[df['TOMADOR']== tomadores_graf4[i], :]
    PCs_baixadas_graf4.append(tab_tomador_graf4['TOTALFRETE'].notnull().sum())
    i+=1

#print(f'PCs baixadas: {PCs_baixadas_graf4}')

fat_cliente_graf4 = []

for tomador in tomadores_graf4:
    df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
    totfre_total_graf4 = df[df['TOMADOR'] == tomador]['TOTALFRETE'].sum()
    fat_cliente_graf4.append(totfre_total_graf4)

fat_cliente_graf4 = [round(valor, 2) for valor in fat_cliente_graf4]

fat_cliente_graf4_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in fat_cliente_graf4]
#print(fat_cliente_graf4)

i=0
media_cliente_graf4 = []
faturamento_potencial_graf4 = []
while(i<len(tomadores_graf4)):
    media_cli_graf4 = fat_cliente_graf4[i]/PCs_baixadas_graf4[i]
    media_cliente_graf4.append(media_cli_graf4)
    fat_pot_graf4 = (fat_cliente_graf4[i]/PCs_baixadas_graf4[i]) * qtd_total_PC_cliente_graf4[i]
    faturamento_potencial_graf4.append(fat_pot_graf4)
    i+=1

media_cliente_graf4 = [round(valor, 2) for valor in media_cliente_graf4]
faturamento_potencial_graf4 = [round(valor, 2) for valor in faturamento_potencial_graf4]

faturamento_potencial_graf4_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in faturamento_potencial_graf4]


#print(media_cliente_graf4)
#print(faturamento_potencial_graf4)

fig4 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf4,
            y=faturamento_potencial_graf4,
            name='Faturamento Potencial',  # Nome da primeira barra
            opacity=0.7,
            text = faturamento_potencial_graf4_formatado,
            textposition='inside', 
            textfont=dict(size=16),
        ),
        go.Bar(
            x=tomadores_graf4,
            y=fat_cliente_graf4,
            text = fat_cliente_graf4_formatado,
            textposition='inside', 
            textfont=dict(size=16),
            name='Faturamento Real'
        ),

    ]
)

fig4.update_layout(
    title='Faturamento por Cliente',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)

#######################################################################################################################################
# Gráfico 5 - Quantidade PCs Cliente 

status_desejados_graf5 = [21,22,23]
df_filtrado_graf5 = df[df['CODMTC'].isin(status_desejados_graf5)]

# Agrupar por TOMADOR e contar a ocorrência de cada STATUS
contagem_por_tomador_graf5 = df_filtrado_graf5.groupby('TOMADOR')['STATUS'].value_counts().unstack(fill_value=0)

# Calcular o total de ocorrências para cada TOMADOR
contagem_por_tomador_graf5['TOTAL'] = contagem_por_tomador_graf5.sum(axis=1)

# Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
top_5_tomadores_graf5 = contagem_por_tomador_graf5.sort_values(by='TOTAL', ascending=False).head(5)

# Preencher valores ausentes com 0
top_5_tomadores_graf5 = top_5_tomadores_graf5.fillna(0)

# Verificar se a coluna existe antes de acessá-la e atribuir 0 se não existir
carga_recusada_graf5 = top_5_tomadores_graf5[23].values if 23 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
cancelado_cliente_graf5 = top_5_tomadores_graf5[22].values if 22 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
declinado_falta_atendimento_graf5 = top_5_tomadores_graf5[21].values if 21 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)

# Extrair os resultados em vetores
tomadores_graf5 = top_5_tomadores_graf5.index.values
total_ocorrencias_graf5 = top_5_tomadores_graf5['TOTAL'].values

fig5 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf5,
            y=total_ocorrencias_graf5,
            name='Quantidade de PC Cancelada',  # Nome da primeira barra
            opacity=0.7,
            text = total_ocorrencias_graf5,
            textposition='inside', 
            textfont=dict(size=18),
        )
    ]
)

fig5.update_layout(
    title='Quantidade de Carga Cancelada (TOP 5)',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)


#######################################################################################################################################
# Gráfico 6 - Quantidade PCs Atrasadas  

# Obtém a data de hoje
df['DATRET'] = pd.to_datetime(df['DATRET'], errors='coerce')

filtered_df = df[(df['DATRET'].notnull()) & (df['DATRET'] < datetime.now()) & (df['SITUAC'].isin(['D', 'M'])) & (df['CTE'].isnull())]

# Obtendo o total de registros
pcs_em_atraso_graf6 = filtered_df


# Filtra as prescrições de crédito em atraso

# Agrupa por cliente e conta as prescrições de crédito em atraso para cada cliente
pcs_por_cliente_graf6 = pcs_em_atraso_graf6.groupby('TOMADOR').size().reset_index(name='PCS_EM_ATRASO_POR_CLIENTE')

# Ordena em ordem decrescente e seleciona os top 5
top5_pcs_por_cliente_graf6 = pcs_por_cliente_graf6.sort_values(by='PCS_EM_ATRASO_POR_CLIENTE', ascending=False).head(5)

# Obtém os top 5 tomadores e resultados
top5_tomadores_graf6 = top5_pcs_por_cliente_graf6['TOMADOR'].to_list()
top5_resultados_por_cliente_graf6 = top5_pcs_por_cliente_graf6['PCS_EM_ATRASO_POR_CLIENTE'].to_list()

# Exibe os top 5 resultados
# print(top5_tomadores_graf6)
# print(top5_resultados_por_cliente_graf6)

fig6 = go.Figure(
    data=[
        go.Bar(
            x=top5_tomadores_graf6,
            y=top5_resultados_por_cliente_graf6,
            name='Quantidade de PC Cancelada',  # Nome da primeira barra
            opacity=0.7,
            text = top5_resultados_por_cliente_graf6,
            textposition='inside', 
            textfont=dict(size=18),
        )
    ]
)

fig6.update_layout(
    title='Quantidade de Carga em Atraso (TOP 5)',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)

#######################################################################################################################################
# Gráfico 7 - Quantidade PCs em Aberto 

df_filtrado_graf7 = df[(df['CTE'].isnull()) & (df['SITUAC'].isin(['D', 'M']))]

pcs_por_cliente_graf7 = df_filtrado_graf7.groupby('TOMADOR').size().reset_index(name='PCs_em_aberto_por_cliente')
top5_pcs_por_cliente_graf7 = pcs_por_cliente_graf7.sort_values(by='PCs_em_aberto_por_cliente', ascending=False).head(5)

# Obtém os top 5 tomadores e resultados
top5_tomadores_graf7 = top5_pcs_por_cliente_graf7['TOMADOR'].to_list()
top5_resultados_por_cliente_graf7 = top5_pcs_por_cliente_graf7['PCs_em_aberto_por_cliente'].to_list()

fig7 = go.Figure(
    data=[
        go.Bar(
            x=top5_tomadores_graf7,
            y=top5_resultados_por_cliente_graf7,
            name='Quantidade de PC Cancelada',  # Nome da primeira barra
            opacity=0.7,
            text = top5_resultados_por_cliente_graf7,
            textposition='inside', 
            textfont=dict(size=18),
        )
    ]
)

fig7.update_layout(
    title='Quantidade de Carga em Aberto (TOP 5)',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)


#######################################################################################################################################
# Card 1



df['STATUS'] = df['STATUS'].str.strip().str.upper()

df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
totfre_total_card1 = df['TOTALFRETE'].sum()
#print(totfre_total_card1)
PCs_baixadas_card1 = df['TOTALFRETE'].notnull().sum()

PCs_carga_recusada_card1 = df[df['CODMTC'] == 23].shape[0]
PCs_cancelado_cliente_card1 = df[df['CODMTC'] == 22].shape[0]
PCs_declinada_atendimento_card1 = df[df['CODMTC'] == 21].shape[0]
PCs_declinadas_card1 = int(PCs_carga_recusada_card1) + int(PCs_cancelado_cliente_card1) + int(PCs_declinada_atendimento_card1)
#print(PCs_declinadas_card1)
media_global_output_card1 = totfre_total_card1/PCs_baixadas_card1
faturamento_potencial_perdido__noformat_card1 = (totfre_total_card1/PCs_baixadas_card1) * PCs_declinadas_card1
faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido__noformat_card1, 2)

faturamento_potencial_perdido_card1_formatado = locale.format_string('%.2f', faturamento_potencial_perdido_card1, grouping=True)
#######################################################################################################################################
# Card 2

PCs_declinadas_cliente_card2 = df[df['CODMTC'] == 22].shape[0]

#######################################################################################################################################
# Card 3

PCs_declinadas_atendimento_card3 = df[df['CODMTC'] == 21].shape[0]
#######################################################################################################################################
# Card 4

PCs_carga_recusada_card4 = df[df['CODMTC'] == 23].shape[0]
#######################################################################################################################################
# Card 5 Todas as Cargas

PCs_totais_card5 = df.shape[0]
#print(PCs_totais_card5)

#######################################################################################################################################
# Card 6

PCs_cadastradas_card6 = filtered_df = df[(df['CTE'].isnull()) & (df['SITUAC'].isin(['D', 'M']))]

# Contando o número de registros no DataFrame resultante
PCs_cadastradas_card6 = filtered_df.shape[0]

#######################################################################################################################################
# Card 7

# Contando o número de registros no DataFrame resultante

df['DATRET'] = pd.to_datetime(df['DATRET'], errors='coerce')

# Filtrando os dados conforme as condições da sua consulta SQL
filtered_df = df[(df['DATRET'].notnull()) & (df['DATRET'] < datetime.now()) & (df['SITUAC'].isin(['D', 'M'])) & (df['CTE'].isnull())]

# Obtendo o total de registros
PCs_em_atraso_card7 = len(filtered_df)


#######################################################################################################################################
# Card 8 Faturamento Real

df_filtrado_card8 = df[(df['TOTALFRETE'].notnull()) & (df['SITUAC'].isin(['D', 'M', 'B']))]

faturamento_real_card8 = df_filtrado_card8['TOTALFRETE'].sum()

faturamento_real_card8 = locale.format_string('%.2f', faturamento_real_card8, grouping=True)


############################################################ Dropdown 2 #################################################################
# Select Clientes

todos_clientes_drop2 = list(df['TOMADOR'].unique())
todos_clientes_drop2.insert(0, 'TODOS OS CLIENTES')

############################################################ Dropdown 3 #################################################################
# Select Filial

todas_filiais_drop3 = list(df['FILPC'].unique())
todas_filiais_drop3.sort()
todas_filiais_drop3.insert(0, 'TODAS AS FILIAIS')


############################################################ Dropdown 4 #################################################################
# Select Ponto Inicial

pontos_iniciais_drop4 = list(df['PONTOINI'].unique())
pontos_iniciais_drop4.insert(0, 'TODOS')

############################################################ Dropdown 5 #################################################################
# Select Ponto Final

pontos_finais_drop5 = list(df['PONTOFIM'].unique())
pontos_finais_drop5.insert(0, 'TODOS')

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################


# call back
app.layout = dbc.Container([
    html.H1(
        children=[
            'Dashboard Performance TDM'
        ],
        className='text-center mb-4',
        style={
            "font-weight": "bold",
            "color": "white",
            "background-color": "#003B34",
            "padding": "20px"
        }
    ),

############################################################ Dropdown 1 #################################################################
    # Dropdown para escolher a linha

    dbc.Row([
        dbc.Col([
            html.Label('Linha:', style={"font-weight": "bold"}),
            dbc.Select(
                id='lista_linhas',
                value='TODAS AS LINHAS',                    
                options=[{'label': i, 'value': i} for i in opcoes_CODLINLIN],
                style={'width': '100%', 'margin': '10px 0 10px 0', 'border-radius': '10px'}
            ),
        ], width=2),

        dbc.Col([
            html.Label('Cliente:', style={"font-weight": "bold"}),
            dbc.Select(
                id="select_clientes",
                value='TODOS OS CLIENTES',
                options=[{'label': i, 'value': i} for i in todos_clientes_drop2],
                style={'width': '100%', 'margin': '10px 0 10px 10px', 'border-radius': '10px'}
            ),
        ], width=2),

        dbc.Col([
            html.Label('Filial:', style={"font-weight": "bold"}),
            dbc.Select(
                id="select_fil",
                value='TODAS AS FILIAIS',
                options=[{'label': i, 'value': i} for i in todas_filiais_drop3],
                style={'width': '100%', 'margin': '10px 0 10px 0', 'border-radius': '10px'}
            ),
        ], width=2),

        dbc.Col([
            html.Label('Ponto Inicial:', style={"font-weight": "bold"}),
            dbc.Select(
                id="select_ponto_ini",
                value='TODOS',
                options=[{'label': i, 'value': i} for i in pontos_iniciais_drop4],
                style={'width': '100%', 'margin': '10px 0 10px 0', 'border-radius': '10px'}
            ),
        ], width=2),

        dbc.Col([
            html.Label('Ponto Final:', style={"font-weight": "bold"}),
            dbc.Select(
                id="select_ponto_fim",
                value='TODOS',
                options=[{'label': i, 'value': i} for i in pontos_finais_drop5],
                style={'width': '100%', 'margin': '10px 0 10px 0', 'border-radius': '10px'}
            ),
        ], width=2),


        dbc.Col([
            html.Label('Data:', style={"font-weight": "bold"}),

                dcc.DatePickerSingle(
                    id='dropdown_data',
                    date='2024-01-01',                    
                    display_format='YYYY-MM-DD',
                    className='rounded-border',
                    style={'width': '100%'}
                ),
        ], width=2),

    ], justify='center', align='center'),

    ############################################################## Cards ###################################################################
    dbc.Row([
        dbc.Col(
            dbc.Card(
                id='card_fat_pot_perdido',
                children=[
                    dbc.CardHeader("Potencial Perdido", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'R$ {faturamento_potencial_perdido_card1_formatado}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", 'text-align': 'center'}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}
            ),

        ),

        dbc.Col(
            dbc.Card(
                id='card_fat_real',
                children=[
                    dbc.CardHeader("Faturamento Real", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{faturamento_real_card8}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),

        dbc.Col(
            dbc.Card(
                id='card_declinadas_cliente',
                children=[
                    dbc.CardHeader("Canceladas Cliente", style={"font-size": "0.7rem", "font-weight": "bold", 'text-align': 'center'}),
                    dbc.CardBody([
                        html.H4(f'{PCs_declinadas_cliente_card2}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", 'text-align': 'center'}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_declinada_atendimento',
                children=[
                    dbc.CardHeader("Cargas Falta Atendimento", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_declinadas_atendimento_card3}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_CARGA RECUSADA',
                children=[
                    dbc.CardHeader("Cargas Recusadas", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_carga_recusada_card4}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),

        dbc.Col(
            dbc.Card(
                id='card_pc_cadastrada',
                children=[
                    dbc.CardHeader("Cargas em Aberto", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_cadastradas_card6}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),

        dbc.Col(
            dbc.Card(
                id='card_pc_em_atraso',
                children=[
                    dbc.CardHeader("Cargas em Atraso", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_em_atraso_card7}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),

        dbc.Col(
            dbc.Card(
                id='card_pc_total',
                children=[
                    dbc.CardHeader("Todas as Cargas no Sistema", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_totais_card5}', className="card-title", style={"font-size": "0.7rem", "font-weight": "bold", "text-align": "center"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "8rem", "width": "11rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),



    ], className='mt-4'),

############################################################ Gráfico 1, 4 e 5 ##################################################################
    dbc.Row([
        # Primeiro gráfico e dropdown sobreposto
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='grafico_situac',
                    figure=fig,
                    style={'width': '100%', 'height': '70vh'}
                ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=8,
            className='mt-4',
        ),

        # Quarto gráfico
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='grafico_cliente',
                    figure=fig4,
                    style={'width': '100%', 'height': '70vh'} 
                ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=4,  # Largura da coluna do quarto gráfico
            className='mt-4',
        ),
    ]),
        # Quinto grafico
    dbc.Row([
        dbc.Col(
            html.Div(
            dcc.Graph(
                id='grafico_quantidade_cliente',
                figure=fig5,
                style={'width': '100%', 'height': '100vh'} 
            ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=6,  # Largura da coluna do quinto gráfico
            className='mt-4',
        ),

        dbc.Col(
            html.Div(
            dcc.Graph(
                id='grafico_fat_poten_perdido_cli',
                figure=fig3,
                style={'width': '100%', 'height': '100vh'}
            ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=6,
            className='mt-4',
        ),
    ], className='mt-4'),  # Margem superior para separar os gráficos


############################################################ Gráfico 2 ##################################################################
        # Segundo gráfico
    dbc.Row([
        dbc.Col(
            html.Div(
            dcc.Graph(
                id='grafico_fat_cli',
                figure=fig2,
                style={'width': '100%', 'height': '90vh', 'margin': '0px 0px 0px 0px'}
            ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
        ),
    ], className='mt-4'),  # Margem superior para separar os gráficos

    dbc.Row([
        dbc.Col(
            html.Div(
            dcc.Graph(
                id='grafico_quantidade_pc_atrasado',
                figure=fig6,
                style={'width': '100%', 'height': '100vh'} 
            ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=6,  # Largura da coluna do quinto gráfico
            className='mt-4',
        ),

        dbc.Col(
            html.Div(
            dcc.Graph(
                id='grafico_quantidade_pc_em_aberto',
                figure=fig7,
                style={'width': '100%', 'height': '100vh'} 
            ),
                style={'borderRadius': '20px', 'overflow': 'hidden'},
            ),
            width=6,  # Largura da coluna do quinto gráfico
            className='mt-4',
        ),
    ]),


], fluid=True, style={"backgroundColor":  "#F2F2F2"})

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################




#######################################################################################################################################
# Gráfico 1

@app.callback(
    Output('grafico_situac', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_output(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:

        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        situacoes_CODLINLIN = np.array(['Atendido', 'Cadastradas', 'Em atendimento', 'CANCELADO - CLIENTE', 'DECLINADO - FALTA ATENDIMENTO', 'CARGA RECUSADA'])

        quantidades_CODLINLIN = [
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'B'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'D'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'M'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 22].shape[0],         
            tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 21].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 23].shape[0]
                         
        ]

        fig = px.pie(names=situacoes_CODLINLIN, values=quantidades_CODLINLIN, title='Distribuição das Situações')
        fig.update_traces(
            textposition='auto', 
            textinfo='value', 
            outsidetextfont=dict(size=20), 
            insidetextfont=dict(size=30)
        )  # Define para mostrar os valores

        return fig

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
#Card 1
@app.callback(
    Output('card_fat_pot_perdido', 'children'),
    [        
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card1(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data','lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_copia = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        tabela_filtrada_final_copia.to_csv('tabela_card1.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_card1.csv", sep=";", decimal=",")

        tabela_filtrada_final['TOTALFRETE'] = pd.to_numeric(tabela_filtrada_final['TOTALFRETE'], errors='coerce')
        totfre_total_card1 = tabela_filtrada_final['TOTALFRETE'].sum()
        #print(totfre_total_card1)
        PCs_baixadas_card1 = tabela_filtrada_final['TOTALFRETE'].notnull().sum()

        PCs_carga_recusada_card1 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 23].shape[0]
        PCs_cancelado_cliente_card1 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 22].shape[0]
        PCs_declinada_atendimento_card1 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 21].shape[0]
        PCs_declinadas_card1 = int(PCs_carga_recusada_card1) + int(PCs_cancelado_cliente_card1) + int(PCs_declinada_atendimento_card1)
        #print(PCs_declinadas_card1)

        faturamento_potencial_perdido__noformat_card1 = media_global_output_card1 * PCs_declinadas_card1
        faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido__noformat_card1, 2)

        faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido_card1, 2)

        faturamento_potencial_perdido_card1_formatado = locale.format_string('%.2f', faturamento_potencial_perdido_card1, grouping=True)

        card_content1 = [
                    dbc.CardHeader("Potencial Perdido", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'R$ {faturamento_potencial_perdido_card1_formatado}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'})
                    ])
        ]

        return card_content1

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate



#######################################################################################################################################
# Card 2
@app.callback(
    Output('card_declinadas_cliente', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card2(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]


        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_declinadas_cliente_card2 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'] == 22].shape[0]

        #print(PCs_declinadas_cliente_card2)

        card_content2 = [
            dbc.CardHeader("Canceladas Cliente", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'}),
            dbc.CardBody([
                html.H4(f'{PCs_declinadas_cliente_card2}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'}),
            ]),
        ]

        return card_content2

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 3

@app.callback(
    Output('card_declinada_atendimento', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card3(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_declinadas_atendimento_card3 = (tabela_filtrada_final['CODMTC'] == 21).sum()


        card_content3 = [
            dbc.CardHeader("Cargas Falta Atendimento", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{PCs_declinadas_atendimento_card3}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content3

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 4

@app.callback(
    Output('card_CARGA RECUSADA', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card4(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]
        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_carga_recusada_card4  = (tabela_filtrada_final['CODMTC'] == 23).sum()



        card_content3 = [
            dbc.CardHeader("Cargas Recusadas", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{PCs_carga_recusada_card4}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content3

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 5

@app.callback(
    Output('card_pc_total', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card5(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]



        PCs_totais_card5 = tabela_filtrada_final.shape[0]


        card_content5 = [
            dbc.CardHeader("Todas as Cargas no Sistema", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{PCs_totais_card5}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content5

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


#######################################################################################################################################
# Card 6

@app.callback(
    Output('card_pc_cadastrada', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card6(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]



        PCs_cadastradas_card6 = tabela_filtrada_final[(tabela_filtrada_final['CTE'].isnull()) & (tabela_filtrada_final['SITUAC'].isin(['D', 'M']))].shape[0]
        

        card_content6 = [
            dbc.CardHeader("Cargas em Aberto", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{PCs_cadastradas_card6}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content6

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 7

@app.callback(
    Output('card_pc_em_atraso', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card7(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]


        tabela_filtrada_final['DATRET'] = pd.to_datetime(tabela_filtrada_final['DATRET'], errors='coerce')

        # Filtrando os dados conforme as condições da sua consulta SQL
        filtered_df = tabela_filtrada_final[(tabela_filtrada_final['DATRET'].notnull()) & (tabela_filtrada_final['DATRET'] < datetime.now()) & (tabela_filtrada_final['SITUAC'].isin(['D', 'M'])) & (tabela_filtrada_final['CTE'].isnull())]

        # Obtendo o total de registros
        PCs_em_atraso_card7 = len(filtered_df)



        card_content6 = [
            dbc.CardHeader("Cargas em Atraso", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{PCs_em_atraso_card7}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content6

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 7

@app.callback(
    Output('card_fat_real', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card7(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        df_filtrado_card8 = df[(df['TOTALFRETE'].notnull()) & (df['SITUAC'].isin(['D', 'M', 'B']))]

        faturamento_real_card8 = df_filtrado_card8['TOTALFRETE'].sum()

        faturamento_real_card8 = locale.format_string('%.2f', faturamento_real_card8, grouping=True)

        card_content7 = [
            dbc.CardHeader("Faturamento Real", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{faturamento_real_card8}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content7

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


#######################################################################################################################################
# Gráfico 2

@app.callback(
    Output('grafico_fat_cli', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value'),
    ],
    allow_duplicate=True
)

def update_graf2(value_data, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_fil[
            tabela_filtrada_fil.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        tabela_filtrada_final_fatiada.to_csv('tabela_grafico2.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico2.csv", sep=";", decimal=",")


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
            PCs_baixadas_graf2.append(tab_tomador_graf2['TOTALFRETE'].notnull().sum())
            i+=1

        #print(f'PCs baixadas: {PCs_baixadas_graf2}')

        fat_cliente_graf2 = []

        for tomador in tomadores_graf2:
            tabela_filtrada_final.loc[:, 'TOTALFRETE'] = pd.to_numeric(tabela_filtrada_final['TOTALFRETE'], errors='coerce')
            totfre_total_graf2 = tabela_filtrada_final[tabela_filtrada_final['TOMADOR'] == tomador]['TOTALFRETE'].sum()
            fat_cliente_graf2.append(totfre_total_graf2)

        fat_cliente_graf2 = [round(valor, 2) for valor in fat_cliente_graf2]

        fat_cliente_graf2_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in fat_cliente_graf2]

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

        faturamento_potencial_graf2_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in faturamento_potencial_graf2]

        #print(media_cliente_graf2)
        #print(faturamento_potencial_graf2)

        fig2 = go.Figure(
            data=[
            go.Bar(
                x=tomadores_graf2,
                y=faturamento_potencial_graf2,
                name='Faturamento Potencial',  # Nome da primeira barra
                opacity=0.7,
                offsetgroup = 1,
                text=faturamento_potencial_graf2_formatado,  # Adicionando valores de texto acima das barras
                textposition='inside',  # Posição automática do texto
                textfont=dict(size=14),
            ),

            go.Bar(
                x=tomadores_graf2,
                y=fat_cliente_graf2,
                name='Faturamento Real',
                opacity=0.7,
                offsetgroup = 2,
                text=fat_cliente_graf2_formatado,  # Adicionando valores de texto acima das barras
                textposition='inside', 
                textfont=dict(size=14),
            ),
            ]
        )

        fig2.update_layout(
            title='Faturamento (TOP 10)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )
        return fig2

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


#######################################################################################################################################
# Gráfico 3

@app.callback(
    Output('grafico_fat_poten_perdido_cli', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_graf3(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        tabela_filtrada_final_fatiada.to_csv('tabela_grafico3.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico3.csv", sep=";", decimal=",")


        status_desejados_graf3 = [21,22,23]
        tabela_filtrada_final_filtrado_graf3 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'].isin(status_desejados_graf3)]

        # Agrupar por TOMADOR e contar a ocorrência de cada STATUS
        contagem_por_tomador_graf3 = tabela_filtrada_final_filtrado_graf3.groupby('TOMADOR')['CODMTC'].value_counts().unstack(fill_value=0)

        # Calcular o total de ocorrências para cada TOMADOR
        contagem_por_tomador_graf3['TOTAL'] = contagem_por_tomador_graf3.sum(axis=1)

        # Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
        top_5_tomadores_graf3 = contagem_por_tomador_graf3.sort_values(by='TOTAL', ascending=False).head(5)

        # Preencher valores ausentes com 0
        top_5_tomadores_graf3 = top_5_tomadores_graf3.fillna(0)

        tomadores_graf3 = top_5_tomadores_graf3.index.values


        media_cliente_graf3 = media_cliente_graf2
        tomadores_graf3 = tomadores_graf3

        PCs_declinadas_graf3 = []
        PCs_carga_recusada_graf3 = []
        PCs_declinada_atendimento_graf3 = []
        PCs_declinada_cliente_graf3 = []
        i=0
        while(i<len(tomadores_graf3)):
            tab_tomador_graf3 = tabela_filtrada_final.loc[tabela_filtrada_final['TOMADOR']== tomadores_graf3[i], :]
            PCs_carga_recusada_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 23].shape[0])
            PCs_declinada_cliente_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 22].shape[0])
            PCs_declinada_atendimento_graf3.append(tab_tomador_graf3[tab_tomador_graf3['CODMTC'] == 21].shape[0])
            PCs_declinadas_graf3.append(PCs_carga_recusada_graf3[i] + PCs_declinada_cliente_graf3[i] + PCs_declinada_atendimento_graf3[i])
            i+=1

        faturamento_potencial_perdido_graf3 = []
        i=0
        while(i<len(tomadores_graf3)):
            faturamento_potencial_perdido_graf3.append(media_cliente_graf3[i] * PCs_declinadas_graf3[i])
            i+=1

        faturamento_potencial_perdido_graf3 = [round(valor, 2) for valor in faturamento_potencial_perdido_graf3]

        faturamento_potencial_perdido_graf3_formatado = [locale.format_string('%.2f', valor, grouping=True) for valor in faturamento_potencial_perdido_graf3]


        fig3 = go.Figure(
            go.Bar(
                x=tomadores_graf3,
                y=faturamento_potencial_perdido_graf3,
                name='Faturamento potencial perdido por cliente',  # Nome da primeira barra
                opacity=0.7,
                text = faturamento_potencial_perdido_graf3_formatado,
                textposition='inside', 
                textfont=dict(size=14),
            )
        )

        fig3.update_layout(
            title='Faturamento Potencial Perdido (TOP 5)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )

        return fig3

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Gráfico 4

@app.callback(
    Output('grafico_cliente', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_graf4(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        tabela_filtrada_final_fatiada.to_csv('tabela_grafico4.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico4.csv", sep=";", decimal=",")


        resultado_graf4 = tabela_filtrada_final.groupby('TOMADOR').size().reset_index(name='frequencia')
        resultado_graf4 = resultado_graf4.sort_values(by='frequencia', ascending=False).head(1)
        tomadores_graf4 = resultado_graf4['TOMADOR'].tolist()
        qtd_total_PC_cliente_graf4 = resultado_graf4['frequencia'].tolist()

        #print(f'Tomadores: {tomadores_graf4}')
        #print(f'Total PCs clientes: {qtd_total_PC_cliente_graf4}')

        PCs_baixadas_graf4 = []
        i=0

        while(i<len(tomadores_graf4)):
            tab_tomador_graf4 = tabela_filtrada_final.loc[tabela_filtrada_final['TOMADOR']== tomadores_graf4[i], :]
            PCs_baixadas_graf4.append(tab_tomador_graf4['TOTALFRETE'].notnull().sum())
            i+=1

        #print(f'PCs baixadas: {PCs_baixadas_graf4}')

        fat_cliente_graf4 = []

        for tomador in tomadores_graf4:
            tabela_filtrada_final.loc[:, 'TOTALFRETE'] = pd.to_numeric(tabela_filtrada_final['TOTALFRETE'], errors='coerce')
            totfre_total_graf4 = tabela_filtrada_final[tabela_filtrada_final['TOMADOR'] == tomador]['TOTALFRETE'].sum()
            fat_cliente_graf4.append(totfre_total_graf4)

        fat_cliente_graf4 = [round(valor, 2) for valor in fat_cliente_graf4]

        #print(fat_cliente_graf4)

        i=0
        media_cliente_graf4 = []
        faturamento_potencial_graf4 = []
        while(i<len(tomadores_graf4)):
            media_cli_graf4 = fat_cliente_graf4[i]/PCs_baixadas_graf4[i]
            media_cliente_graf4.append(media_cli_graf4)
            fat_pot_graf4 = (fat_cliente_graf4[i]/PCs_baixadas_graf4[i]) * qtd_total_PC_cliente_graf4[i]
            faturamento_potencial_graf4.append(fat_pot_graf4)
            i+=1

        media_cliente_graf4 = [round(valor, 2) for valor in media_cliente_graf4]
        faturamento_potencial_graf4 = [round(valor, 2) for valor in faturamento_potencial_graf4]

        fig4 = go.Figure(
            data=[
                go.Bar(
                    x=tomadores_graf4,
                    y=faturamento_potencial_graf4,
                    name='Faturamento Potencial',  # Nome da primeira barra
                    opacity=0.7,
                    text = faturamento_potencial_graf4_formatado,
                    textposition='inside', 
                    textfont=dict(size=16),
                ),
                go.Bar(
                    x=tomadores_graf4,
                    y=fat_cliente_graf4,
                    text = fat_cliente_graf4_formatado,
                    textposition='inside', 
                    textfont=dict(size=16),
                    name='Faturamento Real',
                ),

            ]
        )

        fig4.update_layout(
            title='Faturamento Por Cliente',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )
        return fig4

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Gráfico 5

@app.callback(
    Output('grafico_quantidade_cliente', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_graf5(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]
        tabela_filtrada_final_fatiada.to_csv('tabela_grafico5.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico5.csv", sep=";", decimal=",")
 
        status_desejados_graf5 = [21,22,23]
        df_filtrado_graf5 = tabela_filtrada_final[tabela_filtrada_final['CODMTC'].isin(status_desejados_graf5)]

        # Agrupar por TOMADOR e contar a ocorrência de cada STATUS
        contagem_por_tomador_graf5 = df_filtrado_graf5.groupby('TOMADOR')['CODMTC'].value_counts().unstack(fill_value=0)

        # Calcular o total de ocorrências para cada TOMADOR
        contagem_por_tomador_graf5['TOTAL'] = contagem_por_tomador_graf5.sum(axis=1)

        # Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
        top_5_tomadores_graf5 = contagem_por_tomador_graf5.sort_values(by='TOTAL', ascending=False).head(5)

        # Preencher valores ausentes com 0
        top_5_tomadores_graf5 = top_5_tomadores_graf5.fillna(0)

        # Verificar se a coluna existe antes de acessá-la e atribuir 0 se não existir
        carga_recusada_graf5 = top_5_tomadores_graf5[23].values if 23 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
        cancelado_cliente_graf5 = top_5_tomadores_graf5[22].values if 22 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
        declinado_falta_atendimento_graf5 = top_5_tomadores_graf5[21].values if 21 in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)

        # Extrair os resultados em vetores
        tomadores_graf5 = top_5_tomadores_graf5.index.values
        #print(tomadores_graf5)
        total_ocorrencias_graf5 = top_5_tomadores_graf5['TOTAL'].values
        #print(total_ocorrencias_graf5)
        fig5 = go.Figure(
            data=[
                go.Bar(
                    x=tomadores_graf5,
                    y=total_ocorrencias_graf5,
                    name='Quantidade de PC Cancelada',  # Nome da primeira barra
                    opacity=0.7,
                    text = total_ocorrencias_graf5,
                    textposition='inside', 
                    textfont=dict(size=18),
                )
            ]
        )

        fig5.update_layout(
            title='Quantidade de Carga Cancelada (TOP 5)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )
        
        return fig5

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


#######################################################################################################################################
# Gráfico 6

@app.callback(
    Output('grafico_quantidade_pc_atrasado', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_graf7(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]
        tabela_filtrada_final_fatiada.to_csv('tabela_grafico5.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico5.csv", sep=";", decimal=",")
 


        tabela_filtrada_final['DATRET'] = pd.to_datetime(tabela_filtrada_final['DATRET'], errors='coerce')

        filtered_df = tabela_filtrada_final[(tabela_filtrada_final['DATRET'].notnull()) & (tabela_filtrada_final['DATRET'] < datetime.now()) & (tabela_filtrada_final['SITUAC'].isin(['D', 'M'])) & (tabela_filtrada_final['CTE'].isnull())]

        # Obtendo o total de registros
        pcs_em_atraso_graf6 = filtered_df

        # Agrupa por cliente e conta as prescrições de crédito em atraso para cada cliente
        pcs_por_cliente_graf6 = pcs_em_atraso_graf6.groupby('TOMADOR').size().reset_index(name='PCS_EM_ATRASO_POR_CLIENTE')

        if pcs_por_cliente_graf6.empty:
            pcs_por_cliente_graf6 = pd.DataFrame({'TOMADOR': [], 'PCS_EM_ATRASO_POR_CLIENTE': [0]})

        # Ordena em ordem decrescente e seleciona os top 5
        top5_pcs_por_cliente_graf6 = pcs_por_cliente_graf6.sort_values(by='PCS_EM_ATRASO_POR_CLIENTE', ascending=False).head(5)

        # Obtém os top 5 tomadores e resultados
        top5_tomadores_graf6 = top5_pcs_por_cliente_graf6['TOMADOR'].to_list()
        top5_resultados_por_cliente_graf6 = top5_pcs_por_cliente_graf6['PCS_EM_ATRASO_POR_CLIENTE'].to_list()

        # Exibe os top 5 resultados
        # print(top5_tomadores_graf6)
        # print(top5_resultados_por_cliente_graf6)

        fig6 = go.Figure(
            data=[
                go.Bar(
                    x=top5_tomadores_graf6,
                    y=top5_resultados_por_cliente_graf6,
                    name='Quantidade de PC Cancelada',  # Nome da primeira barra
                    opacity=0.7,
                    text = top5_resultados_por_cliente_graf6,
                    textposition='inside', 
                    textfont=dict(size=18),
                )
            ]
        )

        fig6.update_layout(
            title='Quantidade de Carga em Atraso (TOP 5)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )

        
        return fig6

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Gráfico 7

@app.callback(
    Output('grafico_quantidade_pc_em_aberto', 'figure'),
    [
        Input('dropdown_data', 'date'),
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_graf7(value_data, value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

        if value_data == '2024-01-01':
            tabela_filtrada_data = df
        else: 
            tabela_filtrada_data = df.loc[df['DATINC'] >= value_data]

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]

        if value_fil == "TODAS AS FILIAIS":
            tabela_filtrada_fil = df
        else:
            value_fil_num = int(value_fil)
            tabela_filtrada_fil = df.loc[df['FILPC'] == value_fil_num]

        if value_ponto_ini == 'TODOS':
            tabela_filtrada_ponto_ini = df
        else:
            tabela_filtrada_ponto_ini = df.loc[df['PONTOINI'] == value_ponto_ini]

        if value_ponto_fim == 'TODOS':
            tabela_filtrada_ponto_fim = df
        else:
            tabela_filtrada_ponto_fim = df.loc[df['PONTOFIM'] == value_ponto_fim] 
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_linhas[
            tabela_filtrada_linhas.index.isin(tabela_filtrada_data.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]
        tabela_filtrada_final_fatiada.to_csv('tabela_grafico5.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico5.csv", sep=";", decimal=",")
 
        df_filtrado_graf7 = tabela_filtrada_final[(tabela_filtrada_final['CTE'].isnull()) & (tabela_filtrada_final['SITUAC'].isin(['D', 'M']))]
        pcs_por_cliente_graf7 = df_filtrado_graf7.groupby('TOMADOR').size().reset_index(name='PCs_em_aberto_por_cliente')
        top5_pcs_por_cliente_graf7 = pcs_por_cliente_graf7.sort_values(by='PCs_em_aberto_por_cliente', ascending=False).head(5)

        # Obtém os top 5 tomadores e resultados
        top5_tomadores_graf7 = top5_pcs_por_cliente_graf7['TOMADOR'].to_list()
        top5_resultados_por_cliente_graf7 = top5_pcs_por_cliente_graf7['PCs_em_aberto_por_cliente'].to_list()

        fig7 = go.Figure(
            data=[
                go.Bar(
                    x=top5_tomadores_graf7,
                    y=top5_resultados_por_cliente_graf7,
                    name='Quantidade de PC Cancelada',  # Nome da primeira barra
                    opacity=0.7,
                    text = top5_resultados_por_cliente_graf7,
                    textposition='inside', 
                    textfont=dict(size=18),
                )
            ]
        )

        fig7.update_layout(
            title='Quantidade de Carga em Aberto (TOP 5)',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )

        
        return fig7

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate



if __name__ == '__main__':
    app.run_server(host='192.168.0.24', port=2500,debug=True)