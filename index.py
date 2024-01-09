import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP, getcontext

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

    # convert values to decimals
    df = df.applymap(lambda x: Decimal(x) if pd.notna(x) else x)

    lai = Decimal('0.15')
    tc = Decimal('0.05')

    # round values in Velocidad del viento
    getcontext().rounding = ROUND_HALF_UP
    decimal_places = 0
    def round_half_up(value):
        return Decimal(str(value)).quantize(Decimal('1e-{0}'.format(decimal_places)))
    # Apply the rounding function to the specified column
    df['Velocidad del viento (m/s)'] = df['Velocidad del viento (m/s)'].apply(lambda x: round_half_up(x))

    table1 = {
        'Velocidad del viento (m/s)': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
        'Promedio': ['0', '0.03', '0.09', '0.15', '0.17', '0.19', '0.2', '0.56', '0.92', '0.92', '2.11', '2.11', '2.11', '2.11'],
        'Mínimo': ['0', '0.006', '0.012', '0.018', '0.022', '0.025', '0.029', '0.056', '0.082', '0.082', '0.57', '0.57', '0.57', '0.57'],
        'Máximo': ['0', '0.042', '0.163', '0.285', '0.349', '0.414', '0.478', '1.506', '2.534', '2.534', '2.534', '2.534', '2.534', '2.534'],
        '% Resuspensión': ['0', '1.5', '3', '4.5', '6', '7.5', '9', '10', '11', '12', '13', '16', '20', '23']
    }

    reference_table = pd.DataFrame(table1).applymap(lambda x: Decimal(x) if pd.notna(x) else x)

    df = pd.merge(df, reference_table, on='Velocidad del viento (m/s)', how='left')

    df['Vd (cm/s)']     = lai * df['Promedio']
    df['Vd,min (cm/s)'] = lai * df['Mínimo']
    df['Vd,max (cm/s)'] = lai * df['Máximo']

    st.dataframe(df)