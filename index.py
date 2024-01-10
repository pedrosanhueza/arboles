import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP, getcontext

# ---------------------- #
# ------ SIDE BAR ------ #
# ---------------------- #

with st.sidebar:
    
    lai = st.number_input('Leaf area index (LAI)', value=0.15)
    tc = st.number_input('Porcentaje de superficie cubierta', value=5)

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

        df = pd.read_excel(uploaded_file, dtype=str)

    elif fileName.endswith("csv"):

        df = pd.read_csv(uploaded_file, dtype=str)

    else:

        st.warning('Error in file upload', icon="⚠️")

# ------------------------- #
# ------ CALCULATIONS ----- #
# ------------------------- #

at_min = Decimal('0')
at_max = Decimal('0')
at_avg = Decimal('0')
r_min  = Decimal('0')
r_max  = Decimal('0')
r_avg  = Decimal('0')

suma_change_c_avg = 0
suma_change_c_min = 0
suma_change_c_max = 0

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

    # replace zeros for multiplication
    df['MP2,5 (µg/m³)'].replace('0', '0.00000001', inplace=True)
    df['Altura de Mezcla (m)'].replace('0', '0.00000001', inplace=True)

    # replace comma with dots
    df = df.applymap(lambda x: str(x).replace(',', '.'))

    # convert values to decimals
    df = df.applymap(lambda x: Decimal(x) if pd.notna(x) else x)

    lai = Decimal(lai)
    tc = Decimal(tc)

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

    columns_zip = zip(
    df['MP2,5 (µg/m³)'],
    df['Velocidad del viento (m/s)'],
    df['Altura de Mezcla (m)'],
    df['Promedio'],
    df['Mínimo'],
    df['Máximo'],
    df['% Resuspensión'],
    )

    for mp25, vv, h, avg, min, max, resus in columns_zip:

        vd_avg = lai * avg
        vd_min = lai * min
        vd_max = lai * max

        mp25_g   = mp25 / 1000000

        vd_avg_m = vd_avg / 100
        vd_min_m = vd_min / 100
        vd_max_m = vd_max / 100

        f_avg = 3600 * mp25_g * vd_avg_m
        f_min = 3600 * mp25_g * vd_min_m
        f_max = 3600 * mp25_g * vd_max_m


        r_avg = ( at_avg + f_avg ) * resus / 100
        at_avg = at_avg + f_avg - r_avg
        r_min = ( at_min + f_min ) * resus / 100
        at_min = at_min + f_min - r_min
        r_max = ( at_max + f_max ) * resus / 100
        at_max = at_max + f_max - r_max

        f_neto_avg = f_avg - r_avg
        f_neto_min = f_min - r_min
        f_neto_max = f_max - r_max

        f_ugm2h_avg = f_neto_avg * 1000000
        f_ugm2h_min = f_neto_min * 1000000
        f_ugm2h_max = f_neto_max * 1000000

        m_total = mp25 * h

        i_Unit_avg = f_ugm2h_avg * 100 / m_total if f_ugm2h_avg < 1 else f_ugm2h_avg * 100 / (m_total + f_ugm2h_avg)
        i_Unit_min = f_ugm2h_min * 100 / m_total if f_ugm2h_min < 1 else f_ugm2h_min * 100 / (m_total + f_ugm2h_min)
        i_Unit_max = f_ugm2h_max * 100 / m_total if f_ugm2h_max < 1 else f_ugm2h_max * 100 / (m_total + f_ugm2h_max)

        i_total_avg = f_ugm2h_avg * tc / 100 * 100 / (f_ugm2h_avg * tc / 100 + m_total)
        i_total_min = f_ugm2h_min * tc / 100 * 100 / (f_ugm2h_min * tc / 100+ m_total)
        i_total_max = f_ugm2h_max * tc / 100 * 100 / (f_ugm2h_max * tc / 100+ m_total)

        change_c_avg = mp25 / (1 - i_total_avg / 100) - mp25
        change_c_min = mp25 / (1 - i_total_min / 100) - mp25
        change_c_max = mp25 / (1 - i_total_max / 100) - mp25

        suma_change_c_avg += change_c_avg
        suma_change_c_min += change_c_min
        suma_change_c_max += change_c_max
    
    st.write(suma_change_c_avg)