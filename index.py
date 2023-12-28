import streamlit as st
import pandas as pd

st.title("I-tree Candelaria")

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)

    tc = st.number_input('Porcentaje de superficie cubierta', value=5)

col1, col2 = st.columns(2)
col1.metric("Leaf area index", lai)
col2.metric("Superficie Cubierta" , f"{tc}%")

uploaded_file = st.file_uploader("",type=['csv', 'xlsx'])

# if uploaded_file:

fileName = uploaded_file.name    

if fileName.endswith("xlsx"):

    df = pd.read_excel(uploaded_file)

elif fileName.endswith("csv"):

    df = pd.read_csv(uploaded_file)

else:

    st.warning('Error in file upload', icon="⚠️")

if uploaded_file:

    st.table(df)