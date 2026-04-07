import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")
st.title("🟢 Live Excel Dashboard")

# ======================
# Upload Excel
# ======================
file = st.file_uploader("Upload Excel File", type=["xlsx"])

if file:

    df = pd.read_excel(file)

    # تنظيف الأعمدة تلقائياً (بدون ما نعرف اسمها)
    df.columns = df.columns.str.strip()

    # اختيار أول عمود نصي = اسم KPI
    text_cols = df.select_dtypes(include="object").columns
    num_cols = df.select_dtypes(include="number").columns

    if len(text_cols) == 0 or len(num_cols) == 0:
        st.error("Excel must contain text column + numbers")
        st.stop()

    kpi_col = text_cols[0]
    value_col = num_cols[0]

    # ======================
    # KPI CIRCLES (أرقام داخل دوائر)
    # ======================
    total_items = len(df)
    total_value = df[value_col].sum()
    avg_value = df[value_col].mean()
    max_value = df[value_col].max()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Items", total_items)
    c2.metric("Total", round(total_value,2))
    c3.metric("Average", round(avg_value,2))
    c4.metric("Max", round(max_value,2))

    st.divider()

    # ======================
    # LIVE BAR CHART
    # ======================
    fig = px.bar(
        df,
        x=kpi_col,
        y=value_col,
        title="Live Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

else:
    st.info("Upload Excel file")

# ======================
# AUTO REFRESH
# ======================
time.sleep(20)
st.rerun()
