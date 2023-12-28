import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file.name.endswith("xlsx"):
    
    df = pd.read_excel(uploaded_file)

elif uploaded_file.name.endswith("csv"):

    df = pd.read_csv(uploaded_file)

if uploaded_file:

    st.table(uploaded_file)