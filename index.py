import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded CSV File:")

    st.write(df)

    st.write(uploaded_file.name)