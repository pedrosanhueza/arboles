import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:
    # Load the Excel workbook using load_workbook
    wb = load_workbook(uploaded_file)

    # Choose the sheet you want to read
    sheet_name = "Sheet1"

    # Read the selected sheet into a DataFrame
    df = pd.read_excel(wb, sheet_name=sheet_name)

    # Now you can work with the DataFrame 'df'
