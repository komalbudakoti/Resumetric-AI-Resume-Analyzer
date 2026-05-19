import streamlit as st

# ---------------- DASHBOARD ----------------

def show_dashboard():

    st.markdown("""
    <div class="eyebrow">
        The Future of Hiring
    </div>

    <div class="hero-title">
        Stop Guessing,
        Start Optimizing
    </div>

    <p class="lead-text">
        75% of resumes are rejected by ATS systems
        before a recruiter even sees them.
        Resumetric AI helps bridge the gap between
        your experience and recruiter expectations.
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="info-card">

        <div class="info-title">
        📊 ATS Scoring
        </div>

        <div class="info-text">
        Structural resume auditing including
        contact info, sections, formatting,
        and ATS readability.
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="info-card">

        <div class="info-title">
        🔍 Semantic Match
        </div>

        <div class="info-text">
        Vector embeddings calculate deep
        semantic alignment between your
        resume and the job description.
        </div>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("""
        <div class="info-card">

        <div class="info-title">
        ✍️ AI Rewriting
        </div>

        <div class="info-text">
        AI-generated improvements make
        your experience more impactful
        and recruiter-friendly.
        </div>

        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="info-card">

        <div class="info-title">
        🛡️ Privacy First
        </div>

        <div class="info-text">
        Sensitive personal information
        is sanitized locally before
        cloud AI analysis occurs.
        </div>

        </div>
        """, unsafe_allow_html=True)
        


# ---------------- RESULTS ----------------

def show_results(match_percentage, analysis):

    ats_score = analysis.get("ats_score", 0)
    ats_details = analysis.get("ats_details", [])

    matched_skills = analysis.get("matched_skills", [])
    missing_skills = analysis.get("missing_skills", [])

    sentence_improvements = analysis.get(
        "sentence_improvements",
        []
    )

    structural_tips = analysis.get(
        "structural_tips",
        []
    )

    st.success("✅ Analysis Complete!")

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Job Match",
            f"{match_percentage}%"
        )

        st.progress(match_percentage / 100)

    with col2:

        st.metric(
            "📊 ATS Score",
            f"{ats_score}%"
        )

        st.progress(ats_score / 100)

    st.write("")
    st.write("")

    # ---------------- ATS DETAILS ----------------

    st.markdown("## 🛡️ ATS Insights")

    for detail in ats_details:

        st.info(detail)

    st.write("")
    st.write("")

    # ---------------- SKILLS ----------------

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("## ✅ Matched Skills")
                        
        matched_badges = "".join([
            f"""<span style="
                display: inline-block; 
                background-color: #eafaf1; 
                color: #27ae60; 
                padding: 6px 14px; 
                margin: 4px; 
                border-radius: 20px; 
                font-weight: 500; 
                font-size: 14px;
                border: 1px solid #27ae6033;
            ">{skill}</span>""" 
            for skill in matched_skills
        ])
        
        
        if matched_skills:
            st.markdown(f'<div style="line-height: 2.2;">{matched_badges}</div>', unsafe_allow_html=True)
        else:
            st.caption("No matched skills found.")

    with col4:
        st.markdown("## ❌ Missing Skills")
                        
        missing_badges = "".join([
            f"""<span style="
                display: inline-block; 
                background-color: #fdf2f2; 
                color: #de350b; 
                padding: 6px 14px; 
                margin: 4px; 
                border-radius: 20px; 
                font-weight: 500; 
                font-size: 14px;
                border: 1px solid #de350b33;
            ">{skill}</span>""" 
            for skill in missing_skills
        ])
        
        if missing_skills:
            st.markdown(f'<div style="line-height: 2.2;">{missing_badges}</div>', unsafe_allow_html=True)
        else:
            st.caption("No missing skills identified.")

    st.write("")
    st.write("")

    # ---------------- SENTENCE IMPROVEMENTS ----------------

    st.markdown("## ✍️ Sentence Improvements")

    st.markdown("""
    AI suggested rewrites to make your
    experience sound more impactful.
    """)

    for item in sentence_improvements:
        
        with st.container():
            col_orig, col_imp = st.columns(2)
            
            with col_orig:
                st.markdown("**Original Sentence**")
                
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f1f5f9; 
                        border-left: 5px solid #cbd5e1; 
                        padding: 15px; 
                        border-radius: 8px;
                        color: #334155;                                
                    ">
                        {item.get("original", "")}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                                        
            with col_imp:
                st.markdown("**AI Recommended Rewrite**")
                st.success(item.get("improved", ""))
        
    
        st.markdown("---")
    
    # ---------------- STRUCTURAL TIPS ----------------
    st.markdown("## 🛠️ Structural Advice")

    for tip in structural_tips:
        st.warning(tip)

    st.write("")
    st.write("")

    # ---------------- RESET ----------------
    if st.button("← Analyze Another Resume"):
        st.session_state.clear()
        st.session_state.page = "📊 Analyze Resume"
        st.session_state.navigation_radio = "📊 Analyze Resume"
        st.rerun()

# ---------------- ABOUT ----------------

def show_about():

    st.markdown("""
    <div class="eyebrow">
        Technical Overview
    </div>

    <div class="hero-title" style="
        font-size:56px;
    ">
        The Architecture
        of Resumetric
    </div>

    <p class="lead-text">
        A deep dive into semantic alignment,
        ATS optimization, privacy protection,
        and AI-powered resume analysis.
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.markdown("""
    <div class="info-card">

    <div class="info-title">
    🔍 Intelligence Engine
    </div>

    <div class="info-text">
    Sentence Transformers + Hybrid Similarity
    scoring enables semantic understanding
    beyond keyword matching.
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="info-card">

    <div class="info-title">
    🛡️ Privacy First Analysis
    </div>

    <div class="info-text">
    Personal information is sanitized locally
    before any cloud-based AI analysis begins.
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ---------------- SYSTEM STACK ----------------

    st.markdown("##  System Architecture")

    tech1, tech2, tech3, tech4 = st.columns(4)

    with tech1:
        st.info("🐍 Python / Flask")

    with tech2:
        st.info("⚡ Groq LPU")

    with tech3:
        st.info("🤖 Llama 3.3")

    with tech4:
        st.info("🧾 spaCy NLP")

    st.write("")
    st.write("")
     
    st.success("""
    Resumetric AI combines ATS optimization,
    semantic intelligence, and privacy-first AI
    processing into one intelligent resume analysis platform.
    """)