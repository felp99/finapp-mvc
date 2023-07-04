import streamlit as st
import pandas as pd
import pyodbc
import datetime
from database import Database
from transactions import Transactions

st.set_page_config(
    page_title="Transactions",
    page_icon="🪀",    
    layout="wide",
    initial_sidebar_state="expanded",
)

CD_CATEGORY_TYPE = {0: "🟢",
                    1: "🔻"}
CD_CATEGORY_TYPE_STR = {0: "ENTRADA",
                    1: "SAÍDA"}

TODAY = datetime.datetime.now()

db = Database()



all_categories = db.run_query("select * from T_CATEGORIES")
all_transactions = db.run_query("select * from T_TRANSACTIONS")

with st.sidebar:        
    transaction_date = st.date_input("Data")
    transaction_description = st.text_input("Descrição")
    transaction_type = st.selectbox("Tipo", 
                ["ENTRADA", "SAÍDA"], 
                index=0, 
                key=None)
    categories = filter(lambda x: x["CD_CATEGORY_TYPE"] == [k for k, v in CD_CATEGORY_TYPE_STR.items() if v == transaction_type][0], all_categories)    
    transaction_category = st.selectbox("Categoria", 
                map(lambda x: x["TX_NAME"], categories), 
                index=0, 
                key=None)
    transaction_value = st.number_input("Value")
    transaction_add = st.button("ADICIONAR")

    if transaction_add:
        if transaction_description == '':
            st.warning('Descrição não pode ser nula')
            st.stop()

ts = Transactions()
ts.transactionsTable(10)
ts.balanceMetric()
    
if transaction_add:
    db.insert_query(f'''
                INSERT INTO T_TRANSACTIONS 
                (DT_PAYMENT, TX_DESCRIPTION, NU_VALUE, ID_CATEGORY, DT_CREATED) 
                VALUES 
                 ('{transaction_date}', 
                 '{transaction_description}', 
                  {transaction_value}, 
                 (select ID_CATEGORY from T_CATEGORIES where TX_NAME = '{transaction_category}' 
                  AND CD_CATEGORY_TYPE = {[k for k, v in CD_CATEGORY_TYPE_STR.items() if v == transaction_type][0]}),
                  '{TODAY}')
                ''')
    st.experimental_rerun()