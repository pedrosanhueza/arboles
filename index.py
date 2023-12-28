import streamlit as st
import pandas as pd

st.title("I-tree Candelaria")

uploaded_file = st.file_uploader("",type=['csv', 'xlsx'])

if uploaded_file:

    fileName = uploaded_file.name    
    
    if fileName.endswith("xlsx"):

        df = pd.read_excel(uploaded_file)

    elif fileName.endswith("csv"):
    
        df = pd.read_csv(uploaded_file)

    else:

        st.warning('Error in file upload', icon="⚠️")
    
    st.table(df)

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)
    
    st.write('Índice de área foliar: ', lai)

    tc = st.number_input('Porcentaje de superficie cubierta', value=5)
    
    st.write('Porcentaje de superficie cubierta: ', tc, "%")

col1, col2 = st.columns(2)
col1.metric("LAI", f"{lai} m2/m2")
col2.metric("Superficie Cubierta" , tc)