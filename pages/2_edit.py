import streamlit as st
import pandas as pd
from transactions import Transactions

class Edit():
    def __init__(self) -> None:
        self.page()
        pass

    def page(self):
        
        ts = Transactions()

        ts.editableTable(10);
        # edited = st.data_editor(all_transactions, key="data_editor")
        # st.json(st.session_state["data_editor"]["edited_rows"]);
        return

Edit()