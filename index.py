import streamlit as st
import pandas as pd

uploadedFile = st.file_uploader("fileUploadLabel", type=['csv','xlsx'])

st.write(uploadedFile.name)