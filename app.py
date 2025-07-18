import streamlit as st
import pandas as pd

# --- Set page config ---
st.set_page_config(
    page_title="Unused Data Clean AI",
    layout="wide",
    page_icon="🧠"
)

# --- Custom Banner Header ---
st.markdown("""
    <div style='background-color: #1E3A8A; padding: 20px; border-radius: 10px;'>
        <h1 style='text-align: center; color: white;'>🧠 Unused Data Clean AI</h1>
        <h4 style='text-align: center; color: #D1D5DB;'>Analyze, Score, and Clean Your Data with AI</h4>
    </div>
""", unsafe_allow_html=True)

# --- Icon Row with Labels ---
st.markdown("""
<div style="text-align:center; margin-top: 30px; margin-bottom: 10px;">
    <span style="margin: 40px;">
        📁<br><strong>Upload File</strong>
    </span>
    <span style="margin: 40px;">
        📊<br><strong>Profile Metrics</strong>
    </span>
    <span style="margin: 40px;">
        🧠<br><strong>AI Decay Score</strong>
    </span>
    <span style="margin: 40px;">
        🪄<br><strong><a href='#' style='text-decoration:none;'>Cleanup Suggestion</a></strong>
    </span>
</div>
""", unsafe_allow_html=True)

# --- Horizontal Line ---
st.markdown("---")

# --- Upload Section ---
st.markdown("### 📤 Upload your dataset and get instant insights.")
uploaded_file = st.file_uploader("Upload CSV or Excel File (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # --- Calculate Metrics ---
        total_cells = df.size
        total_rows = len(df)
        null_percentage = df.isnull().sum().sum() * 100 / total_cells
        duplicate_percentage = df.duplicated().sum() * 100 / total_rows
        outdated_percentage = 12.0  # placeholder
        inconsistency_percentage = 15.0  # placeholder
        decay_score = 100.0 - (null_percentage + duplicate_percentage + outdated_percentage + inconsistency_percentage)/4

        # --- Show Metrics in Two Columns ---
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("🕳️ Null %", f"{null_percentage:.2f} %", disabled=True)
            st.text_input("📆 Outdated %", f"{outdated_percentage:.2f} %", disabled=True)

        with col2:
            st.text_input("🔁 Duplicate %", f"{duplicate_percentage:.2f} %", disabled=True)
            st.text_input("🧩 Inconsistency %", f"{inconsistency_percentage:.2f} %", disabled=True)

        st.text_input("🔥 Decay Score", f"{decay_score:.2f} %", disabled=True)

        # --- Cleaned CSV Download ---
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

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center;'>Data Quality Insights -Joget DX 8 | Team: Unused Data Clean AI</p>", unsafe_allow_html=True)






import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Unused Data Clean AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hides sidebar on load
)

# --- HEADER ---
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🧠 Unused Data Clean AI</h1>
    <h3 style='text-align: center;'>A Smart Platform to Analyze and Clean Your Unused Data</h3>
    <hr>
""", unsafe_allow_html=True)

# --- BUTTON TO OPEN APP ---
st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <a href='https://huggingface.co/spaces/rupeshchy22102000/data-decay-analyzer' target='_blank'>
            <button style='background-color: #4CAF50; color: white; padding: 14px 28px;
                            border: none; border-radius: 10px; font-size: 18px; cursor: pointer;'>
                🚀 Open Decay Analyzer App
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# --- MENU (SIMULATED) ---
st.markdown("""
    <br><br>
    <h4>📂 All Menu Details</h4>
    <ul style='font-size: 18px; line-height: 1.8;'>
        <li>📊 Analyze Data Quality</li>
        <li>📈 Dashboard</li>
        <li>🗂️ File History</li>
        <li>👁️ View Decay Scores</li>
        <li>🧹 Cleanup Panel</li>
        <li>📋 Reports</li>
        <li>📥 Report Download</li>
    </ul>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>© 2025 Unused Data Clean AI by Rupesh Kumar</p>
""", unsafe_allow_html=True)

