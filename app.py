import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GlobCare Dashboard", layout="wide")

st.title("📊 GlobCare KPI Dashboard")

# قراءة ملف الاكسل
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

st.success("Data Loaded Successfully ✅")

# عرض البيانات
st.subheader("Data Preview")
st.dataframe(df)

# اختيار الاعمدة الرقمية فقط
numeric_cols = df.select_dtypes(include="number")

# KPIs (الدوائر)
if len(numeric_cols.columns) > 0:

    st.subheader("KPIs")

    cols = st.columns(len(numeric_cols.columns))

    for i, col in enumerate(numeric_cols.columns):
        cols[i].metric(
            label=col,
            value=round(numeric_cols[col].sum(), 2)
        )

    # رسم بياني متغير
    st.subheader("📈 Dynamic Chart")

    selected_col = st.selectbox(
        "Choose column",
        numeric_cols.columns
    )

    fig = px.line(df, y=selected_col)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No numeric data found.")
