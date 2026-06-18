
import streamlit as st

KAASHIFY_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --kaashify-navy: #102033;
        --kaashify-blue: #1D4ED8;
        --kaashify-blue-soft: #EFF6FF;
        --kaashify-cyan: #0891B2;
        --kaashify-text: #172033;
        --kaashify-slate: #465569;
        --kaashify-muted: #66758A;
        --kaashify-border: #D8E1EC;
        --kaashify-soft: #F6F8FB;
        --kaashify-card: #FFFFFF;
        --kaashify-success: #047857;
        --kaashify-danger: #B42318;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        color: var(--kaashify-text) !important;
    }

    .stApp {
        background:
            linear-gradient(135deg, rgba(219, 234, 254, 0.58) 0%, rgba(255,255,255,0) 36%),
            linear-gradient(180deg, #F8FAFC 0%, #EEF3F8 100%);
    }

    section[data-testid="stSidebar"] {
        background: #102033;
        border-right: 1px solid rgba(255,255,255,0.10);
    }

    section[data-testid="stSidebar"] * { color: #E5E7EB !important; }
    section[data-testid="stSidebar"] a {
        border-radius: 8px !important;
        margin: 2px 8px !important;
    }
    section[data-testid="stSidebar"] a:hover,
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: rgba(255,255,255,0.12) !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }

    .kaashify-hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #102033 0%, #1E3A5F 62%, #1D4ED8 100%);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 14px;
        padding: 30px 34px;
        color: #FFFFFF;
        box-shadow: 0 18px 42px rgba(15, 23, 42, 0.18);
        margin-bottom: 24px;
    }
    .kaashify-hero:after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.10) 100%);
        pointer-events: none;
    }
    .kaashify-brand-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 7px 11px;
        border-radius: 8px;
        background: rgba(255,255,255,0.11);
        border: 1px solid rgba(255,255,255,0.18);
        color: #EAF2FF;
        font-weight: 700;
        letter-spacing: 0;
        font-size: 0.76rem;
        text-transform: uppercase;
        margin-bottom: 14px;
    }
    .kaashify-title {
        margin: 0;
        font-size: 2.75rem;
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: 0;
    }
    .kaashify-subtitle {
        margin: 12px 0 0 0;
        color: #DCEAFF;
        font-size: 1rem;
        max-width: 820px;
        line-height: 1.55;
    }
    .kaashify-hero,
    .kaashify-hero h1,
    .kaashify-hero p,
    .kaashify-hero span,
    .kaashify-hero div {
        color: #FFFFFF !important;
    }
    .kaashify-hero .kaashify-subtitle {
        color: #DCEAFF !important;
    }
    .kaashify-hero .kaashify-brand-pill {
        color: #EAF2FF !important;
    }

    h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    label, p {
        color: var(--kaashify-text) !important;
    }
    h2, h3 {
        letter-spacing: 0 !important;
    }
    code {
        color: #0F172A !important;
        background: #EAF1F8 !important;
        border-radius: 5px !important;
        padding: 2px 6px !important;
    }

    .page-title, .header-style {
        color: var(--kaashify-navy) !important;
        font-weight: 800 !important;
        letter-spacing: 0 !important;
        margin: 0 0 12px 0 !important;
        font-size: 2.35rem !important;
        line-height: 1.15 !important;
    }
    .page-kicker {
        color: var(--kaashify-blue) !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0;
        font-size: .78rem;
        margin-bottom: 8px;
    }
    .section-header {
        color: var(--kaashify-navy) !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        margin-top: 26px !important;
        margin-bottom: 16px !important;
        border-left: 4px solid var(--kaashify-blue) !important;
        padding-left: 14px !important;
    }

    div[data-testid="metric-container"], .status-box, .kpi-container {
        background: var(--kaashify-card) !important;
        border: 1px solid var(--kaashify-border) !important;
        border-radius: 10px !important;
        padding: 18px 20px !important;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07) !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--kaashify-blue) !important;
        font-weight: 800 !important;
        letter-spacing: 0 !important;
        font-size: 2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--kaashify-slate) !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
        font-size: 0.86rem !important;
    }

    div[data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stDataFrame"], .stAlert {
        border-radius: 10px !important;
    }
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid var(--kaashify-border);
        padding: 18px;
        box-shadow: 0 10px 24px rgba(15,23,42,.06);
    }

    div[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid var(--kaashify-border) !important;
        box-shadow: 0 6px 16px rgba(15,23,42,.04) !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--kaashify-border);
        margin-bottom: 18px;
    }
    button[data-baseweb="tab"] {
        color: var(--kaashify-slate) !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 12px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--kaashify-blue) !important;
        background: var(--kaashify-blue-soft) !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFormSubmitButton"] button {
        background: #FFFFFF !important;
        color: var(--kaashify-navy) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: 1px solid #C7D2E0 !important;
        box-shadow: 0 6px 14px rgba(15,23,42,0.08) !important;
        min-height: 2.55rem !important;
    }
    .stButton > button *,
    .stDownloadButton > button *,
    div[data-testid="stFormSubmitButton"] button * {
        color: inherit !important;
    }
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: #1D4ED8 !important;
        color: white !important;
        border: 0 !important;
    }
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: var(--kaashify-navy) !important;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        border-color: var(--kaashify-blue) !important;
        color: var(--kaashify-blue) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #1E40AF !important;
        color: #FFFFFF !important;
    }
    .stButton > button:disabled,
    .stButton > button:disabled:hover,
    .stDownloadButton > button:disabled,
    .stDownloadButton > button:disabled:hover,
    div[data-testid="stFormSubmitButton"] > button:disabled,
    div[data-testid="stFormSubmitButton"] > button:disabled:hover {
        background: #E8EEF5 !important;
        color: #7A8798 !important;
        border-color: #D5DFEA !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 1 !important;
    }

    input, textarea, select,
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {
        background: #FFFFFF !important;
        color: var(--kaashify-text) !important;
        border-color: #C7D2E0 !important;
        border-radius: 8px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #8A97A8 !important;
        opacity: 1 !important;
    }
    input:disabled,
    textarea:disabled,
    div[data-baseweb="input"][disabled],
    div[data-baseweb="base-input"][disabled],
    div[data-testid="stNumberInput"] input:disabled {
        background: #FFFFFF !important;
        color: #0B1220 !important;
        -webkit-text-fill-color: #0B1220 !important;
        opacity: 1 !important;
    }
    div[data-testid="stNumberInput"] [disabled],
    div[data-testid="stNumberInput"] [aria-disabled="true"],
    div[data-testid="stNumberInput"] [data-disabled="true"],
    div[data-testid="stNumberInput"] [data-baseweb="input"],
    div[data-testid="stNumberInput"] [data-baseweb="base-input"] {
        background: #FFFFFF !important;
        color: #0B1220 !important;
        -webkit-text-fill-color: #0B1220 !important;
        opacity: 1 !important;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInput"] input:disabled,
    div[data-testid="stNumberInput"] input[aria-disabled="true"] {
        color: #0B1220 !important;
        -webkit-text-fill-color: #0B1220 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] svg,
    div[data-baseweb="input"] svg {
        color: var(--kaashify-text) !important;
        fill: var(--kaashify-text) !important;
    }
    input:focus, textarea:focus,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--kaashify-blue) !important;
        box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.14) !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 1px dashed #B7C4D5 !important;
        border-radius: 10px !important;
        color: var(--kaashify-text) !important;
    }
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploaderDropzone"] > div,
    div[data-testid="stFileUploaderDropzoneInstructions"],
    div[data-testid="stFileUploaderDropzoneInstructions"] > div {
        background: #FFFFFF !important;
        color: var(--kaashify-text) !important;
        opacity: 1 !important;
    }
    div[data-testid="stFileUploaderDropzone"] * {
        color: var(--kaashify-text) !important;
        -webkit-text-fill-color: var(--kaashify-text) !important;
        opacity: 1 !important;
    }
    div[data-testid="stFileUploaderDropzone"] button,
    div[data-testid="stFileUploader"] button {
        background: #EFF6FF !important;
        color: var(--kaashify-navy) !important;
        -webkit-text-fill-color: var(--kaashify-navy) !important;
        border: 1px solid #B7C7DC !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }
    div[data-testid="stFileUploaderDropzone"] button:hover,
    div[data-testid="stFileUploader"] button:hover {
        background: #DBEAFE !important;
        border-color: var(--kaashify-blue) !important;
        color: var(--kaashify-blue) !important;
        -webkit-text-fill-color: var(--kaashify-blue) !important;
    }
    div[data-testid="stFileUploaderDropzone"] svg,
    div[data-testid="stFileUploader"] svg {
        color: var(--kaashify-navy) !important;
        fill: var(--kaashify-navy) !important;
    }

    div[data-testid="stNumberInput"] button {
        background: #F8FAFC !important;
        color: var(--kaashify-navy) !important;
        border-color: #C7D2E0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stNumberInput"] button svg {
        color: var(--kaashify-navy) !important;
        fill: var(--kaashify-navy) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--kaashify-border) !important;
        background: #FFFFFF !important;
        box-shadow: 0 8px 18px rgba(15,23,42,.05) !important;
    }
    div[data-testid="stDataFrame"] button,
    div[data-testid="stElementToolbar"] button {
        background: #FFFFFF !important;
        color: var(--kaashify-navy) !important;
        border: 1px solid #C7D2E0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(15,23,42,.08) !important;
    }
    div[data-testid="stDataFrame"] button svg,
    div[data-testid="stElementToolbar"] button svg {
        color: var(--kaashify-navy) !important;
        fill: var(--kaashify-navy) !important;
    }
    .stAlert {
        border: 1px solid var(--kaashify-border) !important;
        color: var(--kaashify-text) !important;
    }
    .stAlert * {
        color: var(--kaashify-text) !important;
    }
    .kpi-container {
        color: var(--kaashify-navy) !important;
        font-weight: 700 !important;
    }
    .net-pay-val {
        color: var(--kaashify-blue) !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        margin-left: 8px;
    }
    .small-note {
        color: var(--kaashify-muted) !important;
        font-size:0.95rem;
        line-height: 1.55;
    }
</style>
"""

def apply_kaashify_theme():
    st.markdown(KAASHIFY_CSS, unsafe_allow_html=True)

def render_hero(title="Kaashify ERP", subtitle="Professional HR, payroll, onboarding, documents and secure local database operations.", kicker="Kaashify ERP"):
    apply_kaashify_theme()
    st.markdown(f"""
    <div class="kaashify-hero">
        <div class="kaashify-brand-pill">✦ {kicker}</div>
        <h1 class="kaashify-title">{title}</h1>
        <p class="kaashify-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle=None, kicker="Kaashify ERP"):
    apply_kaashify_theme()
    st.markdown(f"<div class='page-kicker'>{kicker}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='page-title'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='small-note' style='margin-top:-8px;margin-bottom:24px;'>{subtitle}</p>", unsafe_allow_html=True)
