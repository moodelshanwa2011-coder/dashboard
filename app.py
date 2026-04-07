import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# إعداد الصفحة
st.set_page_config(page_title="ICU Riyadh Master Dashboard", layout="wide")

# 1. قاعدة البيانات المستخرجة من المستند (8 مؤشرات عبر الأرباع السنوية)
# تم دمج بيانات الوحدة (Unit) مع المرجع (Benchmark) لكل مؤشر
raw_data = {
    "Quarter": ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024", "1Q 2025", "2Q 2025", "3Q 2025"],
    "Total Falls": [0, 0.24, 0.06, 0.36, 0, 1.59, 0.18, 0], # 
    "Falls_BM": [0.04, 0.09, 0.24, 0.28, 0.14, 0.12, 0, 0.25], # NDNQI Mean 
    "HAPI %": [7.30, 6.45, 6.54, 4.60, 4.61, 4.17, 6.67, 3.33], # 
    "HAPI_BM": [26.67, 7.77, 14.29, 6.9, 9.68, 4.96, 4.58, 4.97], # 
    "CLABSI": [1.38, 1.28, 1.56, 1.20, 1.8, 1.26, 1.50, 1.09], # 
    "CLABSI_BM": [1.3, 2.67, 2.42, 2.63, 1.21, 3.02, 3.38, 3.87], # 
    "VAE (Ventilator)": [1.57, 2.17, 2.04, 1.89, 2.49, 1.91, 1.6, 1.39], # 
    "VAE_BM": [1.06, 2.42, 0, 0, 1.6, 6.69, 3.4, 3.33], # 
    "CAUTI": [0, 0.70, 0.67, 0.40, 0.54, 0.43, 0, 0.6], # 
    "CAUTI_BM": [0.46, 0.99, 0.51, 1.02, 1.13, 0, 0.44, 0.54], # 
    "Nurse Turnover %": [5.21, 4.84, 3.74, 4.51, 4.16, 1.43, 3.22, 3.69], # 
    "Turnover_BM": [1.6, 4.49, 6.25, 4.69, 4.35, 3.97, 2.9, 5.74], # 
    "BSN Education %": [67.19, 82.99, 82.74, 83.36, 83.30, 83.78, 85.01, 85.25], # 
    "BSN_BM": [83.53, 70.31, 71.21, 68.25, 71.83, 70, 70.59, 71.83], # 
    "Total RN Hours": [13, 20.14, 18.22, 18.34, 18.93, 18.28, 18.48, 11.97], # 
    "Hours_BM": [7.99, 19.09, 12.54, 19.20, 12.39, 19.82, 12.87, 19.15] # 
}

df = pd.DataFrame(raw_data)

def draw_circle_kpi(label, current_val, benchmark_val, unit):
    # المنطق: إذا زادت الإصابات عن المرجع فهي باللون الأحمر، وإذا قلت فهي زرقاء
    # استثناء: في التعليم (BSN) وساعات العمل، الزيادة تكون إيجابية (زرقاء)
    is_bad = current_val > benchmark_val if "Education" not in label and "Hours" not in label else current_val < benchmark_val
    color = "#FF0000" if is_bad else "#007BFF"
    
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = current_val,
        delta = {'reference': benchmark_val, 'relative': False, 'valueformat': ".2f"},
        number = {'font': {'color': color, 'size': 45}, 'suffix': unit},
        title = {'text': label, 'font': {'size': 18}},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(height=220, margin=dict(l=10, r=10, t=40, b=10))
    return fig

# --- حلقة العرض اللانهائية ---
st.title("🏥 لوحة مراقبة أداء ICU - الرياض")
placeholder = st.empty()

while True:
    for i in range(len(df)):
        with placeholder.container():
            row = df.iloc[i]
            st.markdown(f"## الربع السنوي الحالي: <span style='color:#007BFF'>{row['Quarter']}</span>", unsafe_allow_html=True)
            
            # عرض 8 دوائر KPI في شبكة 2x4
            c1, c2, c3, c4 = st.columns(4)
            c5, c6, c7, c8 = st.columns(4)
            
            # الصف الأول
            c1.plotly_chart(draw_circle_kpi("سقوط المرضى", row["Total Falls"], row["Falls_BM"], ""), use_container_width=True)
            c2.plotly_chart(draw_circle_kpi("إصابات الضغط HAPI", row["HAPI %"], row["HAPI_BM"], "%"), use_container_width=True)
            c3.plotly_chart(draw_circle_kpi("عدوى الدم CLABSI", row["CLABSI"], row["CLABSI_BM"], ""), use_container_width=True)
            c4.plotly_chart(draw_circle_kpi("جهاز التنفس VAE", row["VAE (Ventilator)"], row["VAE_BM"], ""), use_container_width=True)
            
            # الصف الثاني
            c5.plotly_chart(draw_circle_kpi("عدوى المسالك CAUTI", row["CAUTI"], row["CAUTI_BM"], ""), use_container_width=True)
            c6.plotly_chart(draw_circle_kpi("دوران التمريض", row["Nurse_Turnover %"], row["Turnover_BM"], "%"), use_container_width=True)
            c7.plotly_chart(draw_circle_kpi("تعليم التمريض BSN", row["BSN Education %"], row["BSN_BM"], "%"), use_container_width=True)
            c8.plotly_chart(draw_circle_kpi("ساعات عمل التمريض", row["Total RN Hours"], row["Hours_BM"], "h"), use_container_width=True)
            
            # بار تشارت سفلي يعكس تغير الأداء
            st.divider()
            metrics_names = ["Falls", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN", "RN Hours"]
            current_vals = [row["Total Falls"], row["HAPI %"], row["CLABSI"], row["VAE (Ventilator)"], row["CAUTI"], row["Nurse_Turnover %"], row["BSN Education %"], row["Total RN Hours"]]
            
            fig_bar = go.Figure(data=[go.Bar(x=metrics_names, y=current_vals, marker_color='#007BFF')])
            fig_bar.update_layout(title="تغير المؤشرات عبر الأرباع السنوية", height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # الانتظار 10 ثوانٍ قبل الانتقال للربع التالي
            time.sleep(10)
            if i == len(df)-1: # للبدء من جديد بعد الوصول لآخر ربع
                st.rerun()
