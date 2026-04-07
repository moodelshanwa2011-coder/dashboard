import streamlit as st
import pandas as pd

st.title("GlobCare KPI Dashboard")

try:
    df = pd.read_excel("data.xlsx")
    st.success("File loaded successfully ✅")
    st.dataframe(df)

    nums = df.select_dtypes(include="number")

    if not nums.empty:
        st.subheader("KPIs")
        cols = st.columns(len(nums.columns))

        for i, c in enumerate(nums.columns):
            cols[i].metric(c, int(nums[c].sum()))

except Exception as e:
    st.error("Error reading Excel file")
    st.write(e)
