import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:

    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
