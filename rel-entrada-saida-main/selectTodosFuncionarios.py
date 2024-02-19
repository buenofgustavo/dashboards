import pandas as pd
def selectTodosFuncionarios(nome_arquivo):

    df = pd.read_csv(nome_arquivo, sep=";", decimal=",")

    todos_fucionarios = list(df['Parceiro'])
    
    return todos_fucionarios

