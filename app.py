import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Interactive Excel Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.success("File Uploaded Successfully ✅")

    # فلتر الشهر
    if "Month" in df.columns:
        month = st.selectbox("Select Month", df["Month"].unique())
        df = df[df["Month"] == month]

    # أرقام سريعة
    col1, col2 = st.columns(2)

    col1.metric("عدد الصفوف", len(df))

    # تحويل Actual لأرقام بشكل آمن
if "Actual" in df.columns:
    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")

    avg_actual = df["Actual"].mean()

    if pd.notnull(avg_actual):
        col2.metric("متوسط Actual", round(avg_actual, 2))

    # رسم بياني
    if "KPI" in df.columns and "Actual" in df.columns:
        st.subheader("Actual Performance")
        st.bar_chart(df.set_index("KPI")["Actual"])

    # الجدول
    st.subheader("Data")
    st.dataframe(df)
