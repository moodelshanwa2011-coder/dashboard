import streamlit as st
import time

st.set_page_config(layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

.title{
    text-align:center;
    font-size:32px;
    font-weight:bold;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:20px;
}

.container{
    text-align:center;
}

.circle{
    width:110px;
    height:110px;
    border-radius:50%;
    background:#2196F3;
    color:white;
    display:inline-flex;
    justify-content:center;
    align-items:center;
    font-size:24px;
    font-weight:bold;
    margin:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)


# ---------- DATA (زودنا عدد الدواير) ----------
months = [
    {"name":"يناير","values":[10,20,30,40,50,60]},
    {"name":"فبراير","values":[15,25,35,45,55,65]},
    {"name":"مارس","values":[12,22,32,42,52,62]},
    {"name":"ابريل","values":[18,28,38,48,58,68]},
]

placeholder = st.empty()

# ---------- AUTO REFRESH ----------
while True:
    for month in months:

        circles_html = "".join(
            [f'<div class="circle">{v}</div>' for v in month["values"]]
        )

        placeholder.markdown(f"""
        <div class="title">📊 Dashboard Live</div>
        <div class="subtitle">بيانات شهر {month["name"]}</div>

        <div class="container">
            {circles_html}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(10)
