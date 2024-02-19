from flask import Flask, jsonify
import pandas as pd
import pyodbc

app = Flask(__name__)

def execute_sql_query():
    conn = pyodbc.connect('')
    sql_query = """



SELECT TOP 5
    cgr.descri as PAGADOR, 
    cgr.codcgr as CODPAG,
    SUM(con.TOTFRE) AS total_TOTFRE
FROM rodcon con
LEFT JOIN rodcli cli ON con.CODPAG = cli.CODCLIFOR
LEFT JOIN rodcgr cgr ON cli.CODCGR = cgr.CODCGR
WHERE
    con.situac NOT IN ('c', 'i')
    AND con.CTEAUT = 's'
    AND con.datinc >= DATEADD(MONTH, -1, GETDATE())
GROUP BY 
    cgr.CODCGR,
    cgr.descri
ORDER BY
     sum(con.TOTFRE) DESC;


    """
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df.to_dict(orient='records')

@app.route('/faturamento-ultimo-mes', methods=['GET'])

def get_resultado_sql():
    resultado = execute_sql_query()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host="192.168.100.115", port=7031, debug=True)
