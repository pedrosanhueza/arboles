import streamlit as st
import pandas as pd

uploadedFile = st.file_uploader("fileUploadLabel", type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")

try:
    df=pd.read_csv(uploadedFile, error_bad_lines=True, warn_bad_lines=False)
except:
    try:
            df = pd.read_excel(uploadedFile)
    except:      
            df=pd.DataFrame()

if df:
    st.table(df)