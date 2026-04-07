import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# إعدادات الصفحة
st.set_page_config(page_title="ICU Riyadh Master Dashboard", layout="wide")

# 1. تجهيز البيانات والمقارنات (Benchmarks) بناءً على مستند المستشفى 
# تم استخراج المتوسطات (Benchmarks) من عمود NDNQI mean في جدولك
data_map = {
    "Total Falls": {"value": 0.25, "benchmark": 0.18, "unit": "per 1000 days"},
    "HAPI %": {"value": 3.33, "benchmark": 4.97, "unit": "%"},
    "CLABSI": {"value": 3.87, "benchmark": 1.09, "unit": "per 1000 days"},
    "Nurse Turnover": {"value": 3.69, "benchmark": 5.74, "unit": "%"}
}

def create_kpi_card(title, current_val, benchmark_val, unit):
    # تحديد اللون: أزرق إذا كان أقل من أو يساوي المرجع، أحمر إذا تخطاه
    # ملاحظة: في التمريض، زيادة السقوط والعدوى سيئة (أحمر)، لكن زيادة التعليم جيدة.
    # هنا سنعتمد القاعدة العامة: "تخطي المرجع في الإصابات = أحمر"
    is_over_limit = current_val > benchmark_val
    color = "#FF4B4B" if is_over_limit else "#007BFF" # أحمر أو أزرق
    
    fig = go.Figure()
    
    # إضافة الرقم المتحرك (Indicator)
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = current_val,
        number = {'suffix': f" {unit}", 'font': {'color': color, 'size': 50}},
        delta = {'reference': benchmark_val, 'relative': False, 'position': "bottom"},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)", # خلفية شفافة
    )
    return fig

# --- واجهة العرض ---
st.title("🏥 ICU Riyadh - Live Performance Monitor")
st.subheader("متابعة مؤشرات الأداء مقارنة بالمعايير العالمية (NDNQI) ")

placeholder = st.empty()

# حلقة التحديث التلقائي (كل 10 دقائق أو للمحاكاة)
while True:
    with placeholder.container():
        # تقسيم الشاشة لـ 4 أعمدة للمؤشرات الدائرية/الرقمية
        cols = st.columns(4)
        
        # عرض الكروت بناءً على بيانات الجدول 
        for i, (name, stats) in enumerate(data_map.items()):
            with cols[i]:
                # محاكاة تغيير بسيط في الأرقام لجعلها "متحركة" عند كل تحديث
                display_val = stats["value"] 
                fig = create_kpi_card(name, display_val, stats["benchmark"], stats["unit"])
                st.plotly_chart(fig, use_container_width=True)
        
        # بار تشارت يعكس التغير الحالي
        st.divider()
        st.markdown("### 📊 تحليل مقارنة الأداء الحالي بالـ Benchmark")
        
        chart_data = pd.DataFrame({
            "Metric": list(data_map.keys()),
            "Current": [d["value"] for d in data_map.values()],
            "Benchmark": [d["benchmark"] for d in data_map.values()]
        })
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Current Value', x=chart_data['Metric'], y=chart_data['Current'], marker_color='#007BFF'))
        fig_bar.add_trace(go.Bar(name='Benchmark', x=chart_data['Metric'], y=chart_data['Benchmark'], marker_color='#D3D3D3'))
        
        fig_bar.update_layout(barmode='group', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

        # التحديث كل 10 دقائق
        time.sleep(600)
        st.rerun()
    
