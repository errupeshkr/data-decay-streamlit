import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Unused Data Clean AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    header, footer {visibility: hidden;}
    .highlight-box {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .red { background-color: #ffe6e6; }
    .green { background-color: #e6ffe6; }
    .yellow { background-color: #fff9e6; }
    </style>
""", unsafe_allow_html=True)

# ---------- PAGE TITLE ----------
st.markdown("## 📊 Data Decay Score Analyzer")
st.markdown("""
<div class='highlight-box' style='background-color: #173A5E; color: white;'>
<h3>🧠 Unused Data Clean AI</h3>
<p>Analyze, Score, and Clean Your Data with AI</p>
</div>
""", unsafe_allow_html=True)

# ---------- ICON MENU ----------
col1, col2, col3, col4 = st.columns(4)
col1.markdown("📁 **Upload File**")
col2.markdown("📊 **Profile Metrics**")
col3.markdown("🧠 **AI Decay Score**")
col4.markdown("🧹 **Cleanup Suggestion**")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel File (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    if file_ext == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.markdown("### 📄 Uploaded Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ---------- METRIC CALCULATIONS ----------
    row_count, col_count = df.shape
    total_cells = row_count * col_count

    null_count = df.isnull().sum().sum()
    duplicate_count = df.duplicated().sum()

    # Outdated: values more than 2 years old
    outdated_count = 0
    for col in df.select_dtypes(include=["datetime", "object"]).columns:
        try:
            parsed_dates = pd.to_datetime(df[col], errors='coerce')
            outdated_count += parsed_dates[parsed_dates < datetime.datetime.now() - pd.DateOffset(years=2)].count()
        except:
            continue

    # Inconsistency: inconsistent casing
    inconsistent_case_count = 0
    for col in df.select_dtypes(include='object'):
        unique_vals = df[col].dropna().unique()
        if any(x != x.title() for x in unique_vals):
            inconsistent_case_count += 1

    # Percentages
    null_percent = round((null_count / total_cells) * 100, 2)
    duplicate_percent = round((duplicate_count / row_count) * 100, 2)
    outdated_percent = round((outdated_count / row_count) * 100, 2)
    decay_score = round((null_percent + duplicate_percent + outdated_percent + inconsistent_case_count * 5) / 4, 2)

    # ---------- METRICS BOX ----------
    st.markdown("### 📊 Profile Metrics and Scores")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Null %", f"{null_percent} %")
        st.text_input("Duplicate %", f"{duplicate_percent} %")
        st.text_input("Outdated %", f"{outdated_percent} %")
        st.text_input("Inconsistency Columns", str(inconsistent_case_count))

    with col2:
        st.markdown(f"""
        <div class='highlight-box {"red" if decay_score > 70 else "yellow" if decay_score > 40 else "green"}'>
            <h4>🤖 AI Decay Score: {decay_score} %</h4>
            {"⚠️ <b>Low Quality Data!</b>" if decay_score > 70 else "✅ <b>Good Quality Data</b>"}
        </div>
        """, unsafe_allow_html=True)

    # ---------- CLEANUP SUGGESTIONS ----------
    st.markdown("### 🧹 Suggested Cleanup Actions")
    cleanup_notes = []

    if null_percent > 50:
        cleanup_notes.append("🔴 Null % > 50 → Suggest **Drop Columns**")
    elif null_percent < 20:
        cleanup_notes.append("🟡 Null % < 20 → Suggest **Fill Missing Values** (mean/mode)")

    if duplicate_percent > 0:
        cleanup_notes.append("🟠 Duplicate % > 0 → Suggest **Remove Duplicates**")

    if inconsistent_case_count > 0:
        cleanup_notes.append("🟣 Inconsistent Case → Suggest **Standardize to Title Case**")

    if outdated_percent > 30:
        cleanup_notes.append("🔵 Outdated > 30% → Suggest **Flag for Archival**")

    if decay_score > 70:
        cleanup_notes.append("⚠️ Decay Score > 70 → Suggest **Immediate Review**")

    for note in cleanup_notes:
        st.markdown(f"- {note}")

else:
    st.warning("📤 Please upload a file to get started.")
