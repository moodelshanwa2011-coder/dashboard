import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("GlobCare Performance Dashboard")

# تحديث تلقائي كل 10 ثواني
count = st_autorefresh(interval=10000, key="refresh")

# قراءة الاكسل
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

# تنظيف البيانات
df = df.dropna(how="all")

# أول عمود = Month
months = df.iloc[:, 0]

# باقي الأعمدة KPI
kpis = df.iloc[:, 1:]

# اختيار شهر تلقائي
index = count % len(df)

current_month = months.iloc[index]
current_values = kpis.iloc[index]

st.subheader(f"Month: {current_month}")

# ===== KPI CIRCLES (بطاقات) =====
cols = st.columns(len(current_values))

values_list = []

for col, (name, value) in zip(cols, current_values.items()):
    col.metric(label=name, value=value)
    values_list.append(value)

# ===== BAR CHART =====
chart_df = pd.DataFrame({
    "KPI": current_values.index,
    "Value": pd.to_numeric(values_list, errors="coerce")
})

fig = px.bar(chart_df, x="KPI", y="Value", text="Value")

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)
