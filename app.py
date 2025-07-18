import streamlit as st
import pandas as pd
from io import StringIO

# --- Page Configuration ---
st.set_page_config(
    page_title="Unused Data Clean AI",
    layout="centered",
    page_icon="📊"
)

# --- Welcome Header ---
st.markdown("<h1 style='text-align: center;'>📊 Unused Data Clean AI</h1>", unsafe_allow_html=True)
st.markdown("#### 📤 Upload your CSV or Excel file")

# --- File Upload ---
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

# --- Process and Display ---
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # --- Calculate Data Quality Metrics ---
        total_cells = df.size
        total_rows = len(df)
        null_percentage = df.isnull().sum().sum() * 100 / total_cells
        duplicate_percentage = df.duplicated().sum() * 100 / total_rows
        outdated_percentage = 10.0  # Dummy
        inconsistency_percentage = 15.0  # Dummy
        decay_score = 100.0 - (null_percentage + duplicate_percentage + outdated_percentage + inconsistency_percentage)/4

        # --- Display Metrics ---
        st.markdown("### 📊 Data Quality Metrics")
        col1, col2 = st.columns(2)
        col1.metric("🕳️ Null %", f"{null_percentage:.2f} %")
        col2.metric("🔁 Duplicate %", f"{duplicate_percentage:.2f} %")
        col1.metric("📆 Outdated %", f"{outdated_percentage:.2f} %")
        col2.metric("🧩 Inconsistency %", f"{inconsistency_percentage:.2f} %")
        st.metric("🔥 Decay Score", f"{decay_score:.2f} %")

        # --- Download Cleaned Data (Dummy for now) ---
        cleaned_csv = df.drop_duplicates().dropna()
        csv = cleaned_csv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("Please upload a file to get started.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ for Data Quality Insights</p>", unsafe_allow_html=True)
