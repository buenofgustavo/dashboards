from datetime import datetime

data1 = "19-01-2024 17:56:57"
data2 = "19-01-2024 07:52:12"

# Convertendo as strings para objetos datetime
data1_obj = datetime.strptime(data1, "%d-%m-%Y %H:%M:%S")
data2_obj = datetime.strptime(data2, "%d-%m-%Y %H:%M:%S")

# Calculando a diferença entre as duas datas
diferenca = data1_obj - data2_obj

print(diferenca)