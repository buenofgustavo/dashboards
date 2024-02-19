import pandas as pd

def soma_diarias_por_parceiro(caminho_arquivo):
    # Carrega o arquivo CSV para um DataFrame
    df = pd.read_csv(caminho_arquivo, sep=";", decimal=",")

    # Agrupa por Parceiro e soma as Diarias
    resultado = df.groupby('Parceiro')['Diarias'].sum().reset_index()
    resultado.to_csv("diariasDoMes.csv", sep=";", decimal=",", index=False)
