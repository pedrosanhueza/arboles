import streamlit as st
import pandas as pd

sample_data = {
    'Fecha': ['1/1/22 0:00', '1/1/22 1:00', '1/1/22 2:00'],
    'MP2.5 (µg/m³)': [25.6, 7.0, 5.4],
    'Velocidad del viento (m/s)': ["3,0", "2,6", "1,8"],
    'Altura de Mezcla (m)': [124, 78, 52]
}

df = pd.DataFrame(sample_data)

st.title("Planilla I-tree Candelaria")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

with st.sidebar:

    lai = st.text_input("Leaf area index (LAI)👇","1.5")

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

import streamlit as st
import pandas as pd
from io import StringIO

st.title("Excel File Reader")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string-based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as a string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:

    # Checking file type and reading into a DataFrame
    if uploaded_file.name.endswith(('.xls', '.xlsx')):
        dataframe = pd.read_excel(uploaded_file, engine='openpyxl')
        st.dataframe(dataframe)  # Display DataFrame
    elif uploaded_file.name.endswith('.csv'):
        dataframe = pd.read_csv(uploaded_file)
        st.dataframe(dataframe)  # Display DataFrame
    else:
        st.warning("Unsupported file format. Please upload a CSV or Excel file.")

