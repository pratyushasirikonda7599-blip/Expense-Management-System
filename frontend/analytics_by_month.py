import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_by_month_tab():
    response = requests.get(f"{API_URL}/analytics_by_month")
    if response.status_code == 200:
        expenses_month = response.json()
        #st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        expenses_month = []



    df = pd.DataFrame(expenses_month)
    st.title("Expenses Breakdown per month")
    st.bar_chart(data=df.set_index('expense_month')['total'],width=100,height=350,use_container_width=True)

    df["total"] = df["total"].map("{:.2f}".format)
    st.table(df.sort_index())