import pandas as pd
import pyodbc
import io
import csv

# Conexão com o banco de dados
conn = pyodbc.connect('')

cursor = conn.cursor()
query = """SELECT TOP 5
    cgr.descri as PAGADOR, 
    cgr.codcgr as CODPAG,
    COUNT(con.codcon) AS total_codcon
FROM rodcon con
LEFT JOIN rodcli cli ON con.CODPAG = cli.CODCLIFOR
LEFT JOIN rodcgr cgr ON cli.CODCGR = cgr.CODCGR
WHERE
    con.situac NOT IN ('c', 'i')
    AND con.CTEAUT = 's'
    AND con.datinc >= DATEADD(day, -7, GETDATE())
GROUP BY 
    cgr.CODCGR,
    cgr.descri
ORDER BY
    COUNT(con.codcon) DESC;"""

cursor.execute(query)

resultados = cursor.fetchall()
df = pd.read_sql_query(query, conn)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('sqltop5clientessemanal.csv', index=False)

conn.close()
