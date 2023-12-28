import streamlit as st
import pandas as pd

uploadedFile = st.file_uploader("fileUploadLabel", type=['csv','xlsx'])

if uploadedFile:
    
    st.write(uploadedFile.name)

    st.table(uploadedFile)

    st.write(uploadedFile)