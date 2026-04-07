import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Interactive Excel Dashboard",
    layout="wide"
)

# ---------------- DARK STYLE ----------------
st.markdown("""
<style>
body {
    background-color:#0E1117;
    color:white;
}
.block-container {
    padding-top:2rem;
}
.metric-card {
    background-color:#1c1f26;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 0 10px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 Interactive Excel Dashboard")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    # ---------- READ FILE ----------
    df = pd.read_excel(uploaded_file)

    # ---------- FIX NUMBERS ----------
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('%', '')
        df[col] = pd.to_numeric(df[col], errors='ignore')

    st.success("File Uploaded Successfully ✅")

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("Filters")

    category_col = st.sidebar.selectbox(
        "Select Category Column",
        df.columns
    )

    selected_values = st.sidebar.multiselect(
        "Choose Values",
        df[category_col].dropna().unique()
    )

    if selected_values:
        df = df[df[category_col].isin(selected_values)]

    # ---------------- DATA PREVIEW ----------------
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    # ---------------- KPI CARDS ----------------
    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:

        st.subheader("Key Metrics")

        cols = st.columns(len(numeric_df.columns))

        for i, col in enumerate(numeric_df.columns):
            value = round(numeric_df[col].mean(), 2)

            cols[i].markdown(f"""
            <div class="metric-card">
                <h3>{col}</h3>
                <h1>{value}</h1>
            </div>
            """, unsafe_allow_html=True)

        # ---------------- CHARTS ----------------
        st.subheader("Interactive Charts")

        chart_col = st.selectbox(
            "Select Column for Chart",
            numeric_df.columns
        )

        if category_col in df.columns:

            fig = px.bar(
                df,
                x=category_col,
                y=chart_col,
                color=category_col,
                title=f"{chart_col} by {category_col}"
            )

            fig.update_layout(
                template="plotly_dark",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬆ Upload an Excel file to start.")
