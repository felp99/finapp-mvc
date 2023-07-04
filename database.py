import streamlit as st
import pandas as pd
import pyodbc
import datetime

class Database:

    def __init__(self):
        self.conn = self.init_connection()
        self.all_transactions = self.getAllTransactions();
        self.all_categories = self.getAllCategories();
        pass

    def init_connection(self):
        return pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"]
        )
    
    def run_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            return [dict(zip([column[0] for column in cur.description], row))
                    for row in cur.fetchall()]
    
    def insert_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            cur.commit()
        self.conn.close()

    def getAllCategories(self):
        return self.run_query("select * from T_CATEGORIES");

    def getAllTransactions(self):
        return self.run_query("select * from T_TRANSACTIONS");

    def getCategoriesFilteredByType(self, type, categories):
        CD_CATEGORY_TYPE_STR = {0: "ENTRADA", 1: "SAÍDA"};
        categoriesUsed = categories if categories is not None else self.getAllCategories();
        return filter(lambda x: x["CD_CATEGORY_TYPE"] == [k for k, v in CD_CATEGORY_TYPE_STR.items() if v == type][0], categoriesUsed)    
