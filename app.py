import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE SETTINGS
# ======================
st.set_page_config(page_title="Excel Dashboard", layout="wide")

st.title("📊 Interactive Excel Dashboard")

# ======================
# FILE UPLOAD
# ======================
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    # Read Excel
    df = pd.read_excel(uploaded_file)

    st.success("File Uploaded Successfully ✅")

    # ======================
    # DATA PREVIEW
    # ======================
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    # ======================
    # KPI SECTION
    # ======================
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        st.subheader("📌 KPIs")

        cols = st.columns(len(numeric_cols))

        for i, col in enumerate(numeric_cols):
            cols[i].metric(
                label=col,
                value=round(df[col].sum(), 2)
            )

    # ======================
    # FILTERS
    # ======================
    st.sidebar.header("Filters")

    category_cols = df.select_dtypes(include="object").columns

    selected_col = None

    if len(category_cols) > 0:
        selected_col = st.sidebar.selectbox(
            "Select Category",
            category_cols
        )

        selected_value = st.sidebar.multiselect(
            "Choose Values",
            df[selected_col].dropna().unique()
        )

        if selected_value:
            df = df[df[selected_col].isin(selected_value)]

    # ======================
    # CHART SECTION
    # ======================
    st.subheader("📈 Charts")

    if len(numeric_cols) > 0:

        chart_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig = px.bar(df, x=df.index, y=chart_col)

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Upload an Excel file to start")
