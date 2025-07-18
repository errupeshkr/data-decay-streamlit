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

# Set page config
st.set_page_config(
    page_title="Unused Data Clean AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------
# 🎉 Welcome Section (Main Page)
# ---------------------------------
st.markdown("<h1 style='text-align: center; color: green;'>🧠 Welcome to Unused Data Clean AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Analyze, Clean and Download Your Data Easily</h4>", unsafe_allow_html=True)

st.divider()

# Upload File Section
st.subheader("📤 Upload Your CSV/Excel File")
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.write("File name:", uploaded_file.name)

# ---------------------------------
# 📌 Sidebar Navigation Menu
# ---------------------------------
st.sidebar.markdown("## 📂 All Menu Details")

st.sidebar.markdown("🔎 **Analyze Data Quality**")
st.sidebar.markdown("📊 **Dashboard**")
st.sidebar.markdown("🗂️ **File History** &nbsp; <span style='color: white; background-color: blue; border-radius: 10px; padding: 2px 6px;'>40</span>", unsafe_allow_html=True)
st.sidebar.markdown("👁️ **View Decay Scores** &nbsp; <span style='color: white; background-color: red; border-radius: 10px; padding: 2px 6px;'>40</span>", unsafe_allow_html=True)
st.sidebar.markdown("🧹 **Cleanup Panel**")
st.sidebar.markdown("📄 **Reports**")
st.sidebar.markdown("🧽 **Cleanup Panel**")
st.sidebar.markdown("📥 **Report Download**")

# ---------------------------------
# 💡 Footer or Next Steps
# ---------------------------------
st.divider()
st.markdown("### 📌 What's Next?")
st.markdown("""
- ✅ Get auto metrics like **Null %**, **Duplicate %**, **Outdated %**, **Inconsistency %**, and **Decay Score**
- 📉 Visualize results on Dashboard
- 🧹 Clean the data using Cleanup Panel
- 📥 Download the final cleaned report
""")

