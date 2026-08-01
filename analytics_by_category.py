import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def analytics_by_category_tab():
    date_col1,date_col2=st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with date_col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("GetAnalytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }
        response = requests.post(f"{API_URL}/analytics_by_category",json=payload)
        if response.status_code == 200:
            response = response.json()
            # st.write(existing_expenses)
        else:
            st.error("Failed to retrieve expenses")
            response = []
        #st.write(response)

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]['total'] for category in response],
            "Percentage": [response[category]['percentage'] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        st.subheader("Expense Breakdown by Category")
        st.bar_chart(data=df_sorted.set_index("Category")["Percentage"],width =100,height=350,use_container_width=True)

        # to set the decimal limit
        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        st.table(df_sorted)
