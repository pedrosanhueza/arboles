import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:

    fileName = uploaded_file.name    
    
    if fileName.endswith("xlsx"):

        st.write("xlsx")

    elif fileName.endswith("csv"):

        st.write("csv")
    
    df = pd.read_excel(uploaded_file)

    st.table(df)