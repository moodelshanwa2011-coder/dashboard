import streamlit as st
import pandas as pd

st.title("📂 Upload Excel File")

# زر رفع الملف
uploaded_file = st.file_uploader(
    "اختار ملف Excel",
    type=["xlsx"]
)

# بعد الرفع
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.success("تم رفع الملف ✅")

    # عرض البيانات
    st.dataframe(df)
