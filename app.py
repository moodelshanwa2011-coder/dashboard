import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background-color:#0b1220;
    color:white;
    font-family:Segoe UI;
}

.title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
}

.month {
    text-align:center;
    color:#9ca3af;
    margin-bottom:30px;
}

.grid {
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
    gap:25px;
    padding:20px;
}

.card {
    background:#111827;
    border-radius:15px;
    padding:20px;
    text-align:center;
}

.kpi-name {
    color:#9ca3af;
    margin-bottom:15px;
    font-size:15px;
}

.circle {
    width:120px;
    height:120px;
    border-radius:50%;
    margin:auto;
    background:#1f2937;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:26px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


# ---------- READ EXCEL ----------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]
metrics = df.columns[1:]

header = st.empty()
chart_holder = st.empty()

# ---------- LIVE LOOP ----------
while True:

    for i in range(len(df)):

        cards_html = ""

        values = []

        for metric in metrics:
            val = df.loc[i, metric]
            values.append(val)

            cards_html += f"""
            <div class="card">
                <div class="kpi-name">{metric}</div>
                <div class="circle">{val}</div>
            </div>
            """

        page_html = f"""
        <div class="title">GlobCare Performance Dashboard</div>
        <div class="month">Month: {months[i]}</div>

        <div class="grid">
            {cards_html}
        </div>
        """

        header.markdown(page_html, unsafe_allow_html=True)

        # ----- BAR CHART -----
        chart_df = pd.DataFrame({
            "KPI": metrics,
            "Value": values
        })

        fig = px.bar(chart_df, x="KPI", y="Value", text="Value")

        fig.update_layout(
            plot_bgcolor="#0b1220",
            paper_bgcolor="#0b1220",
            font_color="white"
        )

        chart_holder.plotly_chart(fig, use_container_width=True)

        time.sleep(10)
