from database import Database
import pandas as pd
import streamlit as st
import pandas as pd
import pyodbc
import datetime

class Transactions():
    def __init__(self) -> None:
        db = Database();
        self.all_transactions = db.all_transactions;
        self.all_categories = db.all_categories;
        self.allTransactionsDataframe();
        self.balance = self.income-self.expense;
        pass

    def allTransactionsDataframe(self):

        CD_CATEGORY_TYPE = {0: "🟢", 1: "🔻"}

        all_transactions_df = pd.DataFrame(self.all_transactions)
        all_transactions_df["DT_PAYMENT"] = pd.to_datetime(all_transactions_df["DT_PAYMENT"])
        all_transactions_df["NU_VALUE"] = pd.to_numeric(all_transactions_df["NU_VALUE"])
        all_transactions_df.drop(columns=["ID_CREDIT_INVOICE_INFO"], inplace=True)

        all_categories_df =  pd.DataFrame(self.all_categories)
        all_categories_df.drop(columns=["TX_DESCRIPTION"], inplace=True)

        all_transactions_df = pd.merge(all_transactions_df, all_categories_df, on="ID_CATEGORY")

        self.income = all_transactions_df[all_transactions_df["CD_CATEGORY_TYPE"] == 0]["NU_VALUE"].sum()
        self.expense = all_transactions_df[all_transactions_df["CD_CATEGORY_TYPE"] == 1]["NU_VALUE"].sum()

        # all_transactions_df.set_index("DT_PAYMENT", inplace=True)
        # all_transactions_df.sort_index(inplace=True)

        all_transactions_df["TIPO"] = all_transactions_df["CD_CATEGORY_TYPE"].map(CD_CATEGORY_TYPE)
        #all_transactions_df['NU_VALUE'] = all_transactions_df['NU_VALUE'].map('R${:,.2f}'.format)

        all_transactions_df.drop(columns=["CD_CATEGORY_TYPE", "ID_CATEGORY", "ID_USER"], inplace=True)

        all_transactions_df.rename(columns={"TX_DESCRIPTION":"DESCRIÇÃO",
                                #"NU_VALUE": "VALOR",
                                "TX_NAME": "CATEGORIA"}, inplace=True)
        #all_transactions_df.index.name='DT_PAYMENT'

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
                            "CATEGORIA": st.column_config.SelectboxColumn(
                                help="The category of the app",
                                width="medium",
                                required=True,
                                options=map(lambda x: x["TX_NAME"], self.all_categories),
                            ),
                            "DT_PAYMENT": st.column_config.DatetimeColumn(
                                "DATA PAGAMENTO",
                                format="DD/MM/YYYY",
                            ),
                            "DT_CREATED": st.column_config.DatetimeColumn(
                                "DATA CRIAÇÃO",
                                format="DD/MM/YYYY",
                                disabled=True,
                            ),
                            "NU_VALUE": st.column_config.NumberColumn(
                                "VALOR",
                                format="R$ %.2f",
                            )
                        },)

        st.write(st.session_state["data_editor"]["edited_rows"])
        # for i in st.session_state["data_editor"]["edited_rows"]:
        #     json = dict(dataframe.iloc[i].to_json()
        #     id = json["ID_TRANSACTION"]

    def balanceMetric(self):
        return st.metric('Saldo', self.formatMoney(self.balance), delta=12, delta_color="normal", help=None, label_visibility="visible");

    def formatMoney(self, float):
        return f'R${round(float, 2)}';