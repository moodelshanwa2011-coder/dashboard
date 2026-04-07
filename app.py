import streamlit as st
import pandas as pd

st.title("📊 Excel Dashboard")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully ✅")

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Basic Info")
    st.write(df.describe())
