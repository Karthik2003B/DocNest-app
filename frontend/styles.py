def apply_custom_styles():
    return """
    <style>

    /* ---------- GLOBAL LAYOUT ---------- */
    .block-container {
        max-width: 1180px;
        padding-top: 3rem !important;
        padding-bottom: 2rem;
    }

    .main .block-container {
        background: transparent !important;
    }


    /* ---------- SIDEBAR (GLASS STYLE) ---------- */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.35) !important;   /* transparent */
        backdrop-filter: blur(12px);                     /* glass effect */
        border-right: 1px solid rgba(255,255,255,0.15);
        color: white !important;
    }

    /* Buttons inside sidebar */
    section[data-testid="stSidebar"] button {
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        text-align: left !important;
        padding: 10px !important;
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }

    /* Hover effect */
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.15) !important;
    }

    /* Active / Clicked */
    section[data-testid="stSidebar"] button:focus {
        background: rgba(255,255,255,0.25) !important;
    }
    

    /* ---------- HERO ---------- */
    .hero-box {
        margin-top: 40px !important;
        background: rgba(255, 255, 255, 0.35);
        border: 1px solid rgba(255,255,255,0.34);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
        color: #102a43;
        backdrop-filter: blur(6px);
    }

    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        color: #0f2740;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #35516b;
    }

    /* ---------- AUTH ---------- */
    .auth-brand {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }

    .auth-title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.3rem;
    }

    .auth-subtitle {
        color: #111827 !important;   /* same as input text */
        font-size: 1rem;
        margin-bottom: 1.2rem;
        font-weight: 500;
    }

    .switch-text {
        color: white;   /* match as well */
        font-size: 0.95rem;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
        text-align: center;
        font-weight: 500;
    }

    /* ---------- CARDS ---------- */
    .auth-box,
    .metric-card,
    .doc-card {
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(255,255,255,0.45);
        border-radius: 20px;
        backdrop-filter: blur(6px);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
    }

    .auth-box {
        padding: 1.2rem;
        min-height: 100%;
    }

    .metric-card {
        padding: 1.2rem 1rem;
        min-height: 130px;
    }

    .doc-card {
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
    }

    /* ---------- TEXT ---------- */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #102a43;
        margin-top: 0.6rem;
        margin-bottom: 0.8rem;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.35rem;
    }

    .metric-note {
        font-size: 0.88rem;
        color: #64748b;
    }

    .doc-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.45rem;
    }

    .doc-chip {
        display: inline-block;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        background: rgba(223,246,246,0.92);
        color: #1d5560;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    .doc-meta,
    .small-muted {
        color: #4b5563;
        font-size: 0.92rem;
    }

    /* ---------- BUTTONS ---------- */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stLinkButton"] > a {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        padding: 0.7rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, rgba(84,181,185,0.92), rgba(78,150,173,0.92)) !important;
        color: white !important;
        box-shadow: 0 12px 24px rgba(84, 181, 185, 0.16) !important;
    }

    /* ---------- INPUTS ---------- */
    div[data-testid="stTextInput"] > div,
    div[data-testid="stTextArea"] > div,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stDateInput"] > div,
    div[data-testid="stFileUploader"] > div {
        background: rgba(255,255,255,0.82) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.45) !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stDateInput"] input {
        background: transparent !important;
        color: #111827 !important;
        border: none !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: transparent !important;
        color: #111827 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #6b7280 !important;
    }

    div[role="listbox"] {
        background: white !important;
        color: #111827 !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
    }

    </style>
    """
    