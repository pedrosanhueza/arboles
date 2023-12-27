import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file:

    st.write(uploaded_file.name)
    
    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded CSV File:")
    
    st.write(df)