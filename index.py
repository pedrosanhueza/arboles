import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file:

    fileName = uploaded_file.name
    
    st.write(fileName)
    
    if fileName.endswith("csv"):
        
        df = pd.read_csv(uploaded_file)

    elif fileName.endswith("xlsx"):

        df = pd.read_excel(uploaded_file)

    st.write("### Uploaded CSV File:")
    
    st.write(df)