import streamlit as st
from resume_analyzer import process_uploaded_file
from components import (
    show_dashboard,
    show_about,
    show_results
)
from styles import load_css

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Resumetric AI",
    page_icon="📄",
    layout="wide"
)

load_css()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div class="brand-title">
        Resumetric AI
    </div>

    <div class="brand-subtitle">
        Smart Resume Optimization
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Analyze Resume",
            "⚙️ System Logic"
        ]
    )

# ---------------- DASHBOARD ----------------

if page == "🏠 Dashboard":

    show_dashboard()

# ---------------- ANALYZE RESUME ----------------

elif page == "📊 Analyze Resume":

    st.markdown("""
    <div class="eyebrow">
        Optimizer
    </div>

    <div class="hero-title" style="
        font-size:54px;
        margin-bottom:10px;
    ">
        Resumetric AI Analyzer
    </div>

    <p class="lead-text">
        Upload your professional documents to receive
        ATS scoring, semantic matching, and AI-powered
        optimization recommendations.
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF/DOCX)",
        type=["pdf", "docx"]
    )

    job_description = st.text_area(
        "Job Description",
        height=250,
        placeholder="Paste the job description here..."
    )

    st.write("")

    if st.button(
        "🚀 Start AI Analysis",
        use_container_width=True
    ):

        if uploaded_file is None:

            st.warning("Please upload a resume.")

        elif not job_description.strip():

            st.warning("Please enter a job description.")

        else:

            with st.spinner("AI is analyzing your resume..."):

                try:

                    match_percentage, analysis = process_uploaded_file(
                        uploaded_file,
                        job_description
                    )

                    show_results(
                        match_percentage,
                        analysis
                    )

                except Exception as e:

                    st.error(f"Error: {str(e)}")

# ---------------- ABOUT PAGE ----------------

elif page == "⚙️ System Logic":

    show_about()