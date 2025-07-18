import streamlit as st
import pandas as pd
import io

# Hide the Streamlit default sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Custom CSS for highlighting
highlight_style = """
    <style>
        .metric-container {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            background-color: #f3f5f9;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
        }
        .metric-label {
            font-size: 1rem;
            color: #666;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2a2a2a;
        }
    </style>
"""
st.markdown(highlight_style, unsafe_allow_html=True)

# --- Header ---
st.markdown("## 📊 Data Quality Metrics")
st.write("---")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1]
    
    # Load file
    if file_ext == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_ext == 'xlsx':
        df = pd.read_excel(uploaded_file)

    total_cells = df.size
    total_rows = len(df)
    
    # Calculate Metrics
    null_percent = round(df.isnull().sum().sum() / total_cells * 100, 2)
    duplicate_percent = round(df.duplicated().sum() / total_rows * 100, 2)
    outdated_percent = 12.0  # Placeholder (replace with your logic)
    inconsistency_percent = 15.0  # Placeholder (replace with your logic)

    decay_score = round(100 - ((null_percent + duplicate_percent + outdated_percent + inconsistency_percent) * 0.25), 2)

    # --- Display Metrics with Highlights ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>🦠 Null %</div>
                <div class='metric-value'>{null_percent} %</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>📅 Outdated %</div>
                <div class='metric-value'>{outdated_percent} %</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>🧬 Duplicate %</div>
                <div class='metric-value'>{duplicate_percent} %</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>🧩 Inconsistency %</div>
                <div class='metric-value'>{inconsistency_percent} %</div>
            </div>
        """, unsafe_allow_html=True)

    # Decay Score Full Width
    st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-label'>🔥 Decay Score</div>
            <div class='metric-value'>{decay_score} %</div>
        </div>
    """, unsafe_allow_html=True)

    # --- Download Cleaned File ---
    cleaned_csv = df.drop_duplicates().dropna()
    buffer = io.StringIO()
    cleaned_csv.to_csv(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        label="📥 Download Cleaned CSV",
        data=buffer,
        file_name="cleaned_data.csv",
        mime="text/csv",
    )
else:
    st.info("Please upload a CSV or Excel file to begin analysis.")
