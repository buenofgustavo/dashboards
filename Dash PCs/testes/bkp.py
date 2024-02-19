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

##################################################################################################################
# GRÁFICO 1

situacoes_CODLINLIN = np.array(['Atendido', 'Cadastrado', 'Em atendimento', 'CANCELADO - CLIENTE', 'DECLINADO - FALTA ATENDIMENTO', 'CARGA RECUSADA'])

quantidades_CODLINLIN = [
    df[df['SITUAC'] == 'B'].shape[0],
    df[df['SITUAC'] == 'D'].shape[0],
    df[df['SITUAC'] == 'M'].shape[0],
    df[df['STATUS'] == 'CANCELADO - CLIENTE'].shape[0],
    df[df['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0],
    df[df['STATUS'] == 'CARGA RECUSADA'].shape[0]
]


fig = px.pie(names=situacoes_CODLINLIN, values=quantidades_CODLINLIN, title='Distribuição das Situações')
fig.update_traces(textposition='inside', textinfo='value')  # Define para mostrar os valores


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
    PCs_baixadas_graf2.append(tab_tomador_graf2[tab_tomador_graf2['SITUAC'] == 'B'].shape[0])
    i+=1

#print(f'PCs baixadas: {PCs_baixadas_graf2}')

fat_cliente_graf2 = []

for tomador in tomadores_graf2:
    df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
    totfre_total_graf2 = df[df['TOMADOR'] == tomador]['TOTALFRETE'].sum()
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


#######################################################################################################################################
# Gráfico 3

media_cliente_graf3 = media_cliente_graf2
tomadores_graf3 = tomadores_graf2

PCs_declinadas_graf3 = []
PCs_carga_recusada_graf3 = []
PCs_declinada_atendimento_graf3 = []
PCs_declinada_cliente_graf3 = []
i=0
while(i<len(tomadores_graf3)):
    tab_tomador_graf3 = df.loc[df['TOMADOR']== tomadores_graf3[i], :]
    PCs_carga_recusada_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'CARGA RECUSADA'].shape[0])
    PCs_declinada_cliente_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'CANCELADO - CLIENTE'].shape[0])
    PCs_declinada_atendimento_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0])
    PCs_declinadas_graf3.append(PCs_carga_recusada_graf3[i] + PCs_declinada_cliente_graf3[i] + PCs_declinada_atendimento_graf3[i])
    i+=1

faturamento_potencial_perdido_graf3 = []
i=0
while(i<len(tomadores_graf3)):
    faturamento_potencial_perdido_graf3.append(media_cliente_graf3[i] * PCs_declinadas_graf3[i])
    i+=1

faturamento_potencial_perdido_graf3 = [round(valor, 2) for valor in faturamento_potencial_perdido_graf3]


fig3 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf3,
            y=faturamento_potencial_perdido_graf3,
            name='Faturamento potencial perdido por cliente',  # Nome da primeira barra
            opacity=0.7
        )
    ]
)

fig3.update_layout(
    title='Faturamento Potencial Perdido',  # Título do gráfico
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
    PCs_baixadas_graf4.append(tab_tomador_graf4[tab_tomador_graf4['SITUAC'] == 'B'].shape[0])
    i+=1

#print(f'PCs baixadas: {PCs_baixadas_graf4}')

fat_cliente_graf4 = []

for tomador in tomadores_graf4:
    df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
    totfre_total_graf4 = df[df['TOMADOR'] == tomador]['TOTALFRETE'].sum()
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

#print(media_cliente_graf4)
#print(faturamento_potencial_graf4)

fig4 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf4,
            y=faturamento_potencial_graf4,
            name='Faturamento Potencial',  # Nome da primeira barra
            opacity=0.7
        ),
        go.Bar(
            x=tomadores_graf4,
            y=fat_cliente_graf4,

            name='Faturamento Real'
        ),

    ]
)

fig4.update_layout(
    title='Faturamento Por cliente',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)

#######################################################################################################################################
# Gráfico 5 - Quantidade PCs Cliente 

status_desejados_graf5 = ["CARGA RECUSADA", "CANCELADO - CLIENTE", "DECLINADO - FALTA ATENDIMENTO"]
df_filtrado_graf5 = df[df['STATUS'].isin(status_desejados_graf5)]

# Agrupar por TOMADOR e contar a ocorrência de cada STATUS
contagem_por_tomador_graf5 = df_filtrado_graf5.groupby('TOMADOR')['STATUS'].value_counts().unstack(fill_value=0)

# Calcular o total de ocorrências para cada TOMADOR
contagem_por_tomador_graf5['TOTAL'] = contagem_por_tomador_graf5.sum(axis=1)

# Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
top_5_tomadores_graf5 = contagem_por_tomador_graf5.sort_values(by='TOTAL', ascending=False).head(5)

# Preencher valores ausentes com 0
top_5_tomadores_graf5 = top_5_tomadores_graf5.fillna(0)

# Verificar se a coluna existe antes de acessá-la e atribuir 0 se não existir
carga_recusada_graf5 = top_5_tomadores_graf5['CARGA RECUSADA'].values if 'CARGA RECUSADA' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
cancelado_cliente_graf5 = top_5_tomadores_graf5['CANCELADO - CLIENTE'].values if 'CANCELADO - CLIENTE' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
declinado_falta_atendimento_graf5 = top_5_tomadores_graf5['DECLINADO - FALTA ATENDIMENTO'].values if 'DECLINADO - FALTA ATENDIMENTO' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)

# Extrair os resultados em vetores
tomadores_graf5 = top_5_tomadores_graf5.index.values
total_ocorrencias_graf5 = top_5_tomadores_graf5['TOTAL'].values

fig5 = go.Figure(
    data=[
        go.Bar(
            x=tomadores_graf5,
            y=total_ocorrencias_graf5,
            name='Quantidade de PC Cancelada',  # Nome da primeira barra
            opacity=0.7
        )
    ]
)

fig5.update_layout(
    title='Quantidades de PCs Canceladas',  # Título do gráfico
    title_font_size=20,  # Tamanho da fonte do título (opcional)
    title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
    title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
    # Você pode ajustar a posição e o tamanho do título conforme necessário
)



#######################################################################################################################################
# Card 1

df['TOTALFRETE'] = pd.to_numeric(df['TOTALFRETE'], errors='coerce')
totfre_total_card1 = df['TOTALFRETE'].sum()
#print(totfre_total_card1)

PCs_baixadas_card1 = df[df['SITUAC'] == 'B'].shape[0]

#print(PCs_baixadas_card1)

