import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")

st.title("GlobCare Performance Dashboard")

# قراءة ملف الاكسل
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:, 0]
kpis = df.columns[1:]

placeholder = st.empty()

# تشغيل لايف
while True:

    for i in range(len(df)):

        with placeholder.container():

            st.subheader(f"Month: {months[i]}")

            # ===== KPI CIRCLES =====
            cols = st.columns(len(kpis))

            values = []

            for col, kpi in zip(cols, kpis):

                value = df.loc[i, kpi]
                values.append(value)

                col.metric(
                    label=kpi,
                    value=value
                )

            # ===== BAR CHART =====
            chart_df = pd.DataFrame({
                "KPI": kpis,
                "Value": values
            })

            fig = px.bar(
                chart_df,
                x="KPI",
                y="Value",
                text="Value"
            )

            st.plotly_chart(fig, use_container_width=True)

        time.sleep(10)
