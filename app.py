import streamlit as st
import pandas as pd

st.title("📊 Excel Dashboard")

# رفع ملف الاكسل
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df)

    # اختيار عمود رقمي
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        st.subheader("📈 Charts")

        column = st.selectbox("Choose column", numeric_cols)

        st.bar_chart(df[column])
    else:
        st.warning("No numeric columns found.")
