import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ======================
# PAGE SETUP
# ======================
st.set_page_config(layout="wide")
st.title("🟢 LIVE KPI DASHBOARD")

# ======================
# FILE UPLOAD
# ======================
file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:

    # قراءة الشيتات
    sheets = pd.ExcelFile(file).sheet_names
    sheet = st.selectbox("Choose Sheet", sheets)

    # قراءة البيانات
    df = pd.read_excel(file, sheet_name=sheet)
    df.columns = df.columns.str.strip()

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    # اختيار الأعمدة
    text_col = st.selectbox("KPI Column", df.columns)
    num_col = st.selectbox("Value Column", df.columns)

    # ======================
    # CREATE DASHBOARD
    # ======================
    if st.button("Create Dashboard"):

        # تحويل للأرقام (منع الأخطاء)
        df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
        df = df.dropna(subset=[num_col])

        # ===== KPI METRICS =====
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", len(df))
        c2.metric("Total", round(df[num_col].sum(), 2))
        c3.metric("Average", round(df[num_col].mean(), 2))
        c4.metric("Max", round(df[num_col].max(), 2))

        st.divider()

        # ===== CHART =====
        fig = px.bar(
            df,
            x=text_col,
            y=num_col,
            title="Live KPI Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬆️ Upload Excel file to start")

# ======================
# AUTO REFRESH (LIVE)
# ======================
time.sleep(30)
st.rerun()
