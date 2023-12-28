import streamlit as st
import pandas as pd

uploaded_files = st.file_uploader("Choose a CSV file")

if uploaded_files:
    
    df = pd.read_csv(uploaded_files)