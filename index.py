import streamlit as st
import pandas as pd
from decimal import Decimal

# ---------------------- #
# ------ SIDE BAR ------ #
# ---------------------- #

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)
    tc = st.number_input('Porcentaje de superficie cubierta', value=0.05)

# ------------------------- #
# ------ FILE UPLOAD ------ #
# ------------------------- #

st.title("I-tree Candelaria")

col1, col2 = st.columns(2)
col1.metric("Leaf area index", lai)
col2.metric("Superficie Cubierta" , f"{tc}%")

uploaded_file = st.file_uploader("Subir archivo",type=['csv', 'xlsx'], label_visibility="hidden")

if uploaded_file:

    fileName = uploaded_file.name    

    if fileName.endswith("xlsx"):

        df = pd.read_excel(uploaded_file)

    elif fileName.endswith("csv"):

        df = pd.read_csv(uploaded_file, dtype=str)

    else:

        st.warning('Error in file upload', icon="⚠️")

# ------------------------- #
# ------ CALCULATIONS ----- #
# ------------------------- #
        
if uploaded_file:
    
    # drop 'fecha' column
    df.columns = map(str.lower, df.columns)
    if 'fecha' in df.columns:
        df = df.drop('fecha', axis=1)

    # change column name 'velocidad'
    substrings_to_replace_velocidad = ["vv", "viento", "velocidad", "velocidad del viento"]
    for column in df.columns:
        if any(substring in column.lower() for substring in substrings_to_replace_velocidad):
            new_column_name = "Velocidad del viento (m/s)"
            df.rename(columns={column: new_column_name}, inplace=True)

    # change column name 'mp2,5'
    substrings_to_replace_mp = ["mp", "2,5", "25"]
    for column in df.columns:
        if any(substring in column.lower() for substring in substrings_to_replace_mp):
            new_column_name = "MP2,5 (µg/m³)"
            df.rename(columns={column: new_column_name}, inplace=True)

    # change column name 'altura'
    substrings_to_replace_mp = ["mh", "altura", "mezcla"]
    for column in df.columns:
        if any(substring in column.lower() for substring in substrings_to_replace_mp):
            new_column_name = "Altura de Mezcla (m)"
            df.rename(columns={column: new_column_name}, inplace=True)

    # replace comma with dots
    df = df.applymap(lambda x: str(x).replace(',', '.'))

    st.dataframe(df)