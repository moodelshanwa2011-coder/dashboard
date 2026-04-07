import streamlit as st
import pandas as pd

st.title("UPLOAD TEST")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("Uploaded ✅")
    st.dataframe(df)
