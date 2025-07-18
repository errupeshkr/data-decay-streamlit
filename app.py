import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Hide sidebar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- CSS Styling ---
st.markdown("""
<style>
/* Hide sidebar toggle */
[data-testid="stSidebar"] { display: none; }

/* Highlight blocks */
.metric-box {
    background-color: #F3F4F6;
    padding: 15px 25px;
    border-radius: 12px;
    margin-bottom: 15px;
    font-size: 18px;
    color: #111827;
    font-weight: 500;
}
.metric-title {
    font-size: 15px;
    color: #6B7280;
    margin-bottom: 5px;
}
h1, h2, h3 {
    color: #1F2937;
}
.stButton>button {
    background-color: #2563EB;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("## 👋 Welcome to Unused Data Clean AI")
st.write("Upload your CSV/Excel file to view data quality insights and download the cleaned version.")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your file", type=["csv", "xlsx"])

# --- Processing ---
if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # --- Data Profiling ---
    total_rows, total_columns = df.shape
    total_cells = total_rows * total_columns

    null_percentage = (df.isnull().sum().sum() / total_cells) * 100

    duplicate_percentage = (df.duplicated().sum() / total_rows) * 100

    outdated_percentage = 0
    for col in df.columns:
        if "date" in col.lower():
            try:
                dates = pd.to_datetime(df[col], errors='coerce')
                outdated_percentage = ((dates < "2023-01-01").sum() / total_rows) * 100
                break
            except:
                pass

    inconsistency_percentage = 0
    for col in df.columns:
        if df[col].dtype == object:
            inconsistency_percentage += (df[col].str.strip().value_counts().sum() - df[col].value_counts().sum())
    inconsistency_percentage = (inconsistency_percentage / total_rows) * 100

    decay_score = 100 - (null_percentage + duplicate_percentage + outdated_percentage + inconsistency_percentage)/4

    # --- Display Highlighted Metrics ---
    st.markdown("### 📊 <span style='color:#111827'>Data Quality Metrics</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-title'>🕳️ Null %</div>
            {null_percentage:.2f} %
        </div>
        <div class='metric-box'>
            <div class='metric-title'>📆 Outdated %</div>
            {outdated_percentage:.2f} %
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-title'>🌀 Duplicate %</div>
            {duplicate_percentage:.2f} %
        </div>
        <div class='metric-box'>
            <div class='metric-title'>🧩 Inconsistency %</div>
            {inconsistency_percentage:.2f} %
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-title'>🔥 Decay Score</div>
        {decay_score:.2f} %
    </div>
    """, unsafe_allow_html=True)

    # --- Download cleaned CSV ---
    cleaned_df = df.drop_duplicates()
    csv_buffer = BytesIO()
    cleaned_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_buffer.getvalue(),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
