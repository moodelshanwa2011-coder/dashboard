import streamlit as st
import time

st.set_page_config(layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

.circle{
    width:100px;
    height:100px;
    border-radius:50%;
    background:#4CAF50;
    color:white;
    display:inline-flex;
    justify-content:center;
    align-items:center;
    font-size:22px;
    margin:10px;
}

.container{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


# ---------- DATA ----------
months = [
    {"name":"يناير","values":[10,20,30]},
    {"name":"فبراير","values":[15,25,35]},
    {"name":"مارس","values":[12,22,32]},
    {"name":"ابريل","values":[18,28,38]},
]

placeholder = st.empty()

# ---------- AUTO CHANGE EVERY 10 SECONDS ----------
while True:
    for month in months:

        circles_html = "".join(
            [f'<div class="circle">{v}</div>' for v in month["values"]]
        )

        placeholder.markdown(f"""
        <div class="container">
            <h2>{month["name"]}</h2>
            {circles_html}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(10)
