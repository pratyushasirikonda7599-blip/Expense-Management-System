import streamlit as st
from add_update_UI import add_update_tab
from analytics_by_category import analytics_by_category_tab
from analytics_by_month import analytics_by_month_tab


st.title("Expense Management System")

tab1, tab2, tab3 = st.tabs(["Add/Update","Analytics by Category", "Analytics by Months"])

with tab1:
    add_update_tab()
with tab2:
    analytics_by_category_tab()
with tab3:
    analytics_by_month_tab()
