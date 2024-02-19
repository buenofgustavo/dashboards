from alimentadorDeDados import processarArquivo
from selectTodosFuncionarios import selectTodosFuncionarios
from lerArquivos import lerArquivos
from diariasTotaisMensal import soma_diarias_por_parceiro

from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
from dash.dash_table import DataTable
import pandas as pd


todos_funcionarios = []


nome_arquivo = f'zNomesColunas.csv'
df = pd.read_csv(nome_arquivo, sep=";", decimal=",")
#df = df.iloc[:, 1:]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.layout = dbc.Container([
    dbc.Row([

        dbc.Col([
            html.Label('Funcionários:', style={"font-weight": "bold"}),
            dbc.Select(
                id="select_funcionarios",
                
                options=[{'label': i, 'value': i} for i in todos_funcionarios],
                style={'width': '100%', 'margin': '10px 0 10px 10px', 'border-radius': '10px'}
            ),
        ], width=4),

        dbc.Col([
            html.Label('Data:', style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='dropdown_data',
                date='01-01-2024',                    
                display_format='DD-MM-YYYY',
                className='rounded-border',
                style={'width': '100%'}
                    ),
        ], width=2),

        dbc.Button(
            children="Todo o Mês", id="button-ver-todos", className="me-1", n_clicks=0, color="success", 
            style={"margin": "20px","fontSize": "12px", "width": "150px", "height": "50px", "borderRadius": "12px"}
        ),

        dbc.Button(
            children="Diárias de Todos Funcinários", id="button-ver-todas-diarias", className="me-1", n_clicks=0, color="success", 
            style={"margin": "20px","fontSize": "12px", "width": "150px", "height": "50px", "borderRadius": "12px"}
        ),

        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Ler arquivos da pasta")),
            dbc.ModalBody("Foi atualizado com sucesso!"),
        ],
            id="modal-lg",
            size="lg",
            is_open=False,
        ),

        dbc.Button(
            "Ler arquivos da Pasta", id="button-atualizar", className="me-1", n_clicks=0, color="danger", 
            style={"margin": "20px","fontSize": "12px", "width": "100px", "height": "50px", "borderRadius": "12px"}
        ),

    ], className='mt-4'),

    dbc.Row([
        DataTable(
            id='tabela',
            columns=[
                {'name': col, 'id': col} for col in df.columns
            ],
            data=[],
            style_table={'fontFamily': 'Arial, sans-serif'},
            style_cell={'textAlign': 'center', 'fontSize': '12px'}
        ),
    ], className='mt-4'),


dbc.Row([
    dbc.Card(
        id='card_dias_uteis',
        children=[
            dbc.CardHeader("Dias Úteis", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'', className="card-title", style={"font-size": "0.6rem", "font-weight": "bold", 'text-align': 'center'}),
            ]),
        ],
        className="text-black",
        style={"max-width": "7rem", "width": "7rem", "height":"5.5rem", "background-color": "#f2f2f2", "border-radius": "10px", "margin":"20px"}
    ),
    dbc.Card(
        id='card_diarias',
        children=[
            dbc.CardHeader("Diárias", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'', className="card-title", style={"font-size": "0.6rem", "font-weight": "bold", 'text-align': 'center'}),
            ]),
        ],
        className="text-black",
        style={"max-width": "7rem", "width": "7rem", "height":"5.5rem", "background-color": "#F2F2F2", "border-radius": "10px", "margin":"20px", "color": "black"}
        ),

], className='mt-4'),

])

