import pandas as pd

df = pd.read_csv("tabela_view.csv", sep=";", decimal=",")


PCs_totais_card5 = df.shape[0]

print(PCs_totais_card5)
