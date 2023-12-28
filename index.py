import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:
    
    st.write(uploaded_file.name)

    df = pd.read_excel(uploaded_file)

    st.table(df)