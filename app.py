import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:34px;
    font-weight:bold;
    margin-bottom:0px;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:gray;
    margin-bottom:25px;
}

.container{
    text-align:center;
}

.circle{
    width:130px;
    height:130px;
    border-radius:50%;
    background:#1976D2;
    color:white;
    display:inline-flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin:12px;
    box-shadow:0px 5px 14px rgba(0,0,0,0.25);
}

.kpi-name{
    font-size:14px;
    margin-bottom:6px;
}

.kpi-value{
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOAD EXCEL ----------------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

# أول عمود = الشهر
months = df.iloc[:,0]

# باقي الأعمدة = KPI names
kpis = df.columns[1:]

placeholder = st.empty()

# ---------------- LIVE LOOP ----------------
while True:

    for i in range(len(df)):

        month_name = months[i]

        circles_html = ""

        # إنشاء الدواير من الاكسل
        for kpi in kpis:
            value = df.loc[i, kpi]

            circles_html += f"""
            <div class="circle">
                <div class="kpi-name">{kpi}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """

        placeholder.markdown(f"""
        <div class="main-title">📊 GlobCare KPI Dashboard</div>
        <div class="sub-title">بيانات شهر {month_name}</div>

        <div class="container">
            {circles_html}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(10)
