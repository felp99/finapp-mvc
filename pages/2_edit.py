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
        return

Edit()