import streamlit as st
import pandas as pd

def read_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.title("Excel Reader App")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.subheader("Preview of Data:")
        df = read_excel(uploaded_file)

        if df is not None:
            st.dataframe(df)

if __name__ == "__main__":
    main()