PCs_carga_recusada_card1 = df[df['STATUS'] == 'CARGA RECUSADA'].shape[0]
PCs_declinada_cliente_card1 = df[df['STATUS'] == 'CANCELADO - CLIENTE'].shape[0]
PCs_declinada_atendimento_card1 = df[df['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0]
PCs_declinadas_card1 = int(PCs_carga_recusada_card1) + int(PCs_declinada_cliente_card1) + int(PCs_declinada_atendimento_card1)
#print(PCs_declinadas_card1)

faturamento_potencial_perdido__noformat_card1 = (totfre_total_card1/PCs_baixadas_card1) * PCs_declinadas_card1
faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido__noformat_card1, 2)  
#print(faturamento_potencial_perdido_card1)

#######################################################################################################################################
# Card 2

PCs_declinadas_cliente_card2 = df[df['STATUS'] == 'CANCELADO - CLIENTE'].shape[0]

#######################################################################################################################################
# Card 3

PCs_declinadas_atendimento_card3 = df[df['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0]
#######################################################################################################################################
# Card 4

PCs_carga_recusada_card4 = df[df['STATUS'] == 'CARGA RECUSADA'].shape[0]

#######################################################################################################################################
# Card 5

PCs_totais_card5 = df.shape[0]

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
            html.Label('Data:', style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='dropdown_data',
                date='2024-01-01',                    
                display_format='YYYY-MM-DD',
                className='rounded-border',
                style={'width': '100%', 'margin': '0px 0 0px 0', 'border-radius': '100px'}
            ),
        ], width=2),
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
    ], justify='center', align='center'),

    ############################################################## Cards ###################################################################
    dbc.Row([
        dbc.Col(
            dbc.Card(
                id='card_fat_pot_perdido',
                children=[
                    dbc.CardHeader("Potencial Perdido", style={"font-size": "0.9rem", "font-weight": "bold", "text-align": "center"}),
                    dbc.CardBody([
                        html.H4(f'R$ {faturamento_potencial_perdido_card1}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "15rem", "width": "15rem", "background-color": "#003B34", "border-radius": "10px"}
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_declinadas_cliente',
                children=[
                    dbc.CardHeader("Cargas Declinadas Cliente", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'}),
                    dbc.CardBody([
                        html.H4(f'{PCs_declinadas_cliente_card2}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold", 'text-align': 'center'}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "15rem", "width": "15rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_declinada_atendimento',
                children=[
                    dbc.CardHeader("Cargas Falta Atendimento", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_declinadas_atendimento_card3}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "15rem", "width": "15rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_CARGA RECUSADA',
                children=[
                    dbc.CardHeader("Cargas Recusadas", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_carga_recusada_card4}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "15rem", "width": "15rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
        dbc.Col(
            dbc.Card(
                id='card_pc_total',
                children=[
                    dbc.CardHeader("Cargas Totais", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    dbc.CardBody([
                        html.H4(f'{PCs_totais_card5}', className="card-title", style={"font-size": "0.9rem", "font-weight": "bold"}),
                    ]),
                ],
                className="text-white",
                style={"max-width": "15rem", "width": "15rem", "background-color": "#003B34", "border-radius": "10px"}  # Adicionado estilo fixo e bordas arredondadas
            ),
        ),
    ], className='mt-3'),

############################################################ Gráfico 1, 4 e 5 ##################################################################
    dbc.Row([
        # Primeiro gráfico e dropdown sobreposto
        dbc.Col(
            dcc.Graph(
                id='grafico_situac',
                figure=fig,
                style={'width': '100%', 'height': '70vh', 'margin': '60px 0px 0px 0px'}
            ),
            width=5,  # Largura da coluna do primeiro gráfico
        ),
    ]),
    dbc.Row([
        # Quarto gráfico
        dbc.Col(
            dcc.Graph(
                id='grafico_cliente',
                figure=fig4,
                style={'width': '100%', 'height': '90vh', 'margin': '20px 0px'} 
            ),
            width=4,  # Largura da coluna do quarto gráfico
            className='mt-4',
        ),
    ]),
        # Quinto grafico
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='grafico_quantidade_cliente',
                figure=fig5,
                style={'width': '100%', 'height': '90vh', 'margin': '20px 0px'} 
            ),
            width=3,  # Largura da coluna do quinto gráfico
            className='mt-4',
        ),
    ], className='mt-4'),


############################################################ Gráfico 2 ##################################################################
        # Segundo gráfico
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='grafico_fat_cli',
                figure=fig2,
                style={'width': '100%', 'height': '90vh', 'margin': '0px 0px 0px 0px'}
            ),
        ),
    ], className='mt-4'),  # Margem superior para separar os gráficos

    ############################################################ Gráfico 3 #################################################################
    # Terceiro gráfico
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='grafico_fat_poten_perdido_cli',
                figure=fig3,
                style={'width': '100%', 'height': '90vh', 'margin': '0px 0px 0px 0px'}
            ),
        ),
    ], className='mt-4'),  # Margem superior para separar os gráficos


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
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_output(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        situacoes_CODLINLIN = np.array(['Atendido', 'Cadastrado', 'Em atendimento', 'CANCELADO - CLIENTE', 'DECLINADO - FALTA ATENDIMENTO', 'CARGA RECUSADA'])

        quantidades_CODLINLIN = [
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'B'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'D'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'M'].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['STATUS'] == "CANCELADO - CLIENTE"].shape[0],           
            tabela_filtrada_final[tabela_filtrada_final['STATUS'] == "DECLINADO - FALTA ATENDIMENTO"].shape[0],
            tabela_filtrada_final[tabela_filtrada_final['STATUS'] == "CARGA RECUSADA"].shape[0]                            
        ]

        fig = px.pie(names=situacoes_CODLINLIN, values=quantidades_CODLINLIN, title='Distribuição das Situações')
        fig.update_traces(textposition='inside', textinfo='value')  # Define para mostrar os valores

        return fig

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate

#######################################################################################################################################
# Card 1
@app.callback(
    Output('card_fat_pot_perdido', 'children'),
    [
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card1(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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

        PCs_baixadas_card1 = tabela_filtrada_final[tabela_filtrada_final['SITUAC'] == 'B'].shape[0]

        #print(PCs_baixadas_card1)

        PCs_carga_recusada_card1 = tabela_filtrada_final[tabela_filtrada_final['STATUS'] == 'CARGA RECUSADA'].shape[0]
        PCs_declinada_cliente_card1 = tabela_filtrada_final[tabela_filtrada_final['STATUS'] == 'CANCELADO - CLIENTE'].shape[0]
        PCs_declinada_atendimento_card1 = tabela_filtrada_final[tabela_filtrada_final['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0]
        PCs_declinadas_card1 = int(PCs_carga_recusada_card1) + int(PCs_declinada_cliente_card1) + int(PCs_declinada_atendimento_card1)
        #print(PCs_declinadas_card1)

        faturamento_potencial_perdido__noformat_card1 = (totfre_total_card1/PCs_baixadas_card1) * PCs_declinadas_card1
        faturamento_potencial_perdido_card1 = round(faturamento_potencial_perdido__noformat_card1, 2)  
        #print(faturamento_potencial_perdido_card1)

        card_content1 = [
            dbc.CardHeader("Faturamento Potêncial Perdido"),
            dbc.CardBody([
                html.H4(f'{faturamento_potencial_perdido_card1}', className="card-title"),
            ]),
        ]

        return card_content1

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate



#######################################################################################################################################
# Card 2
@app.callback(
    Output('card_declinadas_cliente', 'children'),
    [
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card2(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_declinadas_cliente_card2 = (tabela_filtrada_final['STATUS'] == 'DECLINADO - CLIENTE').sum()

        #print(PCs_declinadas_cliente_card2)

        card_content2 = [
            dbc.CardHeader("Cargas Declinadas Cliente"),
            dbc.CardBody([
                html.H4(f'{PCs_declinadas_cliente_card2}', className="card-title"),
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
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card3(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_declinadas_atendimento_card3 = (tabela_filtrada_final['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO').sum()


        card_content3 = [
            dbc.CardHeader("Cargas Declinadas Falta Atendimento"),
            dbc.CardBody([
                html.H4(f'{PCs_declinadas_atendimento_card3}', className="card-title"),
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
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card4(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        PCs_carga_recusada_card4  = (tabela_filtrada_final['STATUS'] == 'CARGA RECUSADA').sum()



        card_content3 = [
            dbc.CardHeader("Cargas Recusadas"),
            dbc.CardBody([
                html.H4(f'{PCs_carga_recusada_card4}', className="card-title"),
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
        Input('lista_linhas', 'value'),
        Input('select_clientes', 'value'),
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value')
    ],
    allow_duplicate=True
)

def update_card5(value_linhas, value_clientes, value_fil, value_ponto_ini, value_ponto_fim):

    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_clientes', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:
        if value_linhas == 'TODAS AS LINHAS':
            tabela_filtrada_linhas = df
        else:
            tabela_filtrada_linhas = df.loc[df['LINHA'] == value_linhas]

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
            tabela_filtrada_linhas.index.isin(tabela_filtrada_clientes.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_linhas.index.isin(tabela_filtrada_ponto_fim.index)
        ]



        PCs_totais_card5 = tabela_filtrada_final.shape[0]


        card_content5 = [
            dbc.CardHeader("PCs Totais"),
            dbc.CardBody([
                html.H4(f'{PCs_totais_card5}', className="card-title"),
            ]),
        ]

        return card_content5

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


#######################################################################################################################################
# Gráfico 2

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
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:

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
        tabela_filtrada_final_fatiada = tabela_filtrada_fil[
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


#######################################################################################################################################
# Gráfico 3

@app.callback(
    Output('grafico_fat_poten_perdido_cli', 'figure'),
    [
        Input('select_fil', 'value'),
        Input('select_ponto_ini', 'value'),
        Input('select_ponto_fim', 'value'),
    ],
    allow_duplicate=True
)

def update_graf3(value_fil, value_ponto_ini, value_ponto_fim):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['lista_linhas', 'select_fil', 'select_ponto_ini', 'select_ponto_fim']:

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
        tabela_filtrada_final_fatiada = tabela_filtrada_fil[
            tabela_filtrada_fil.index.isin(tabela_filtrada_fil.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_ini.index) &
            tabela_filtrada_fil.index.isin(tabela_filtrada_ponto_fim.index)
        ]

        tabela_filtrada_final_fatiada.to_csv('tabela_grafico3.csv', sep=';', decimal=',', mode='w', index=False)
        tabela_filtrada_final = pd.read_csv("tabela_grafico3.csv", sep=";", decimal=",")


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

        tabela_filtrada_final = pd.read_csv("tabela_grafico3.csv", sep=";", decimal=",")

        media_cliente_graf3 = media_cliente_graf2
        tomadores_graf3 = tomadores_graf2

        PCs_carga_recusada_graf3 = []
        PCs_declinada_cliente_graf3 = []
        PCs_declinada_atendimento_graf3 = []
        PCs_declinadas_graf3 = []
        i = 0
        while i < len(tomadores_graf3):

            tab_tomador_graf3 = tabela_filtrada_final.loc[tabela_filtrada_final['TOMADOR'] == tomadores_graf3[i], :]
            PCs_carga_recusada_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'CARGA RECUSADA'].shape[0])
            PCs_declinada_cliente_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'CANCELADO - CLIENTE'].shape[0])
            PCs_declinada_atendimento_graf3.append(tab_tomador_graf3[tab_tomador_graf3['STATUS'] == 'DECLINADO - FALTA ATENDIMENTO'].shape[0])

            PCs_declinadas_graf3.append(PCs_carga_recusada_graf3[i] + PCs_declinada_cliente_graf3[i] + PCs_declinada_atendimento_graf3[i])

            i += 1

        #print(PCs_declinadas_graf3)

        faturamento_potencial_perdido_graf3 = []
        i=0
        while(i<len(tomadores_graf3)):
            faturamento_potencial_perdido_graf3.append(media_cliente_graf3[i] * PCs_declinadas_graf3[i])
            i+=1

        faturamento_potencial_perdido_graf3 = [round(valor, 2) for valor in faturamento_potencial_perdido_graf3]


        fig3 = go.Figure(
            data=[
                go.Bar(
                    x=tomadores_graf3,
                    y=faturamento_potencial_perdido_graf3,
                    name='Faturamento potencial perdido por cliente',  # Nome da primeira barra
                    opacity=0.7
                )
            ]
        )

        fig3.update_layout(
            title='Faturamento Potencial Perdido',  # Título do gráfico
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
        Input('select_clientes', 'value'),
    ],
    allow_duplicate=True
)

def update_graf4(value_clientes):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['select_clientes']:

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]
 

        # Aplicando os filtros de linhas, clientes e filiais
        tabela_filtrada_final_fatiada = tabela_filtrada_clientes

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
            PCs_baixadas_graf4.append(tab_tomador_graf4[tab_tomador_graf4['SITUAC'] == 'B'].shape[0])
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
                    opacity=0.7
                ),
                go.Bar(
                    x=tomadores_graf4,
                    y=fat_cliente_graf4,

                    name='Faturamento Real'
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
        Input('select_clientes', 'value'),
    ],
    allow_duplicate=True
)

def update_graf5(value_clientes):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['select_clientes']:

        if value_clientes == 'TODOS OS CLIENTES':
            tabela_filtrada_clientes = df
        else:
            tabela_filtrada_clientes = df.loc[df['TOMADOR'] == value_clientes]
 
        status_desejados_graf5 = ["CARGA RECUSADA", "CANCELADO - CLIENTE", "DECLINADO - FALTA ATENDIMENTO"]
        df_filtrado_graf5 = tabela_filtrada_clientes[tabela_filtrada_clientes['STATUS'].isin(status_desejados_graf5)]

        # Agrupar por TOMADOR e contar a ocorrência de cada STATUS
        contagem_por_tomador_graf5 = df_filtrado_graf5.groupby('TOMADOR')['STATUS'].value_counts().unstack(fill_value=0)

        # Calcular o total de ocorrências para cada TOMADOR
        contagem_por_tomador_graf5['TOTAL'] = contagem_por_tomador_graf5.sum(axis=1)

        # Ordenar os tomadores pelo total em ordem decrescente e pegar os top 5
        top_5_tomadores_graf5 = contagem_por_tomador_graf5.sort_values(by='TOTAL', ascending=False).head(5)

        # Preencher valores ausentes com 0
        top_5_tomadores_graf5 = top_5_tomadores_graf5.fillna(0)

        # Verificar se a coluna existe antes de acessá-la e atribuir 0 se não existir
        carga_recusada_graf5 = top_5_tomadores_graf5['CARGA RECUSADA'].values if 'CARGA RECUSADA' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
        cancelado_cliente_graf5 = top_5_tomadores_graf5['CANCELADO - CLIENTE'].values if 'CANCELADO - CLIENTE' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)
        declinado_falta_atendimento_graf5 = top_5_tomadores_graf5['DECLINADO - FALTA ATENDIMENTO'].values if 'DECLINADO - FALTA ATENDIMENTO' in top_5_tomadores_graf5.columns else [0] * len(top_5_tomadores_graf5)

        # Extrair os resultados em vetores
        tomadores_graf5 = top_5_tomadores_graf5.index.values
        total_ocorrencias_graf5 = top_5_tomadores_graf5['TOTAL'].values

        fig5 = go.Figure(
            data=[
                go.Bar(
                    x=tomadores_graf5,
                    y=total_ocorrencias_graf5,
                    name='Quantidade de PC Cancelada',  # Nome da primeira barra
                    opacity=0.7
                )
            ]
        )

        fig5.update_layout(
            title='Quantidade de PC Cancelada',  # Título do gráfico
            title_font_size=20,  # Tamanho da fonte do título (opcional)
            title_x=0.5,  # Posição horizontal do título (0.5 é centralizado)
            title_y=0.9,  # Posição vertical do título (0.9 fica acima do gráfico)
            # Você pode ajustar a posição e o tamanho do título conforme necessário
        )
        
        return fig5

    # Se o input não for 'lista_linhas', 'select_clientes' ou 'select_filiais', não atualizar o gráfico
    raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(host='192.168.101.165', port=70,debug=True)