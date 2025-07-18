import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Unused Data Clean AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar on load
)

# --- HEADER SECTION (BANNER) ---
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 25px; border-radius: 10px;'>
        <h1 style='text-align: center; color: white;'>🧠 Unused Data Clean AI</h1>
        <h4 style='text-align: center; color: #D1D5DB;'>Analyze, Score, and Clean Your Data with AI</h4>
    </div>
""", unsafe_allow_html=True)

# --- ICON MENU SECTION ---
st.markdown("""
<div style="text-align:center; margin-top: 30px; margin-bottom: 20px;">
    <span style="margin: 50px;">
        📤<br><strong>Upload File</strong>
    </span>
    <span style="margin: 50px;">
        📊<br><strong>Profile Metrics</strong>
    </span>
    <span style="margin: 50px;">
        🧠<br><strong>AI Decay Score</strong>
    </span>
    <span style="margin: 50px;">
        🪄<br><strong>Cleanup Suggestion</strong>
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- FILE UPLOAD SECTION ---
st.markdown("### 📤 Upload your dataset and get instant insights.")
uploaded_file = st.file_uploader("Upload CSV or Excel File (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # --- DATA PROFILING METRICS ---
        total_cells = df.size
        total_rows = len(df)
        null_percentage = df.isnull().sum().sum() * 100 / total_cells
        duplicate_percentage = df.duplicated().sum() * 100 / total_rows
        outdated_percentage = 12.0  # Placeholder
        inconsistency_percentage = 15.0  # Placeholder
        decay_score = 100.0 - (null_percentage + duplicate_percentage + outdated_percentage + inconsistency_percentage) / 4

        # --- METRIC DISPLAY SECTION ---
        st.markdown("### 📊 Data Quality Metrics")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("🕳️ Null %", f"{null_percentage:.2f} %", disabled=True)
            st.text_input("📆 Outdated %", f"{outdated_percentage:.2f} %", disabled=True)

        with col2:
            st.text_input("🔁 Duplicate %", f"{duplicate_percentage:.2f} %", disabled=True)
            st.text_input("🧩 Inconsistency %", f"{inconsistency_percentage:.2f} %", disabled=True)

        st.text_input("🔥 Decay Score", f"{decay_score:.2f} %", disabled=True)

        # --- DOWNLOAD CLEANED DATA ---
        cleaned_df = df.drop_duplicates().dropna()
        csv = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("Upload a .csv or .xlsx file to begin.")

st.markdown("---")

# --- FOOTER ---
st.markdown("""
<p style='text-align: center; color: gray;'>
    © 2025 Unused Data Clean AI | Designed by Rupesh Kumar
</p>
""", unsafe_allow_html=True)
