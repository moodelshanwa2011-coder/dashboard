import streamlit as st
import pandas as pd
import plotly.express as px
import time

# =============================
# PAGE SETTINGS
# =============================
st.set_page_config(page_title="Interactive Excel Dashboard", layout="wide")

st.title("📊 Interactive Excel Dashboard")

# =============================
# AUTO REFRESH (بدون مكتبات)
# =============================
REFRESH_SECONDS = 30

placeholder = st.empty()

with placeholder.container():

    # =============================
    # FILE UPLOAD
    # =============================
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file)

        st.success("File Uploaded Successfully ✅")

        # تنظيف الأعمدة
        df.columns = df.columns.str.strip()

        # =============================
        # MONTH FILTER
        # =============================
        if "Month" in df.columns:
            months = df["Month"].dropna().unique()

            selected_month = st.selectbox(
                "Select Month",
                months
            )

            df = df[df["Month"] == selected_month]

        # =============================
        # تحويل Actual
        # =============================
        if "Actual" in df.columns:
            df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")

        # =============================
        # KPI CARDS
        # =============================
        st.subheader("Key Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(df))

        if "Actual" in df.columns:
            col2.metric(
                "Average Actual",
                round(df["Actual"].mean(), 2)
            )

            col3.metric(
                "Max Actual",
                round(df["Actual"].max(), 2)
            )

        # =============================
        # CHART
        # =============================
        st.subheader("Actual Performance")

        if "KPI" in df.columns and "Actual" in df.columns:

            chart_data = (
                df.groupby("KPI", as_index=False)["Actual"]
                .mean()
            )

            fig = px.bar(
                chart_data,
                x="KPI",
                y="Actual",
                title="Average Actual per KPI"
            )

            st.plotly_chart(fig, use_container_width=True)

        # =============================
        # TABLE
        # =============================
        st.subheader("Data")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("Please upload Excel file")

# =============================
# AUTO REFRESH LOOP
# =============================
time.sleep(REFRESH_SECONDS)
st.rerun()
