import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 GlobCare KPI Dashboard")

# تحميل البيانات
df = pd.read_excel("data.xlsx")

st.success("Data Loaded ✅")

# عرض عدد الصفوف والأعمدة
col1, col2 = st.columns(2)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])

# اختيار عمود للرسم
st.subheader("Chart")

numeric_cols = df.select_dtypes(include="number")

if len(numeric_cols.columns) > 0:
    selected_col = st.selectbox(
        "Choose column",
        numeric_cols.columns
    )

    fig = px.line(df, y=selected_col)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No numeric data found")

# عرض البيانات
st.subheader("Data Table")
st.dataframe(df)
