import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Data Decay Analyzer", layout="wide")
st.title("📊 Data Decay Score Analyzer")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

def calculate_null_percentage(df):
    return (df.isnull().sum().sum() / df.size) * 100

def calculate_duplicate_percentage(df):
    return (df.duplicated().sum() / len(df)) * 100 if len(df) > 0 else 0

def calculate_outdated_percentage(df):
    outdated_count = 0
    current_year = datetime.now().year
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            outdated_count += df[col].apply(lambda x: x.year < current_year - 2 if pd.notnull(x) else False).sum()
    total_rows = df.shape[0]
    return (outdated_count / total_rows) * 100 if total_rows > 0 else 0

def calculate_inconsistency_percentage(df):
    inconsistent_cells = 0
    total_cells = df.size
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].nunique() > 20:
            inconsistent_cells += df[col].nunique()
    return (inconsistent_cells / total_cells) * 100 if total_cells > 0 else 0

def calculate_decay_score(null_perc, dup_perc, out_perc, inc_perc):
    return max(0, 100 - (0.25 * null_perc + 0.25 * dup_perc + 0.25 * out_perc + 0.25 * inc_perc))

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format!")
            st.stop()

        st.success("✅ File uploaded successfully!")

        null_perc = round(calculate_null_percentage(df), 2)
        dup_perc = round(calculate_duplicate_percentage(df), 2)
        out_perc = round(calculate_outdated_percentage(df), 2)
        inc_perc = round(calculate_inconsistency_percentage(df), 2)
        decay_score = round(calculate_decay_score(null_perc, dup_perc, out_perc, inc_perc), 2)

        st.subheader("📈 Data Quality Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Null %", f"{null_perc}%")
        col2.metric("Duplicate %", f"{dup_perc}%")
        col3.metric("Outdated %", f"{out_perc}%")

        col4, col5 = st.columns(2)
        col4.metric("Inconsistency %", f"{inc_perc}%")
        col5.metric("Decay Score", f"{decay_score}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
