# =========================
# FILE: styles.py
# =========================

import streamlit as st


def load_css():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background:#f8fafc;
        color:#0f172a;
    }

    [data-testid="stHeader"] {
        display:none;
    }

    section[data-testid="stSidebar"] {
        background:white;
        border-right:1px solid #e2e8f0;
    }

    .brand-title {
        font-size:32px;
        font-weight:800;
        color:#0f172a;
        margin-top:20px;
    }

    .brand-subtitle {
        color:#64748b;
        margin-bottom:30px;
    }

    .block-container {
        padding-top:3rem;
        padding-left:4rem;
        padding-right:4rem;
        max-width:1400px;
    }

    .eyebrow {
        color:#2563eb;
        text-transform:uppercase;
        letter-spacing:2px;
        font-size:13px;
        font-weight:700;
        margin-bottom:20px;
    }

    .hero-title {
        font-size:72px;
        font-weight:800;
        line-height:1.05;
        letter-spacing:-3px;
        margin-bottom:24px;
        color:#0f172a;
        max-width:950px;
    }

    .lead-text {
        color:#475569;
        font-size:20px;
        line-height:1.9;
        max-width:900px;
    }

    .info-card {
        background:white;
        border:1px solid #e2e8f0;
        border-radius:28px;
        padding:34px;
        box-shadow:
        0 4px 20px rgba(15,23,42,0.04);
    }

    .info-title {
        font-size:24px;
        font-weight:700;
        margin-bottom:18px;
        color:#0f172a;
    }

    .info-text {
        color:#64748b;
        font-size:16px;
        line-height:1.8;
    }

    .stButton > button {
        background:linear-gradient(
            135deg,
            #2563eb,
            #3b82f6
        );

        color:white;
        border:none;
        border-radius:16px;
        padding:16px 28px;
        font-weight:700;
    }

    .stTextArea textarea {

        border-radius:16px !important;

        border:1px solid #cbd5e1 !important;
    }

    @media (max-width:768px) {

        .hero-title {
            font-size:44px;
        }

        .block-container {
            padding-left:1rem;
            padding-right:1rem;
        }
    }

    </style>
    """, unsafe_allow_html=True)