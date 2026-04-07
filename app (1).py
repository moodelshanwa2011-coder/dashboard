
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.markdown(
    """
    <style>
    body {background-color: #0e1117;}
    .metric-card {
        background-color:#161b22;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 0 10px rgba(0,0,0,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 GlobCare KPI Dashboard")

# ----------------------
# Load Excel File
# ----------------------
FILE_NAME = "GlobCare -KPI_Dashboard_v5.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(FILE_NAME)
    return df

try:
    df = load_data()
except Exception as e:
    st.error("❌ Error loading Excel file. Make sure it exists in the repository.")
    st.stop()

st.write("### Data Preview")
st.dataframe(df.head())

# ----------------------
# KPIs (Auto detect numeric columns)
# ----------------------
numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) == 0:
    st.warning("No numeric columns found for KPIs.")
else:
    cols = st.columns(min(4, len(numeric_cols)))
    for i, col in enumerate(numeric_cols[:4]):
        value = df[col].sum()
        cols[i].metric(label=col, value=f"{value:,.0f}")

# ----------------------
# Charts Section
# ----------------------
st.markdown("## 📈 Interactive Charts")

if len(numeric_cols) >= 1:
    col_to_plot = st.selectbox("Choose column", numeric_cols)

    fig = px.line(df, y=col_to_plot, title=f"{col_to_plot} Trend")
    st.plotly_chart(fig, use_container_width=True)

if len(numeric_cols) >= 2:
    fig2 = px.bar(df, x=df.index, y=numeric_cols[0], title=f"{numeric_cols[0]} Distribution")
    st.plotly_chart(fig2, use_container_width=True)
