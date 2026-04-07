import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("ICU Performance Dashboard - Riyadh")

# تحديث كل 10 ثواني
count = st_autorefresh(interval=10000, key="refresh")

# =========================
# DATA (من الصورة)
# =========================

data = [
    {
        "Month": "1Q 2024",
        "Patient Falls": 0.24,
        "Injury Falls": 0.26,
        "Pressure Injury": 14.29,
        "CLABSI": 2.47,
        "VAE": 2.48,
        "CAUTI": 0.98
    },
    {
        "Month": "2Q 2024",
        "Patient Falls": 0.31,
        "Injury Falls": 0.30,
        "Pressure Injury": 6.90,
        "CLABSI": 2.63,
        "VAE": 0,
        "CAUTI": 1.02
    },
    {
        "Month": "3Q 2024",
        "Patient Falls": 0.00,
        "Injury Falls": 0.01,
        "Pressure Injury": 9.54,
        "CLABSI": 1.80,
        "VAE": 1.10,
        "CAUTI": 1.13
    },
    {
        "Month": "1Q 2025",
        "Patient Falls": 1.59,
        "Injury Falls": 0.80,
        "Pressure Injury": 4.17,
        "CLABSI": 3.02,
        "VAE": 6.69,
        "CAUTI": 0.00
    }
]

df = pd.DataFrame(data)

# اختيار شهر تلقائي
index = count % len(df)
row = df.iloc[index]

st.subheader(f"Month: {row['Month']}")

# =========================
# KPI CIRCLES (بطاقات)
# =========================

kpi_data = row.drop("Month")

cols = st.columns(len(kpi_data))

for col, (name, value) in zip(cols, kpi_data.items()):
    col.metric(label=name, value=value)

# =========================
# BAR CHART
# =========================

chart_df = pd.DataFrame({
    "KPI": kpi_data.index,
    "Value": kpi_data.values
})

fig = px.bar(chart_df, x="KPI", y="Value", text="Value")

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)
