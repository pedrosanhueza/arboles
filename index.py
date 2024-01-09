import streamlit as st
import pandas as pd
from decimal import Decimal

# ------ START SIDE BAR ------

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)

    tc = st.number_input('Porcentaje de superficie cubierta', value=5)

col1, col2 = st.columns(2)
col1.metric("Leaf area index", lai)
col2.metric("Superficie Cubierta" , f"{tc}%")

# ------ END SIDE BAR ------

st.title("I-tree Candelaria")

uploaded_file = st.file_uploader("Subir archivo",type=['csv', 'xlsx'], label_visibility="hidden")

if uploaded_file:

    fileName = uploaded_file.name    

    if fileName.endswith("xlsx"):

        df = pd.read_excel(uploaded_file)

    elif fileName.endswith("csv"):

        df = pd.read_csv(uploaded_file, dtype=str)

    else:

        st.warning('Error in file upload', icon="⚠️")

st.dataframe(df)