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

        st.write("Step 2: Normalized data")
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
        st.dataframe(df)

        st.write("Step 3: Round 'Velocidad viento' column")
        df['Velocidad del viento (m/s)'] = df['Velocidad del viento (m/s)'].apply(lambda x: float(str(x).replace(",","."))).round()
        st.dataframe(df)

        st.write("Step 4: Build reference table")
        table1 = {
            'Velocidad del viento (m/s)': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            'Promedio': [0, 0.03, 0.09, 0.15, 0.17, 0.19, 0.2, 0.56, 0.92, 0.92, 2.11, 2.11, 2.11, 2.11],
            'Mínimo': [0, 0.006, 0.012, 0.018, 0.022, 0.025, 0.029, 0.056, 0.082, 0.082, 0.57, 0.57, 0.57, 0.57],
            'Máximo': [0, 0.042, 0.163, 0.285, 0.349, 0.414, 0.478, 1.506, 2.534, 2.534, 2.534, 2.534, 2.534, 2.534],
            '% Resuspensión': [0, 1.5, 3, 4.5, 6, 7.5, 9, 10, 11, 12, 13, 16, 20, 23]
        }
        reference_table = pd.DataFrame(table1)
        st.dataframe(reference_table)

        st.write("Step 5: Merged tables")
        df = pd.merge(df, reference_table, on='Velocidad del viento (m/s)', how='left')
        st.dataframe(df)

        st.write("Step 6: Add LAI column")
        df['LAI (m2/m2)'] = lai
        st.dataframe(df)

        st.write('Step 7: add columns "Vd,min (cm/s)" and "Vd,max (cm/s)" and "Vd (cm/s)"')
        df['Vd,min (cm/s)'] = df['LAI (m2/m2)'] * df['Mínimo']
        df['Vd,max (cm/s)'] = df['LAI (m2/m2)'] * df['Máximo']
        df['Vd (cm/s)'] = df['LAI (m2/m2)'] * df['Promedio']
        st.dataframe(df)

        st.write("Step 8: Change unit measure")
        flux = pd.DataFrame()
        flux['MP2,5 (g/m³)']    = df['MP2,5 (µg/m³)'] / 1000 / 1000
        flux["Vd,min (m/s)"]    = df['Vd,min (cm/s)'] / 100
        flux["Vd,max (m/s)"]    = df['Vd,max (cm/s)'] / 100
        flux["Vd (m/s)"]        = df['Vd (cm/s)'] / 100
        flux["fmin,t (g/m2*h)"] = flux['MP2,5 (g/m³)'] * flux["Vd,min (m/s)"] * 3600
        flux["fmax,t (g/m2*h)"] = flux['MP2,5 (g/m³)'] * flux["Vd,max (m/s)"] * 3600
        flux["ft (g/m2*h)"]     = flux['MP2,5 (g/m³)'] * flux["Vd (m/s)"] * 3600
        st.dataframe(flux.style.format(precision=7))

        st.write('Step 9: New calculated table "Resuspension"')
        resuspension = pd.DataFrame()
        resuspension['% Resuspensión']  = df['% Resuspensión']
        resuspension['fmin,t (g/m2*h)'] = flux["fmin,t (g/m2*h)"]
        resuspension['fmax,t (g/m2*h)'] = flux["fmax,t (g/m2*h)"]
        resuspension['ft (g/m2*h)']     = flux["ft (g/m2*h)"]
        resuspension['At min (g/m2*h)'] = 0
        resuspension['At max (g/m2*h)'] = 0
        resuspension['At (g/m2*h)']     = 0
        resuspension['Rmin (g/m2*h)']   = 0
        resuspension['Rmax (g/m2*h)']   = 0
        resuspension['Rt (g/m2*h)']     = 0
        
        resuspension['Rmin (g/m2*h)']   = ( resuspension['At min (g/m2*h)'].shift(1) + resuspension['fmin,t (g/m2*h)'] ) * resuspension['% Resuspensión'] / 100
        resuspension['At min (g/m2*h)'] = resuspension['At min (g/m2*h)'].shift(1) + resuspension['fmin,t (g/m2*h)'] - resuspension['Rmin (g/m2*h)']
        resuspension['Rmax (g/m2*h)']   = ( resuspension['At max (g/m2*h)'].shift(1) + resuspension['fmax,t (g/m2*h)'] ) * resuspension['% Resuspensión'] / 100
        resuspension['At max (g/m2*h)'] = resuspension['At max (g/m2*h)'].shift(1) + resuspension['fmax,t (g/m2*h)'] - resuspension['Rmax (g/m2*h)']
        resuspension['Rt (g/m2*h)']     = ( resuspension['At (g/m2*h)'].shift(1) + resuspension['ft (g/m2*h)'] ) * resuspension['% Resuspensión'] / 100
        resuspension['At (g/m2*h)']     = resuspension['At (g/m2*h)'].shift(1) + resuspension['ft (g/m2*h)'] - resuspension['Rt (g/m2*h)']

        st.dataframe(resuspension.style.format(precision=12))