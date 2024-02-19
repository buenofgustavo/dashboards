# Card 1

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

df = pd.read_csv("tabela_view.csv", sep=";", decimal=",")

df['STATUS'] = df['STATUS'].str.strip().str.upper()


todos_tomadores_card1 = df['TOMADOR'].unique()

PCs_baixadas_card1 = []
i=0

while(i<len(todos_tomadores_card1)):
    tab_tomador_card1 = df.loc[df['TOMADOR']== todos_tomadores_card1[i], :]
    PCs_baixadas_card1.append(tab_tomador_card1[tab_tomador_card1['SITUAC'] == 'B'].shape[0])
    i+=1


fat_cliente_card1 = []

for tomador in todos_tomadores_card1:
    df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
    totfre_total_card1 = df[(df['TOMADOR'] == tomador) & (df['SITUAC'] == 'B')]['TOTALFRETE'].sum()
    fat_cliente_card1.append(totfre_total_card1)

fat_cliente_card1 = [round(valor, 2) for valor in fat_cliente_card1]

# print('General')
# print(PCs_baixadas_card1[12])
# print(fat_cliente_card1[12])

totfre_total_card1 = df['TOTALFRETE'].sum()
PCs_totais_baixadas_card1 = df[df['SITUAC'] == 'B'].shape[0]

media_global_card1 = totfre_total_card1 / PCs_totais_baixadas_card1

media_cliente_card1 = []

for i in range(len(fat_cliente_card1)):
    if PCs_baixadas_card1[i] != 0:
        media_cliente_card1.append(fat_cliente_card1[i] / PCs_baixadas_card1[i])
    else:
        media_cliente_card1.append(media_global_card1)

media_cliente_card1 = [round(valor, 2) for valor in media_cliente_card1]

# print(todos_tomadores_card1)
# print(media_cliente_card1)

carga_recusada_card1 = df[df['STATUS'] == 'CARGA RECUSADA']
cancelado_cliente_card1 = df[df['STATUS'] == 'CANCELADO - CLIENTE']
declinado_atendimento_card1 = df[df['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO']

# Contar o número de ocorrências para cada cliente
contagem_carga_recusada_card1 = carga_recusada_card1.groupby('TOMADOR').size().reset_index(name='PCs_cargas_recusadas_card1')
contagem_cancelado_cliente_card1 = cancelado_cliente_card1.groupby('TOMADOR').size().reset_index(name='PCs_cancelado_cliente_card1')
contagem_declinado_atendimento_card1 = declinado_atendimento_card1.groupby('TOMADOR').size().reset_index(name='PCs_declinada_atendimento_card1')

tomadores_carga_recusada_card1 = contagem_carga_recusada_card1['TOMADOR'].tolist()
pcs_carga_recusada_card1 = contagem_carga_recusada_card1['PCs_cargas_recusadas_card1'].tolist()

tomadores_cancelado_cliente_card1 = contagem_cancelado_cliente_card1['TOMADOR'].tolist()
pcs_canceladas_cliente_card1 = contagem_cancelado_cliente_card1['PCs_cancelado_cliente_card1'].tolist()

tomadores_declinado_atendimento_card1 = contagem_declinado_atendimento_card1['TOMADOR'].tolist()
pcs_declinado_atendimento_card1 = contagem_declinado_atendimento_card1['PCs_declinada_atendimento_card1'].tolist()

# Exibir os vetores
#print("Tomadores:", tomadores_cancelado_cliente_card1)
#print("PCs_declinadas:", pcs_canceladas_cliente_card1)

#print("Tomadores recusadas:", tomadores_carga_recusada_card1)
#print("Cargas Recusadas:", pcs_carga_recusada_card1)

#print("Tomadores Falta Atendimento:", tomadores_declinado_atendimento_card1)
#print("Cargas Falta Atendimento:", pcs_declinado_atendimento_card1)

quantidade_tomadores_canceladas_card1 = len(pcs_canceladas_cliente_card1)
quantidade_tomadores_recusadas_card1 = len(pcs_carga_recusada_card1)
quantidade_tomadores_falta_atendimento_card1 = len(pcs_declinado_atendimento_card1)

maximo_qnt_tomadores = max(quantidade_tomadores_canceladas_card1, quantidade_tomadores_falta_atendimento_card1, quantidade_tomadores_recusadas_card1)

#print(quantidade_tomadores_canceladas_card1)
#print(quantidade_tomadores_recusadas_card1)
#print(quantidade_tomadores_falta_atendimento_card1)

i=0
j=0
potencial_perdido_cancelado_cliente_card1 = []
while(j<quantidade_tomadores_canceladas_card1):
    i=0
    while(i<len(todos_tomadores_card1)):
        if tomadores_cancelado_cliente_card1[j] == todos_tomadores_card1[i]:
            potencial_perdido_cancelado_cliente_card1.append(pcs_canceladas_cliente_card1[j] * media_cliente_card1[i])

        i+=1
    j+=1
#print(potencial_perdido_cancelado_cliente_card1)

i=0
j=0
potencial_perdido_carga_recusada_cliente_card1 = []
while(j<quantidade_tomadores_recusadas_card1):
    i=0
    while(i<len(todos_tomadores_card1)):
        if tomadores_carga_recusada_card1[j] == todos_tomadores_card1[i]:
            potencial_perdido_carga_recusada_cliente_card1.append(pcs_carga_recusada_card1[j] * media_cliente_card1[i])

        i+=1
    j+=1
#print(potencial_perdido_carga_recusada_cliente_card1)
i=0
j=0
potencial_perdido_declinado_atendimento_cliente_card1 = []
while(j<quantidade_tomadores_falta_atendimento_card1):
    i=0
    while(i<len(todos_tomadores_card1)):
        if tomadores_declinado_atendimento_card1[j] == todos_tomadores_card1[i]:
            potencial_perdido_declinado_atendimento_cliente_card1.append(pcs_declinado_atendimento_card1[j] * media_cliente_card1[i])

        i+=1
    j+=1

#print(potencial_perdido_declinado_atendimento_cliente_card1)

# faturamento_potencial_perdido_card1_noformat = potencial_perdido_cancelado_cliente_card1 + potencial_perdido_carga_recusada_cliente_card1 + potencial_perdido_declinado_atendimento_cliente_card1

# faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido_card1_noformat, 2)
#print(faturamento_potencial_perdido_card1)

i = 0
potencial_total_perdido_carga_recusada_card1 = 0
while(i<quantidade_tomadores_recusadas_card1):
    potencial_total_perdido_carga_recusada_card1 += potencial_perdido_carga_recusada_cliente_card1[i]
    i+=1

i = 0

potencial_total_perdido_cancelado_cliente_card1 = 0
while(i<quantidade_tomadores_canceladas_card1):
    potencial_total_perdido_cancelado_cliente_card1 += potencial_perdido_cancelado_cliente_card1[i]
    i+=1

i=0
potencial_total_perdido_falta_atendimento_card1 = 0
while(i<quantidade_tomadores_falta_atendimento_card1):
    potencial_total_perdido_falta_atendimento_card1 += potencial_perdido_declinado_atendimento_cliente_card1[i]
    i+=1

#print(potencial_total_perdido_cancelado_cliente_card1, potencial_total_perdido_carga_recusada_card1, potencial_total_perdido_falta_atendimento_card1)

faturamento_potencial_perdido_card1 = potencial_total_perdido_cancelado_cliente_card1 + potencial_total_perdido_carga_recusada_card1 + potencial_total_perdido_falta_atendimento_card1

#print(faturamento_potencial_perdido_card1)

