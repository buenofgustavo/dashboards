import os
import csv

from organizadorCsv import organizadorCsv
from organizadorCsvMensal import organizadorCsvMensal

def processarArquivo():
    pasta_origem = '//192.168.0.164/Access Run/arquivos'

    # ALTERAR AQUI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pasta_destino = '//192.168.0.164/Access Run/arquivos-lidos/03'
    arquivos = os.listdir(pasta_origem)

    if arquivos:
        arquivo = arquivos[0]
        caminho_completo_origem = os.path.join(pasta_origem, arquivo)

        print(caminho_completo_origem)

        if os.path.isfile(caminho_completo_origem):
            with open(caminho_completo_origem, 'r') as file_origem:
                # Lê o conteúdo do arquivo como um arquivo CSV
                leitor_csv = csv.reader(file_origem, delimiter=';')
                
                # Pula as três primeiras linhas
                for _ in range(3):
                    next(leitor_csv)
                
                # Lê o restante das linhas, excluindo as colunas especificadas
                linhas = []
                for row in leitor_csv:
                    # Exclua as colunas de índice 2, 3, 4, 5, 6, 9 e 10
                    nova_linha = ";".join(row[i] for i in range(len(row)) if i not in [ 2,3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15])
                    linhas.append(nova_linha)

                # Cria o caminho completo para o arquivo na pasta de destino
                caminho_completo_destino = os.path.join(pasta_destino, arquivo)

                # Escreve o conteúdo no arquivo da pasta de destino
                with open(caminho_completo_destino, 'w', newline='') as file_destino:
                    file_destino.write("\n".join(linhas))

                # Chama a função do outro arquivo
                print(caminho_completo_destino)
                organizadorCsv(caminho_completo_destino)

                # ALTERAR AQUI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                arquivo_mensal = '03mes.csv'
                
                caminho_completo_destino_mensal = os.path.join(pasta_destino, arquivo_mensal)
                print(caminho_completo_destino_mensal)
                organizadorCsvMensal(caminho_completo_destino, caminho_completo_destino_mensal)


                print(f'O arquivo {arquivo} foi copiado para a pasta de destino.')

                # Exclui o arquivo original
            os.remove(caminho_completo_origem)
            print("Arquivo excluído")
        else:
            print('Não há arquivos na pasta de origem.')