@app.callback(
    Output('tabela', 'data'),
    [
        Input('dropdown_data', 'date'),
        Input('select_funcionarios', 'value'),
        Input('button-ver-todos', 'n_clicks'),
        Input('button-ver-todas-diarias', 'n_clicks'),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)

def update_output(value_data, value_funcionarios, n_clicks, n_clicks_todas_diarias):
    partes_da_data = value_data.split("-")
    mes = partes_da_data[1]
    dia = partes_da_data[2]

    if n_clicks_todas_diarias % 2 != 0:
        nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{mes}mes.csv'
        soma_diarias_por_parceiro(nome_arquivo)
        df_filtrado = pd.read_csv("diariasDoMes.csv", sep=";", decimal=",")
    else:
        if n_clicks % 2 != 0:
            nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{mes}mes.csv'
            df_atualizado = pd.read_csv(nome_arquivo, sep=";", decimal=",")
            df_filtrado = df_atualizado.loc[df_atualizado['Parceiro'] == value_funcionarios]

        else:
            nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{dia}.csv'
            df_atualizado = pd.read_csv(nome_arquivo, sep=";", decimal=",")
            df_filtrado = df_atualizado.loc[df_atualizado['Parceiro'] == value_funcionarios]


    return df_filtrado.to_dict('records')
        

def toggle_modal(n1, is_open):
    if n1:
        processarArquivo()
        return not is_open
    return is_open


app.callback(
    Output("modal-lg", "is_open"),
    Input("button-atualizar", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)


@app.callback(
    Output('card_dias_uteis', 'children'),
    [
        Input('dropdown_data', 'date'),
    ],
    allow_duplicate=True
)

def update_output(value_data):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data']:
            
        partes_da_data = value_data.split("-")
        mes = partes_da_data[1]

        if mes == '01':
            dias_uteis = 22
        if mes == '02':
            dias_uteis = 21
        if mes == '03':
            dias_uteis = 22
        
        card_content1 = [
            dbc.CardHeader("Dias Úteis", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{dias_uteis}', className="card-title", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content1

@app.callback(
    Output('card_diarias', 'children'),
    [
        Input('dropdown_data', 'date'),
        Input('select_funcionarios', 'value'),
        Input('button-ver-todos', 'n_clicks'),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)

def update_output(value_data, value_funcionarios, n_clicks):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['dropdown_data', 'select_funcionarios', 'button-ver-todos']:

        if n_clicks % 2 != 0:
            partes_da_data = value_data.split("-")

            mes = partes_da_data[1]

            nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{mes}mes.csv'
            df_atualizado = pd.read_csv(nome_arquivo, sep=";", decimal=",")
            df_filtrado_fatiada = df_atualizado.loc[df_atualizado['Parceiro'] == value_funcionarios]

            df_filtrado_fatiada.to_csv('zDiariasCard2.csv', sep=';', decimal=',', mode='w', index=False)
            tabela_filtrada_final = pd.read_csv("zDiariasCard2.csv", sep=";", decimal=",")
            quantidade_diarias = tabela_filtrada_final['Diarias'].sum()

        else:

            partes_da_data = value_data.split("-")

            mes = partes_da_data[1]
            dia = partes_da_data[2]

            nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{dia}.csv'
            df_atualizado = pd.read_csv(nome_arquivo, sep=";", decimal=",")
            df_filtrado_fatiada = df_atualizado.loc[df_atualizado['Parceiro'] == value_funcionarios]

            df_filtrado_fatiada.to_csv('zDiariasCard2.csv', sep=';', decimal=',', mode='w', index=False)
            tabela_filtrada_final = pd.read_csv("zDiariasCard2.csv", sep=";", decimal=",")
            quantidade_diarias = tabela_filtrada_final['Diarias'].sum()

        
        card_content1 = [
            dbc.CardHeader("Diárias", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            dbc.CardBody([
                html.H4(f'{quantidade_diarias}', className="card-title", style={"font-size": "0.6rem", "font-weight": "bold", "text-align": "center"}),
            ]),
        ]

        return card_content1
    
@app.callback(
    Output('select_funcionarios', 'options'),
    [
        Input('dropdown_data', 'date'),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)

def update_output(value_data):

    partes_da_data = value_data.split("-")
    mes = partes_da_data[1]
    dia = partes_da_data[2]
    nome_arquivo = f'//192.168.0.164/Access Run/arquivos-lidos/{mes}/{dia}.csv'
    df_atualizado = pd.read_csv(nome_arquivo, sep=";", decimal=",")        
    todos_funcionarios = list(df_atualizado['Parceiro'])
    updated_options = [{'label': i, 'value': i} for i in todos_funcionarios]

    return updated_options

@app.callback(
    Output('button-ver-todos', 'children'),
    [
        Input('button-ver-todos', 'n_clicks'),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)

def update_output(n_clicks):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['button-ver-todos']:

        if n_clicks % 2 != 0:
            texto = "Dia"
            return texto
        else:
            texto = "Todo o Mês"
            return texto     

@app.callback(
    Output('button-ver-todas-diarias', 'children'),
    [
        Input('button-ver-todas-diarias', 'n_clicks'),
    ],
    prevent_initial_call=True,
    allow_duplicate=True
)

def update_output(n_clicks):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Se o callback não foi acionado por TODOS input
        raise dash.exceptions.PreventUpdate

    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input in ['button-ver-todas-diarias']:

        if n_clicks % 2 != 0:
            texto = "Ver individualmente"
            return texto
        else:
            texto = "Diárias de Todos Funcinários"
            return texto 
if __name__ == '__main__':
    app.run_server(host='192.168.100.115', port=8050,debug=True)
