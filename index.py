import streamlit as st
import pandas as pd
from openpyxl import load_workbook

sample_data = {
    'Fecha': ['1/1/22 0:00', '1/1/22 1:00', '1/1/22 2:00'],
    'MP2.5 (µg/m³)': [25.6, 7.0, 5.4],
    'Velocidad del viento (m/s)': ["3,0", "2,6", "1,8"],
    'Altura de Mezcla (m)': [124, 78, 52]
}

df = pd.DataFrame(sample_data)

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

col1, col2 = st.columns(2)

with col1:

    lai = st.text_input("Leaf area index (LAI)👇","1.5")

with col2:

    superficie = st.text_input("Porcentage de la superficie cubierta con la vegetacion👇","5.0")

tabla1 = {
    'Velocidad viento (m/s)': [0, 0.03, 0.09, 0.15, 0.17, 0.19, 0.2, 0.56, 0.92, 0.92, 2.11, 2.11, 2.11, 2.11],
    'Promedio': [0, 0.006, 0.012, 0.018, 0.022, 0.025, 0.029, 0.056, 0.082, 0.082, 0.57, 0.57, 0.57, 0.57],
    'Mínimo': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.57, 0.57, 0.57, 0.57],
    'Máximo': [0, 0.042, 0.163, 0.285, 0.349, 0.414, 0.478, 1.506, 2.534, 2.534, 2.534, 2.534, 2.534, 2.534],
    '% Resuspensión': [0, 1.5, 3, 4.5, 6, 7.5, 9, 10, 11, 12, 13, 16, 20, 23]
}

Tabla1 = pd.DataFrame(tabla1)

# st.table(Tabla1)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded CSV File:")

    st.write(df)

    st.write(uploaded_file.name)

# Replace commmas to dots for "Velocidad del viento (m/s)" column
    
df[df.columns[2]] = df[df.columns[2]].astype(str)

df[df.columns[2]] = df[df.columns[2]].apply(lambda x: x.replace(",","."))

df[df.columns[2]] = df[df.columns[2]].astype(float)


def read_excel(file):
    df = pd.DataFrame()
    try:
        with pd.ExcelFile(file) as xls:
            sheet_names = xls.sheet_names
            sheet = st.selectbox("Select Sheet", sheet_names)
            df = pd.read_excel(file, sheet_name=sheet)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
    return df


st.title("Excel File Reader")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = read_excel(uploaded_file)
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("Selected sheet is empty or could not be loaded.")

st.table(df)
