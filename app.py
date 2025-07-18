import streamlit as st
import pandas as pd
import base64
import io

# Hide Streamlit sidebar and top menu
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# App Title and Banner
st.markdown("""
    <h1 style="font-family: Arial; color: #1f2937;">
        📊 Data Decay Score Analyzer
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background-color:#1E3A8A; padding: 20px; border-radius: 10px;">
        <h2 style="color:white; font-family: Arial;">
            🧠 Unused Data Clean AI
        </h2>
        <p style="color:white;">Analyze, Score, and Clean Your Data with AI</p>
    </div>
""", unsafe_allow_html=True)

# --- Navigation Icons with Labels ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("📁 **Upload File**")
with col2:
    st.markdown("📊 **Profile Metrics**")
with col3:
    st.markdown("🧠 **AI Decay Score**")
with col4:
    st.markdown("🪛 **Cleanup Suggestion**")

st.markdown("---")
st.markdown("<center>Upload your dataset and get instant insights.</center>", unsafe_allow_html=True)

# --- File Upload and Analysis Panel ---
col5, col6 = st.columns([1, 1])

with col5:
    uploaded_file = st.file_uploader("📂 Upload CSV or Excel File (.csv / .xlsx)", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # Display uploaded data
        st.dataframe(df.head())

        # Save download link
        def get_table_download_link(df):
            output = io.BytesIO()
            df.to_csv(output, index=False)
            b64 = base64.b64encode(output.getvalue()).decode()
            return f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">📥 Download Cleaned CSV</a>'

with col6:
    if uploaded_file:
        total_cells = df.shape[0] * df.shape[1]
        null_percent = (df.isnull().sum().sum() / total_cells) * 100
        duplicate_percent = (df.duplicated().sum() / len(df)) * 100
        outdated_percent = 15.0  # Placeholder
        inconsistency_percent = 10.0  # Placeholder
        decay_score = round((null_percent + duplicate_percent + outdated_percent + inconsistency_percent) / 4, 2)

        # Highlighted Metrics
        st.markdown(f"<div style='background:#fff3cd;padding:10px;border-radius:10px;'>🟡 <b>Null %</b>: {null_percent:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#fdecea;padding:10px;border-radius:10px;'>🔴 <b>Duplicate %</b>: {duplicate_percent:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#ffe9ec;padding:10px;border-radius:10px;'>🔴 <b>Outdated %</b>: {outdated_percent:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#fff4f4;padding:10px;border-radius:10px;'>🔴 <b>Inconsistency %</b>: {inconsistency_percent:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#e0f7fa;padding:10px;border-radius:10px;'>🧠 <b>Decay Score</b>: {decay_score}</div>", unsafe_allow_html=True)

        # Download link
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
