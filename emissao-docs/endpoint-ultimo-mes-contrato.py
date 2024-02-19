from flask import Flask, jsonify
import pandas as pd
import pyodbc

app = Flask(__name__)

def execute_sql_query():
    conn = pyodbc.connect('')
    sql_query = """



SELECT 
    CODIGO,
	USUINC,
	CONVERT(VARCHAR(10), DATINC, 103) AS DATINC
FROM
    rodcfr
WHERE
    USUINC IN (
        'ana.escorcio',
        'girlaneide.silva',
        'lauana.nascimento',
        'lorrany.lima',
        'laryssa.violatti',
        'juliana.castilho',
        'micaele.lessa',
        'leia.assuncao',
        'aline.felismino',
        'amanda.jesus',
        'gabriela.freire',
        'roberio.filho',
        'maria.sampaio',
        'mariolina.caiado',
        'anabely.diniz',
        'alici.cruz',
        'yasmin.dorea',
        'dayana.dores',
        'jascielle.paula',
        'caio.korpan',
        'fernanda.odi',
        'julio.mendes',
        'luciene.oliveira',
        'janete.gondim',
        'yohanny.moraes',
        'brayan.garcia',
        'rayssa.ramos'
    )
AND DATINC >= DATEADD(MONTH, -1, GETDATE())
AND situac NOT IN ('C', 'I');

    """
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df.to_dict(orient='records')

@app.route('/ultimo-mes-contratos', methods=['GET'])

def get_resultado_sql():
    resultado = execute_sql_query()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host="192.168.100.115", port=7022, debug=True)
