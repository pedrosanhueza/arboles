from openpyxl import load_workbook
import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    # Now you can work with the DataFrame 'df'
