import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🟢 LIVE DASHBOARD")

# ===== Upload =====
file = st.file_uploader("Upload Excel", type=["xlsx"])

if file is not None:

    df = pd.read_excel(file)

    # اختيار الأعمدة تلقائياً
    text_col = df.select_dtypes(include="object").columns[0]
    num_col = df.select_dtypes(include="number").columns[0]

    # ===== KPI CIRCLES =====
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Total", round(df[num_col].sum(),2))
    c3.metric("Average", round(df[num_col].mean(),2))
    c4.metric("Max", round(df[num_col].max(),2))

    st.divider()

    # ===== CHART =====
    fig = px.bar(df, x=text_col, y=num_col)
    st.plotly_chart(fig, use_container_width=True)

    # ===== TABLE =====
    st.dataframe(df, use_container_width=True)

else:
    st.info("⬆️ Upload your Excel file")
