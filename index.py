import streamlit as st
import pandas as pd
from io import StringIO, BytesIO

st.title("Excel File Reader")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string-based or binary IO:
    if uploaded_file.encoding is not None:
        # Text file, decode as UTF-8
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as a string:
        string_data = stringio.read()
        st.write(string_data)
    else:
        # Binary file, use BytesIO
        bytesio = BytesIO(uploaded_file.getvalue())
        st.write(bytesio)

        # Handle binary file as needed, e.g., for Excel files
        if uploaded_file.name.endswith(('.xls', '.xlsx')):
            dataframe = pd.read_excel(bytesio, engine='openpyxl')
            st.dataframe(dataframe)  # Display DataFrame
        else:
            st.warning("Unsupported binary file format. Please upload a text file or Excel file.")
