from flask import Flask, jsonify
import pandas as pd
import pyodbc

app = Flask(__name__)

def execute_sql_query():
    conn = pyodbc.connect('')
    sql_query = """



SELECT 
    COALESCE(cfr.data_inclusao, con.data_inclusao) AS data_inclusao,
    COALESCE(cfr.quantidade_documentos, 0) AS quantidade_documentos_rodcfr,
    COALESCE(con.quantidade_documentos, 0) AS quantidade_documentos_rodcon
FROM
    (SELECT 
        CAST(datinc AS DATE) AS data_inclusao,
        COUNT(*) AS quantidade_documentos
FROM 
    rodcfr
WHERE 
	situac NOT IN ('c', 'i') 
	AND DATINC >= DATEADD(MONTH, -1, GETDATE())
	AND USUINC IN (
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
    GROUP BY CAST(datinc AS DATE)) AS cfr

FULL JOIN

(SELECT 
        CAST(datinc AS DATE) AS data_inclusao,
        COUNT(*) AS quantidade_documentos
FROM 
        rodcon
WHERE 
        situac NOT IN ('c', 'i')
		AND CTEAUT = 'S'
		AND DATINC >= DATEADD(MONTH, -1, GETDATE())
		AND USUINC IN (
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
GROUP BY CAST(datinc AS DATE)) AS con

ON cfr.data_inclusao = con.data_inclusao
ORDER BY data_inclusao;





    """
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df.to_dict(orient='records')

@app.route('/emissao-mensal', methods=['GET'])

def get_resultado_sql():
    resultado = execute_sql_query()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host="192.168.100.115", port=7021, debug=True)
