import streamlit as st
import pandas as pd

st.title("I-tree Candelaria")

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)

    tc = st.number_input('Porcentaje de superficie cubierta', value=5)

col1, col2 = st.columns(2)
col1.metric("Leaf area index", lai)
col2.metric("Superficie Cubierta" , f"{tc}%")

uploaded_file = st.file_uploader("Subir archivo",type=['csv', 'xlsx'], label_visibility="hidden")

if uploaded_file:

    fileName = uploaded_file.name    

    if fileName.endswith("xlsx"):

        df = pd.read_excel(uploaded_file)

    elif fileName.endswith("csv"):

        df = pd.read_csv(uploaded_file)

    else:

        st.warning('Error in file upload', icon="⚠️")

if uploaded_file:

    with st.expander("See explanation"):
    
        st.write("Step 1: Get raw data")
        st.dataframe(df)

        st.write("Step 2: Round 'Velocidad viento' column")
        df['Velocidad del viento (m/s)'] = df['Velocidad del viento (m/s)'].apply(lambda x: float(x.replace(",","."))).round()
        st.dataframe(df)

        st.write("Step 3: Build reference table")
        table1 = {
            'Velocidad del viento (m/s)': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'Promedio': [0, 0.03, 0.09, 0.15, 0.17, 0.19, 0.2, 0.56, 0.92, 0.92, 2.11, 2.11, 2.11, 2.11],
            'Mínimo': [0, 0.006, 0.012, 0.018, 0.022, 0.025, 0.029, 0.056, 0.082, 0.082, 0.57, 0.57, 0.57, 0.57],
            'Máximo': [0, 0.042, 0.163, 0.285, 0.349, 0.414, 0.478, 1.506, 2.534, 2.534, 2.534, 2.534, 2.534, 2.534],
            '% Resuspensión': [0, 1.5, 3, 4.5, 6, 7.5, 9, 10, 11, 12, 13, 16, 20, 23]
        }
        reference_table = pd.DataFrame(table1)
        st.dataframe(reference_table)

        st.write("Step 4: Merged tables")
        df = pd.merge(df, reference_table, on='Velocidad del viento (m/s)', how='left')
        st.dataframe(df)

        st.write("Step 5: Add LAI column")
        df['LAI (m2/m2)'] = lai
        st.dataframe(df)

        st.write('Step 6: add columns "Vd,min (cm/s)" and "Vd,max (cm/s)" and "Vd (cm/s)"')
        df['Vd,min (cm/s)'] = df['LAI (m2/m2)'] * df['Mínimo']
        df['Vd,max (cm/s)'] = df['LAI (m2/m2)'] * df['Máximo']
        df['Vd (cm/s)'] = df['LAI (m2/m2)'] * df['Promedio']
        st.dataframe(df)

        st.write("Step 7: Change unit measure")
        st.write(df.columns)
        df['MP2,5 (g/m³)'] = df['MP2,5 (µg/m³)'] / 1000 / 1000
        df["Vd,min (m/s)"] = df['Vd,min (cm/s)'] / 100

        st.dataframe(df.style.format(precision=7))
