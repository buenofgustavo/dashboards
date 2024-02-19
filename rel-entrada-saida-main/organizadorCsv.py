import pandas as pd
import os
def organizadorCsv(nome_arquivo):


    def calcular_diarias(diferenca_horas):
        if diferenca_horas >= 8:
            return 1
        elif diferenca_horas >= 4:
            return 0.5
        else:
            return 0

    df = pd.read_csv(nome_arquivo, sep=";", names=['Parceiro', 'Tipo', 'Data_Hora'])

    # Convertendo a coluna 'Data_Hora' para datetime com formato especificado
    df['Data_Hora'] = pd.to_datetime(df['Data_Hora'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    # Agrupar por 'Parceiro' e criar uma nova coluna com todas as datas e horas formatadas
    df_agrupado = df.groupby('Parceiro')['Data_Hora'].agg(lambda x: ' | '.join(x.sort_values().dt.strftime('%d-%m-%Y %H:%M:%S').astype(str))).reset_index()

    df_agrupado['Diferenca_Horas'] = df.groupby('Parceiro')['Data_Hora'].agg(lambda x: (x.max() - x.min()).total_seconds() / 3600 - 1 if len(x) > 1 else 0).reset_index()['Data_Hora']

    # Adicionar a nova coluna 'Diarias' com base na diferença de horas
    df_agrupado['Diarias'] = df_agrupado['Diferenca_Horas'].apply(calcular_diarias)
    df_agrupado.to_csv(nome_arquivo, sep=';', decimal=',', index=False)
    

    df_agrupado['Diferenca_Horas'] = df_agrupado['Diferenca_Horas'].apply(lambda x: '{:02}:{:02}'.format(int(x),int((x % 1) * 60)))

    os.remove(nome_arquivo)

    # Salvar o DataFrame agrupado em um novo arquivo, se necessário
