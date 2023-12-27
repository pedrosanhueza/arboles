import streamlit as st
import pandas as pd

sample_data = {
    'Fecha': ['1/1/22 0:00', '1/1/22 1:00', '1/1/22 2:00'],
    'MP2.5 (µg/m³)': [25.6, 7.0, 5.4],
    'Velocidad del viento (m/s)': ["3,0", "2,6", "1,8"],
    'Altura de Mezcla (m)': [124, 78, 52]
}

df = pd.DataFrame(sample_data)

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

lai = st.slider(
    "Leaf area index (LAI)"
    min_value=0,
    max_value=10,
    value=0.15,
    step=0.05
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded CSV File:")

    st.write(df)

    st.write(uploaded_file.name)

# Replace commmas to dots for "Velocidad del viento (m/s)" column
    
df[df.columns[2]] = df[df.columns[2]].astype(str)

df[df.columns[2]] = df[df.columns[2]].apply(lambda x: x.replace(",","."))

df[df.columns[2]] = df[df.columns[2]].astype(float)

