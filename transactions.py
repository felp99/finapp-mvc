import json
from database import Database
import pandas as pd
import streamlit as st
import pandas as pd
import pyodbc
import datetime

class Transactions():
    def __init__(self) -> None:
        self.db = Database();
        self.all_transactions = self.db.all_transactions;
        self.all_categories = self.db.all_categories;
        self.allTransactionsDataframe();
        self.balance = self.income-self.expense;

        self.defaultObject = {
            "DT_PAYMENT":None,
            "TX_TRANSACTION_DESCRIPTION":None,
            "NU_TRANSACTION_VALUE":None,
            "TX_CATEGORY_NAME":None,
            "CD_CATEGORY_TYPE":None,
        }
        pass

    def allTransactionsDataframe(self):

        CD_CATEGORY_TYPE = {0: "ENTRADA", 1: "SAÍDA"}

        all_transactions_df = pd.DataFrame(self.all_transactions)
        all_transactions_df["DT_PAYMENT"] = pd.to_datetime(all_transactions_df["DT_PAYMENT"])
        all_transactions_df["NU_TRANSACTION_VALUE"] = pd.to_numeric(all_transactions_df["NU_TRANSACTION_VALUE"])
        all_transactions_df.drop(columns=["ID_CREDIT_INVOICE_INFO"], inplace=True)

        all_categories_df =  pd.DataFrame(self.all_categories)
        all_categories_df.drop(columns=["TX_CATEGORY_DESCRIPTION"], inplace=True)

        all_transactions_df = pd.merge(all_transactions_df, all_categories_df, on="ID_CATEGORY")

        self.income = all_transactions_df[all_transactions_df["CD_CATEGORY_TYPE"] == 0]["NU_TRANSACTION_VALUE"].sum()
        self.expense = all_transactions_df[all_transactions_df["CD_CATEGORY_TYPE"] == 1]["NU_TRANSACTION_VALUE"].sum()

        all_transactions_df["TIPO"] = all_transactions_df["CD_CATEGORY_TYPE"].map(CD_CATEGORY_TYPE)
        all_transactions_df.drop(columns=["ID_CATEGORY", "ID_USER"], inplace=True)

        self.all_transactions_df = all_transactions_df;

    def transactionsTable(self, n):
        return st.table(self.all_transactions_df.iloc[-n:]
                .sort_values(by=['DT_PAYMENT', 'DT_CREATED'])
                .drop(columns=["DT_CREATED"]))

    def editableTable(self, n):
        dataframe = self.all_transactions_df.sort_values(by=['DT_PAYMENT', 'DT_CREATED']).iloc[-n:].reset_index(drop=True)
        st.data_editor(dataframe,
                        hide_index=True,
                        key="data_editor",
                        column_config={
                            "TX_CATEGORY_NAME": st.column_config.SelectboxColumn(
                                width="medium",
                                required=True,
                                options=map(lambda x: x["TX_CATEGORY_NAME"], self.all_categories),
                            ),
                            "DT_PAYMENT": st.column_config.DatetimeColumn(
                                "DATA PAGAMENTO",
                                format="DD/MM/YYYY",
                                width="small", 
                            ),
                            "DT_CREATED": None,
                            "NU_TRANSACTION_VALUE": st.column_config.NumberColumn(
                                "VALOR",
                                format="R$ %.2f",
                            ), 
                            "TX_DESCRIPTION": st.column_config.TextColumn(
                                        "DESCRIÇÃO",
                                    ),
                            "ID_TRANSACTION": None,
                            "CD_CATEGORY_TYPE": None,
                        },)

        edited_rows = st.session_state["data_editor"]["edited_rows"]
        
        if len(edited_rows) > 0:
            index_position = list(edited_rows.keys())[0];
            object = json.loads(dataframe.iloc[index_position].to_json());

            for k in self.defaultObject:
                try:
                    object[k] = edited_rows[list(edited_rows.keys())[0]][k]
                except:
                    pass

            st.json(edited_rows)
            st.json(object)
            # self.db.insert_query(
            #     f'''
            #     UPDATE T_TRANSACTIONS
            #     SET 
            #         TX_TRANSACTION_DESCRIPTION = '{object["TX_TRANSACTION_DESCRIPTION"]}' 
            #     WHERE ID_TRANSACTION = {object["ID_TRANSACTION"]}
            #     '''
            # )
            # edited_rows.clear()
            # st.experimental_rerun()


        

    def balanceMetric(self):
        return st.metric('Saldo', self.formatMoney(self.balance), delta=12, delta_color="normal", help=None, label_visibility="visible");

    def formatMoney(self, float):
        return f'R${round(float, 2)}';