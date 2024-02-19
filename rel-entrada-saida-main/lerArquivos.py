import pandas as pd

def lerArquivos(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=";", decimal=",")
    return df