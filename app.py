import streamlit as st
import pandas as pd

st.title("📊 Excel Dashboard")

# رفع ملف الاكسل
uploaded_file = st.file_uploader("ارفع ملف Excel", type=["xlsx"])

if uploaded_file is not None:

    # قراءة الملف
    df = pd.read_excel(uploaded_file)

    st.subheader("📄 البيانات")
    st.dataframe(df)

    # اختيار الأعمدة الرقمية فقط
    numeric_cols = df.select_dtypes(include="number")

    if not numeric_cols.empty:

        st.subheader("📈 تحليل البيانات")

        # رسم charts لكل عمود رقمي
        for col in numeric_cols.columns:
            st.write(f"Chart for {col}")
            st.bar_chart(df[col])

    else:
        st.warning("لا يوجد أعمدة رقمية للرسم")
