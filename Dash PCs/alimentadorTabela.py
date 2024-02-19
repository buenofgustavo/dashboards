import csv
import pyodbc
import pandas as pd
import io
import time

def executar_consulta_salvar_csv():
    # Conectar ao banco de dados
    conn = pyodbc.connect('')

    cursor = conn.cursor()

    sql_query = "SELECT * FROM TDM_RODPRC_RODLPR"
    cursor.execute(sql_query)

    # Fetch all rows from the query result
    resultados = cursor.fetchall()

    # Especifique o caminho e o nome do arquivo CSV onde você deseja salvar os resultados
    nome_arquivo_csv = 'tabela_view.csv'

    # Use io.StringIO para criar um buffer de texto que armazenará os dados no formato CSV
    csv_buffer = io.StringIO()

    # Escreve os resultados no buffer CSV, especificando o delimitador como ponto e vírgula e a codificação como utf-8
    escritor_csv = csv.writer(csv_buffer, delimiter=';', lineterminator='\r\n')

    # Escreve o cabeçalho com os nomes das colunas
    escritor_csv.writerow([column[0] for column in cursor.description])

    # Escreve os dados das linhas
    for linha in resultados:
        escritor_csv.writerow(linha)

    # Abre o arquivo CSV para escrita, especificando o modo binário e a codificação como utf-8
    with open(nome_arquivo_csv, 'wb') as arquivo_csv:
        # Obtém o conteúdo do buffer e o escreve no arquivo CSV
        arquivo_csv.write(csv_buffer.getvalue().encode('utf-8'))

    print(f"Os resultados da consulta foram salvos no arquivo '{nome_arquivo_csv}'")

    # Fechar a conexão com o banco de dados
    conn.close()

# Executar a função a cada 15 segundos
while True:
    executar_consulta_salvar_csv()
    time.sleep(900)


