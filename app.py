import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("GlobCare Performance Dashboard")

# تحديث الصفحة كل 10 ثواني
count = st_autorefresh(interval=10000, key="refresh")

# قراءة الاكسل
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

# تحديد الشهر الحالي تلقائياً
row_index = count % len(df)

month = df.iloc[row_index, 0]
data = df.iloc[row_index, 1:]

st.subheader(f"Month: {month}")

# ===== KPI BOXES =====
cols = st.columns(len(data))

for col, (name, value) in zip(cols, data.items()):
    col.metric(label=name, value=value)

# ===== CHART =====
chart_df = pd.DataFrame({
    "KPI": data.index,
    "Value": data.values
})

fig = px.bar(chart_df, x="KPI", y="Value", text="Value")

st.plotly_chart(fig, use_container_width=True)
