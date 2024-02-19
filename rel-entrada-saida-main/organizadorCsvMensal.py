import pandas as pd
def organizadorCsvMensal(nome_arquivo, caminho_completo_destino_mensal):

    df = pd.read_csv(nome_arquivo, sep=";", decimal=",")

    #df = df.iloc[1:]

    df.to_csv(caminho_completo_destino_mensal, sep=";", decimal=",", index=False, mode='a', header=False)
