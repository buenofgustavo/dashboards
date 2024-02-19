import streamlit as st
import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=54.207.225.212\ROD_TDM,1520;'
                      'Database=db_visual_tdm_teste;'
                      'UID=userLucas;'
                      'PWD=hp1y9qlf4')

cursor = conn.cursor()
tabela = pd.read_sql('SELECT * FROM TDM_RODPRC_RODLPR', conn)

st.write(tabela)

conn.close()