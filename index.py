import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel File Reader")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a binary IO:
    bytesio = BytesIO(uploaded_file.getvalue())
    st.write(bytesio)

    # Handle both text and binary files using Pandas functions
    try:
        # Try reading as CSV
        dataframe = pd.read_csv(bytesio)
        st.dataframe(dataframe)  # Display DataFrame
    except pd.errors.ParserError:
        try:
            # Try reading as Excel
            dataframe = pd.read_excel(bytesio, engine='openpyxl')
            st.dataframe(dataframe)  # Display DataFrame
        except pd.errors.ParserError:
            st.warning("Unsupported file format. Please upload a CSV or Excel file.")
