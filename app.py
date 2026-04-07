import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 GlobCare KPI Dashboard")

# Read Excel
df = pd.read_excel("data.xlsx")

st.success("File loaded successfully ✅")

# ===== Convert numbers safely =====
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# ===== KPIs =====
st.subheader("Key Metrics")

numeric_cols = df.select_dtypes(include="number")

if len(numeric_cols.columns) > 0:

    cols = st.columns(len(numeric_cols.columns))

    for i, col in enumerate(numeric_cols.columns):
        cols[i].metric(col, int(numeric_cols[col].sum()))

else:
    st.warning("⚠️ No numeric columns detected")

# ===== Charts =====
st.subheader("Data Visualization")

if len(numeric_cols.columns) > 0:

    chart_col = numeric_cols.columns[0]

    fig = px.bar(
        df,
        x=df.columns[0],
        y=chart_col,
        title=f"{chart_col} Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

# ===== Data Table =====
st.subheader("Full Data")
st.dataframe(df)
