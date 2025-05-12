import streamlit as st
import pandas as pd 
from utils.data_handler import load_data, add_expense
from ml.predictor import predictor

st.set_page_config(page_title="Smart Expense Tracker", layout="centered")
st.markdown("<h1 style='color: #000080;'>Smart Monthly Expense Tracker</h1>",unsafe_allow_html=True)
st.markdown("Track your spending habits and predict future expenses using Machine Learning.")

with st.container(border=True):
    st.header("**Add Expense:**")
    st.subheader("*Log your expenses here..*")

    col1, col2 = st.columns(2)
    with col1: 
        date = st.date_input("Add date of expense")
        expense = st.number_input("Add expense")
    with col2: 
        category = st.multiselect("Add category of expense",["Travel","Food","Fun","Necessary","Miscellaneous"])
        description = st.text_input("Add description")

    if st.button("Add expense"):
        if expense > 0 and category:
            add_expense(date, expense, category, description)
            st.success("Expense added!")
        else:
            st.warning("Please enter amount and category!")

with st.container(border=True):
    st.header("**Monthly tracker:**")
    st.subheader("*Here is a summary of your past expenses by month.*")

    df = load_data()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']) 

    st.dataframe(df.style.format({"expense": "₹{:.2f}"}), use_container_width=True)

    df['month'] = df['date'].dt.to_period('M').astype(str)
    month_totals = df.groupby('month')['expense'].sum()
    st.line_chart(month_totals)

with st.container(border=True):
    st.header("**Expense predictions for next 3 months**")
    preds = predictor(periods=3, df=df)
    st.dataframe(preds.style.format({"Predicted Expense": "₹{:.2f}"}), use_container_width=True)
    st.line_chart(preds.set_index('Month'))