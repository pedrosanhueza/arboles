import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        # Read the contents of the file
        bytes_data = uploaded_file.getvalue()

        # Specify the encoding (assuming UTF-8)
        encoding = 'utf-8'

        # Convert bytes to string using the specified encoding
        s = str(bytes_data, encoding)

        # Use StringIO to create a file-like object for pandas to read
        result = StringIO(s)

        # Now you can use pandas to read the Excel file
        df = pd.read_excel(result)

        # Display the DataFrame
        st.write(df)

    except UnicodeDecodeError:
        st.write("Error: Unable to decode the file. Please make sure it is a valid Excel file.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
