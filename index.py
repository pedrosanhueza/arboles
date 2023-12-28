import streamlit as st
import pandas as pd

uploadedFile = st.file_uploader("fileUploadLabel", type=['csv','xlsx'])

if uploadedFile:
    try:
        bytesData = uploadedFile.getvalue()
        encoding = encodingUTF8 
        s=str(bytesData,encoding)
        result = StringIO(s) 
    except:
        st.write("pass")