import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ======================
# PAGE SETTINGS
# ======================
st.set_page_config(layout="wide")
st.title("🟢 Live KPI Dashboard")

# ======================
# AUTO REFRESH (بدون مكتبات إضافية)
# ======================
count = st.empty()
for seconds in range(20, 0, -1):
    count.info(f"🔄 Refreshing in {seconds} sec")
    time.sleep(1)

st.rerun()

# ======================
# FILE UPLOAD
# ======================
file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:

    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    # تحويل الأرقام
    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")
    df["Target"] = pd.to_numeric(df["Target"], errors="coerce")

    # ======================
    # KPI CALCULATIONS
    # ======================
    total_kpi = len(df)
    avg_actual = df["Actual"].mean()
    total_actual = df["Actual"].sum()
    achievement = (total_actual / df["Target"].sum()) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📊 Total KPIs", total_kpi)
    col2.metric("🎯 Avg Actual", round(avg_actual, 2))
    col3.metric("💰 Total Actual", round(total_actual, 2))
    col4.metric("✅ Achievement", f"{achievement:.1f}%")

    st.divider()

    # ======================
    # CHART
    # ======================
    fig = px.bar(
        df,
        x="KPI",
        y="Actual",
        color="Category",
        title="Actual Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Data Table")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("Upload Excel file first")
