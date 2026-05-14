import time
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# AI FRAUD INTELLIGENCE PLATFORM - FINAL BANK-STYLE VERSION
# =========================================================

st.set_page_config(
    page_title="AI Fraud Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS / DESIGN SYSTEM
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --bg:#F6F8FC;
    --card:#FFFFFF;
    --text:#071226;
    --muted:#64748B;
    --border:#E2E8F0;
    --soft:#EEF3F9;
    --navy:#06182A;
    --blue:#0B5BD3;
    --cyan:#12B8C8;
    --red:#EF4444;
    --orange:#F59E0B;
    --green:#16A34A;
    --purple:#7C3AED;
    --shadow:0 16px 38px rgba(15,23,42,.075);
    --shadow2:0 8px 22px rgba(15,23,42,.055);
}

html, body, [class*="css"]{font-family:'Inter',sans-serif !important;}
.stApp{background:var(--bg);color:var(--text);}
.block-container{
    padding-top:1.2rem !important;
    padding-left:2.05rem !important;
    padding-right:2.05rem !important;
    padding-bottom:3rem !important;
    max-width:1540px !important;
}
/* Keep Streamlit sidebar controls visible. Do not hide header/toolbar because the
   sidebar expand button lives there in recent Streamlit versions. */
#MainMenu, footer{visibility:hidden;}
header{visibility:visible !important;background:transparent !important;}
div[data-testid="stToolbar"]{visibility:visible !important;height:auto !important;position:relative !important;}
[data-testid="collapsedControl"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    z-index:9999999 !important;
    position:fixed !important;
    top:.65rem !important;
    left:.65rem !important;
    background:#FFFFFF !important;
    border:1px solid #CBD5E1 !important;
    border-radius:12px !important;
    box-shadow:0 10px 24px rgba(15,23,42,.18) !important;
}
button[kind="header"], button[data-testid="baseButton-header"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
}
section[data-testid="stSidebar"]{
    display:block !important;
    visibility:visible !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:radial-gradient(circle at top left,#17466F 0%,#081D33 38%,#020B16 100%) !important;
    border-right:1px solid rgba(255,255,255,.08);
}
section[data-testid="stSidebar"] > div{padding-top:1.25rem !important;}
section[data-testid="stSidebar"] *{color:#F8FAFC !important;}
section[data-testid="stSidebar"] .stRadio > label{display:none;}
section[data-testid="stSidebar"] div[role="radiogroup"] label{
    padding:.72rem .82rem !important;
    margin:.18rem 0 !important;
    border-radius:14px !important;
    min-height:44px;
    transition:all .18s ease;
    color:#DDE7F3 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(14,165,233,.14) !important;
    transform:translateX(2px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
    background:linear-gradient(135deg,#0B5BD3 0%,#07508F 100%) !important;
    box-shadow:0 12px 28px rgba(14,165,233,.24);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{
    font-weight:800 !important;
    font-size:14px !important;
}
.sidebar-brand{display:flex;gap:13px;align-items:center;margin:6px 2px 26px 2px;}
.brand-shield{width:54px;height:60px;border-radius:18px;border:2px solid rgba(226,232,240,.28);display:flex;align-items:center;justify-content:center;font-size:29px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 22px rgba(255,255,255,.05);}
.brand-title{font-size:21px;font-weight:900;line-height:1.16;letter-spacing:-.3px;}
.sidebar-pill{display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.075);border:1px solid rgba(255,255,255,.10);border-radius:16px;padding:12px 13px;margin-top:14px;}
.sidebar-user{display:flex;gap:10px;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10);border-radius:18px;padding:13px 12px;margin-top:24px;}
.avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(255,255,255,.25),rgba(255,255,255,.06));font-size:20px;}
.dot{width:8px;height:8px;border-radius:50%;background:#22C55E;display:inline-block;margin-right:8px;box-shadow:0 0 10px rgba(34,197,94,.8);}
.small-muted{font-size:12px;color:#90A4B9 !important;line-height:1.55;}
.badge-red,.badge-orange,.badge-green{color:white;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:900;}
.badge-red{background:#EF4444;}.badge-orange{background:#F59E0B;}.badge-green{background:#16A34A;}

/* Top */
.topbar{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;gap:18px;}
.page-title h1{margin:0;color:var(--text);font-weight:900;letter-spacing:-1px;font-size:35px;}
.page-title p{margin:7px 0 0 0;color:var(--muted);font-size:15px;font-weight:500;}
.top-actions{display:flex;gap:12px;align-items:center;}
.action-chip{background:#fff;border:1px solid var(--border);border-radius:13px;padding:12px 15px;color:#0F172A;font-weight:800;box-shadow:var(--shadow2);white-space:nowrap;}
.export-chip{background:linear-gradient(135deg,#0B5BD3,#1687FF);color:#fff;border-radius:13px;padding:12px 16px;font-weight:900;box-shadow:0 14px 28px rgba(11,91,211,.22);white-space:nowrap;}

/* Main cards */
.card{background:rgba(255,255,255,.96);border:1px solid var(--border);border-radius:22px;box-shadow:var(--shadow);padding:20px;margin-bottom:18px;transition:all .22s ease;}
.chart-header{background:rgba(255,255,255,.96);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow);padding:17px 20px;margin-bottom:16px;transition:all .22s ease;}
.chart-header:hover,.card:hover{box-shadow:0 20px 48px rgba(15,23,42,.10);}
.chart-title{display:flex;align-items:center;justify-content:space-between;color:#071226;font-weight:900;font-size:17px;gap:14px;}
.chart-sub{color:var(--muted);font-size:12px;font-weight:700;text-align:right;}
.kpi-card{position:relative;overflow:hidden;background:rgba(255,255,255,.97);border:1px solid var(--border);border-radius:18px;box-shadow:var(--shadow);padding:17px 18px;min-height:132px;transition:all .22s ease;}
.kpi-card:hover{transform:translateY(-4px);box-shadow:0 24px 55px rgba(15,23,42,.12);}
.kpi-card:after{content:"";position:absolute;right:-30px;top:-34px;width:86px;height:86px;background:radial-gradient(circle,rgba(14,165,233,.13),transparent 70%);}
.kpi-head{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.kpi-label{font-size:13.5px;font-weight:900;color:#0F172A;}
.kpi-icon{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:inset 0 0 18px rgba(255,255,255,.55);}
.kpi-value{font-size:26px;font-weight:950;color:#071226;margin-top:10px;letter-spacing:-.6px;word-break:break-word;line-height:1.05;}
.kpi-foot{display:flex;justify-content:space-between;align-items:center;margin-top:16px;color:var(--muted);font-weight:750;font-size:12.5px;gap:10px;}
.kpi-decision .kpi-value{font-size:21px !important;letter-spacing:-.45px;line-height:1.08;}
.primary-kpi .kpi-card{min-height:158px;border-color:#CBD5E1;}
.primary-kpi .kpi-value{font-size:40px !important;}
.trend-up{color:#16A34A;font-weight:900;}.trend-red{color:#EF4444;font-weight:900;}.trend-neutral{color:#64748B;font-weight:900;}

.metric-mini{display:flex;gap:10px;align-items:center;border:1px solid var(--border);border-radius:16px;padding:12px 14px;background:#fff;box-shadow:var(--shadow2);margin-bottom:10px;transition:all .22s ease;}
.metric-mini:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(15,23,42,.09);}
.metric-dot{width:34px;height:34px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;flex:0 0 auto;}
.metric-text{font-weight:900;color:#0F172A;font-size:13.5px;}
.metric-number{margin-left:auto;font-weight:950;color:#0F172A;text-align:right;}

.status-badge{display:inline-block;border-radius:999px;padding:6px 11px;font-size:12px;font-weight:950;border:1px solid transparent;}
.status-escalated{background:#7F1D1D;color:white;border-color:#DC2626;}
.status-high{background:#FFF7ED;color:#EA580C;border-color:#FDBA74;}
.status-review{background:#FFFBEB;color:#D97706;border-color:#FDE68A;}
.status-safe{background:#ECFDF5;color:#16A34A;border-color:#A7F3D0;}

.alert-box{border-radius:18px;padding:16px 18px;margin-bottom:14px;font-weight:850;box-shadow:var(--shadow2);line-height:1.65;transition:all .22s ease;}
.alert-red{background:#FFF1F2;border:1px solid #FDA4AF;color:#9F1239;}
.alert-orange{background:#FFFBEB;border:1px solid #FDE68A;color:#92400E;}
.alert-green{background:#ECFDF5;border:1px solid #A7F3D0;color:#065F46;}
.table-hint{font-size:12px;font-weight:900;color:#0B5BD3;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:7px 12px;display:inline-block;margin:0 0 12px 0;}
.page-purpose{background:#FFFFFF;border:1px solid #E2E8F0;border-left:6px solid #0B5BD3;border-radius:18px;padding:14px 16px;margin:0 0 18px 0;box-shadow:0 8px 22px rgba(15,23,42,.045);color:#334155;font-size:13px;font-weight:750;line-height:1.65;}
.page-purpose b{color:#071226;}
.connected-workspace{border:1px solid #DDE6F0;border-radius:26px;background:linear-gradient(180deg,#FFFFFF 0%,#F7FAFF 100%);box-shadow:0 18px 45px rgba(15,23,42,.08);padding:18px;margin-top:8px;margin-bottom:24px;}
.analysis-block{border:1px solid #DDE6F0;border-radius:24px;background:linear-gradient(180deg,#FFFFFF 0%,#F8FBFF 100%);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:18px;margin:18px 0 22px 0;}
.section-kicker{font-size:15px;font-weight:950;color:#071226;text-transform:uppercase;letter-spacing:.9px;margin:8px 0 12px 0;}
.soft-divider{height:1px;background:linear-gradient(90deg,transparent,#DDE6F0,transparent);margin:24px 0 18px 0;}
.section-gap{height:24px;}
.queue-search-note{font-size:12px;color:#64748B;font-weight:750;margin-top:-4px;margin-bottom:8px;}
.playbook-card{background:#F8FAFC;border:1px solid #DDE6F0;border-radius:16px;padding:13px 14px;margin-bottom:10px;}
.playbook-title{font-weight:950;color:#071226;font-size:14px;}
.playbook-sub{color:#64748B;font-size:12px;font-weight:750;margin-top:4px;line-height:1.55;}

.live-counter-card{background:linear-gradient(135deg,#FFFFFF 0%,#EEF7FF 100%);border:1px solid #BFDBFE;border-radius:22px;box-shadow:0 18px 42px rgba(11,91,211,.10);padding:18px 22px;margin:10px 0 16px 0;}
.live-counter-number{font-size:46px;font-weight:950;color:#071226;line-height:1;margin-top:8px;letter-spacing:-1.5px;}
.pipeline-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px;}
.pipeline-step{background:#fff;border:1px solid #E2E8F0;border-radius:18px;padding:16px;box-shadow:var(--shadow2);}
.step-num{width:30px;height:30px;border-radius:10px;background:#DBEAFE;color:#0B5BD3;display:flex;align-items:center;justify-content:center;font-weight:950;margin-bottom:10px;}
.step-title{font-weight:950;color:#071226;font-size:14px;}.step-sub{font-size:12px;color:#64748B;font-weight:700;margin-top:4px;line-height:1.5;}

/* Controls */
.stButton>button,.stDownloadButton>button{border-radius:13px !important;border:1px solid var(--border) !important;font-weight:850 !important;min-height:42px;box-shadow:var(--shadow2);transition:all .22s ease;}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#0B5BD3 !important;color:#0B5BD3 !important;transform:translateY(-1px);}
div[data-testid="stFileUploader"] section{border:1.5px dashed #C8D4E4;background:#fff;border-radius:22px;padding:28px;box-shadow:var(--shadow);}
div[data-testid="stDataFrame"]{border-radius:16px;overflow:visible !important;border:1px solid var(--border);box-shadow:var(--shadow2);}
/* Plotly and dataframe toolbars: hidden by default, visible on hover */
.js-plotly-plot .modebar{opacity:0 !important;visibility:hidden !important;transition:opacity .16s ease !important;}
.js-plotly-plot:hover .modebar{opacity:1 !important;visibility:visible !important;}
div[data-testid="stElementToolbar"]{opacity:0 !important;visibility:hidden !important;transition:opacity .16s ease !important;}
div[data-testid="stElementContainer"]:hover div[data-testid="stElementToolbar"],
div[data-testid="stDataFrame"]:hover ~ div[data-testid="stElementToolbar"],
div[data-testid="stDataFrame"]:hover div[data-testid="stElementToolbar"]{opacity:1 !important;visibility:visible !important;}
.stTabs [data-baseweb="tab-list"]{gap:14px;background:#EDF3FA;border-radius:16px;padding:8px;}
.stTabs [data-baseweb="tab"]{border-radius:13px;font-weight:850;color:#334155;min-height:44px;padding:10px 14px !important;}
.stTabs [aria-selected="true"]{background:#fff;color:#0B5BD3;box-shadow:var(--shadow2);min-height:48px;padding:12px 17px !important;border-radius:14px !important;}

/* Sidebar dataset button should stay visible without hover */
section[data-testid="stSidebar"] .stButton>button{
    background:#FFFFFF !important;
    color:#0B5BD3 !important;
    border:1px solid rgba(255,255,255,.85) !important;
    box-shadow:0 10px 24px rgba(0,0,0,.18) !important;
}
section[data-testid="stSidebar"] .stButton>button p,
section[data-testid="stSidebar"] .stButton>button span{
    color:#0B5BD3 !important;
    font-weight:900 !important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:#EFF6FF !important;
    border-color:#93C5FD !important;
    color:#07508F !important;
}

@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:1100px){
    .topbar{flex-direction:column}.page-title h1{font-size:30px}.block-container{padding-left:1rem !important;padding-right:1rem !important}.top-actions{flex-wrap:wrap}.pipeline-steps{grid-template-columns:1fr 1fr}.kpi-card{min-height:124px}
}


/* Compact professional controls */
.tools-panel{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin:8px 0 14px 0;box-shadow:0 8px 22px rgba(15,23,42,.045);}
.live-ticker{background:linear-gradient(135deg,#FFFFFF 0%,#F8FBFF 100%);border:1px solid #DDE6F0;border-radius:22px;padding:18px 20px;margin:12px 0 18px 0;box-shadow:0 18px 42px rgba(15,23,42,.075);}
.live-ticker-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:center;}
.live-metric-label{color:#64748B;font-size:12px;font-weight:900;letter-spacing:.7px;text-transform:uppercase;}
.live-counter-number{font-size:44px;font-weight:950;color:#071226;line-height:1;margin-top:8px;}
.live-event-strip{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:13px 14px;color:#0F172A;font-weight:850;}
.live-dot{width:10px;height:10px;border-radius:50%;display:inline-block;background:#22C55E;margin-right:8px;box-shadow:0 0 0 6px rgba(34,197,94,.13);}
@media(max-width:1100px){.live-ticker-grid{grid-template-columns:1fr;}}


.chart-header{min-height:64px;display:flex;align-items:center;}
.chart-title{width:100%;}
.chart-title .chart-sub:empty{display:none;}
.live-counter-card{max-width:100%;}

/* Final spacing polish */
.section-divider{height:2px;background:#CBD5E1;border-radius:999px;margin:28px 0 24px 0;box-shadow:0 1px 0 rgba(255,255,255,.55);}
.audit-tab-spacer{height:12px;}
.report-toolbar{display:flex;justify-content:space-between;align-items:center;gap:16px;background:#FFFFFF;border:1px solid #D6E0EC;border-radius:18px;padding:14px 16px;margin:10px 0 16px 0;box-shadow:0 10px 26px rgba(15,23,42,.055);}
.report-title{font-weight:950;color:#071226;font-size:16px;}
.report-sub{font-size:12px;font-weight:750;color:#64748B;margin-top:3px;}
.report-table-wrap div[data-testid="stDataFrame"]{border:1px solid #CBD5E1;box-shadow:0 14px 32px rgba(15,23,42,.07);}

/* Audit outputs cards */
.output-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:12px 0 18px 0;}
.output-card{background:#FFFFFF;border:1px solid #D6E0EC;border-radius:18px;padding:16px 17px;box-shadow:0 10px 26px rgba(15,23,42,.055);min-height:112px;}
.output-card-title{font-weight:950;color:#071226;font-size:14px;margin-bottom:6px;}
.output-card-sub{font-weight:750;color:#64748B;font-size:12px;line-height:1.55;}
.output-chip{display:inline-block;margin-top:10px;background:#EFF6FF;border:1px solid #BFDBFE;color:#0B5BD3;border-radius:999px;padding:5px 9px;font-size:11px;font-weight:950;}
@media(max-width:1100px){.output-grid{grid-template-columns:1fr;}}


/* SAFE MOBILE LIGHT MODE FIX */
html, body, [class*="css"] {
    color-scheme: light !important;
}
.stApp {
    background: #F6F8FC !important;
    color: #071226 !important;
}
.card,
.chart-header,
.kpi-card,
.metric-mini,
.playbook-card,
.live-counter-card,
.pipeline-step,
.report-toolbar,
.output-card,
div[data-testid="stDataFrame"],
div[data-baseweb="select"] > div,
input,
textarea {
    background-color: #FFFFFF !important;
    color: #071226 !important;
}
.stButton > button,
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #071226 !important;
    border-color: #D6E0EC !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# MODEL AND DATA LOGIC
# =========================================================
@st.cache_resource
def load_assets():
    model = joblib.load("isolation_forest_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_assets()

required_columns = [
    "TransactionID", "AccountID", "TransactionAmount", "TransactionDate",
    "TransactionType", "Location", "DeviceID", "IP Address", "MerchantID",
    "Channel", "CustomerAge", "CustomerOccupation", "TransactionDuration",
    "LoginAttempts", "AccountBalance", "PreviousTransactionDate"
]

numerical_features = [
    "TransactionAmount", "CustomerAge", "TransactionDuration", "LoginAttempts",
    "AccountBalance", "TransactionHour", "TransactionDay", "TransactionMonth",
    "TransactionDayOfWeek", "TimeSincePreviousTransaction_Minutes",
    "Is_Night_Transaction", "Account_Avg_Amount", "Account_Amount_Deviation",
    "Amount_ZScore_By_Account", "Amount_To_Balance_Ratio",
    "Rapid_Transaction_Flag", "High_Amount_Flag", "High_Login_Attempts_Flag",
    "Rare_Location_Flag", "Rare_Device_Flag", "Rare_Merchant_Flag"
]

categorical_features = [
    "TransactionType", "Location", "DeviceID", "MerchantID", "Channel", "CustomerOccupation"
]


def init_state():
    defaults = {
        "data_loaded": False,
        "df": None,
        "current_page": "▦  Command Center",
        "selected_txn": None,
        "case_decisions": {},
        "audit_log": [],
        "live_count": 50,
        "monitoring_on": False,
        "live_manual_slider_version": 0,
        "last_loaded_at": None,
        "account_actions": {},
        "transaction_actions": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()


def read_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    if file.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    return None


def create_features(df):
    df = df.copy().dropna().drop_duplicates().reset_index(drop=True)
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["PreviousTransactionDate"] = pd.to_datetime(df["PreviousTransactionDate"])
    df["TransactionHour"] = df["TransactionDate"].dt.hour
    df["TransactionDay"] = df["TransactionDate"].dt.day
    df["TransactionMonth"] = df["TransactionDate"].dt.month
    df["TransactionDayOfWeek"] = df["TransactionDate"].dt.dayofweek
    df["TimeSincePreviousTransaction_Minutes"] = (
        df["TransactionDate"] - df["PreviousTransactionDate"]
    ).dt.total_seconds() / 60
    df["Is_Night_Transaction"] = df["TransactionHour"].apply(lambda x: 1 if x < 6 or x > 22 else 0)

    avg = df.groupby("AccountID")["TransactionAmount"].transform("mean")
    std = df.groupby("AccountID")["TransactionAmount"].transform("std").fillna(0)
    df["Account_Avg_Amount"] = avg
    df["Account_Amount_Deviation"] = df["TransactionAmount"] - avg
    df["Amount_ZScore_By_Account"] = (df["TransactionAmount"] - avg) / (std + 1e-6)
    df["Amount_To_Balance_Ratio"] = df["TransactionAmount"] / (df["AccountBalance"] + 1e-6)
    df["Rapid_Transaction_Flag"] = df["TimeSincePreviousTransaction_Minutes"].apply(lambda x: 1 if x < 5 else 0)
    amount_95 = df["TransactionAmount"].quantile(0.95)
    df["High_Amount_Flag"] = df["TransactionAmount"].apply(lambda x: 1 if x > amount_95 else 0)
    df["High_Login_Attempts_Flag"] = df["LoginAttempts"].apply(lambda x: 1 if x >= 3 else 0)
    df["Rare_Location_Flag"] = df.groupby(["AccountID", "Location"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    df["Rare_Device_Flag"] = df.groupby(["AccountID", "DeviceID"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    df["Rare_Merchant_Flag"] = df.groupby(["AccountID", "MerchantID"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    return df


def risk_category(score):
    if score < 30:
        return "Low"
    if score < 60:
        return "Medium"
    return "High"


def case_status(score):
    if score >= 80:
        return "Escalated"
    if score >= 60:
        return "High Priority"
    if score >= 30:
        return "Needs Review"
    return "Safe"


def recommended_action(row):
    if row["Case_Status"] == "Escalated":
        return "Temporarily hold transaction and escalate to fraud investigation team."
    if row["Case_Status"] == "High Priority":
        return "Verify customer activity and assign to analyst review queue."
    if row["Case_Status"] == "Needs Review":
        return "Monitor account activity and review related transactions."
    return "No immediate action required."


def risk_reason(row):
    reasons = []
    if row["High_Amount_Flag"] == 1: reasons.append("High transaction amount")
    if row["Rapid_Transaction_Flag"] == 1: reasons.append("Rapid transaction behavior")
    if row["Is_Night_Transaction"] == 1: reasons.append("Night-time activity")
    if row["High_Login_Attempts_Flag"] == 1: reasons.append("Multiple login attempts")
    if row["Rare_Location_Flag"] == 1: reasons.append("Unusual location")
    if row["Rare_Device_Flag"] == 1: reasons.append("Unusual device")
    if row["Rare_Merchant_Flag"] == 1: reasons.append("Rare merchant")
    if row["Anomaly_Flag"] == 1: reasons.append("ML anomaly detected")
    return " | ".join(reasons) if reasons else "Normal behavior"


def case_priority_score(row):
    triggered = (
        int(row.get("High_Amount_Flag", 0)) + int(row.get("Rapid_Transaction_Flag", 0)) +
        int(row.get("Is_Night_Transaction", 0)) + int(row.get("High_Login_Attempts_Flag", 0)) +
        int(row.get("Rare_Location_Flag", 0)) + int(row.get("Rare_Device_Flag", 0)) +
        int(row.get("Rare_Merchant_Flag", 0)) + int(row.get("Anomaly_Flag", 0))
    )
    return round((float(row["Final_Risk_Score"]) * 0.8) + (triggered * 2.5), 2)


@st.cache_data(show_spinner=False)
def process_data(raw_df):
    df = create_features(raw_df)
    X = df[numerical_features + categorical_features].copy()
    Xp = preprocessor.transform(X)
    pred = model.predict(Xp)
    score = model.decision_function(Xp)
    df["Anomaly_Flag"] = np.where(pred == -1, 1, 0)
    raw_risk = -score
    df["ML_Risk_Score"] = ((raw_risk - raw_risk.min()) / (raw_risk.max() - raw_risk.min() + 1e-6)) * 100
    df["Behavioral_Risk_Score"] = 0
    df["Behavioral_Risk_Score"] += df["High_Amount_Flag"] * 20
    df["Behavioral_Risk_Score"] += df["Rapid_Transaction_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Is_Night_Transaction"] * 10
    df["Behavioral_Risk_Score"] += df["High_Login_Attempts_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Location_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Device_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Merchant_Flag"] * 10
    df["Behavioral_Risk_Score"] = df["Behavioral_Risk_Score"].clip(0, 100)
    df["Final_Risk_Score"] = df["ML_Risk_Score"] * 0.6 + df["Behavioral_Risk_Score"] * 0.4
    df["Risk_Category"] = df["Final_Risk_Score"].apply(risk_category)
    df["Case_Status"] = df["Final_Risk_Score"].apply(case_status)
    df["Fraud_Probability"] = df["Final_Risk_Score"] / 100
    df["Fraud_Prediction"] = df["Risk_Category"].apply(lambda x: 1 if x == "High" else 0)
    df["Risk_Reason"] = df.apply(risk_reason, axis=1)
    df["Recommended_Action"] = df.apply(recommended_action, axis=1)
    df["Case_Priority_Score"] = df.apply(case_priority_score, axis=1)
    return df


def apply_decisions(df):
    df = df.copy()
    df["Analyst_Decision"] = df["TransactionID"].astype(str).map(st.session_state.case_decisions).fillna("Pending Review")
    return df


def log_action(txn, action, note="", row=None, playbook_action=None):
    txn = str(txn)
    st.session_state.case_decisions[txn] = action
    account_id = ""
    if row is not None:
        account_id = str(row.get("AccountID", ""))

    txn_effect = "Recorded analyst decision"
    if playbook_action == "Hold transaction and verify customer":
        st.session_state.transaction_actions[txn] = "Transaction Held - Customer Verification Required"
        txn_effect = "Transaction held and customer verification requested"
    elif playbook_action == "Temporarily block account":
        st.session_state.transaction_actions[txn] = "Transaction Held"
        if account_id:
            st.session_state.account_actions[account_id] = "Temporarily Blocked"
        txn_effect = "Transaction held and account temporarily blocked"
    elif playbook_action == "Escalate to senior fraud investigator":
        st.session_state.transaction_actions[txn] = "Escalated to Senior Investigator"
        txn_effect = "Case escalated to senior fraud investigator"
    elif playbook_action == "Request customer confirmation":
        st.session_state.transaction_actions[txn] = "Customer Confirmation Requested"
        txn_effect = "Customer confirmation requested before release"
    elif playbook_action == "Release transaction / no restriction":
        st.session_state.transaction_actions[txn] = "Released"
        txn_effect = "Transaction released with no account restriction"
    elif playbook_action == "Close as false positive":
        st.session_state.transaction_actions[txn] = "Closed as False Positive"
        txn_effect = "Alert closed as false positive"

    if action == "Confirmed Fraud":
        st.session_state.transaction_actions[txn] = "Transaction Held - Confirmed Fraud"
        if account_id:
            st.session_state.account_actions[account_id] = "Temporarily Blocked"
        txn_effect = "Confirmed fraud: transaction held, account blocked, case escalated"
    elif action == "False Positive":
        st.session_state.transaction_actions[txn] = "Released - False Positive"
        txn_effect = "False positive: alert closed and transaction released"
    elif action == "Marked Safe":
        st.session_state.transaction_actions[txn] = "Cleared"
        if account_id and st.session_state.account_actions.get(account_id) == "Temporarily Blocked":
            st.session_state.account_actions[account_id] = "Active"
        txn_effect = "Marked safe: case closed with no restriction"
    elif action == "Escalated":
        st.session_state.transaction_actions[txn] = "Escalated"
        txn_effect = "Case escalated for further investigation"
    elif action == "Under Investigation":
        st.session_state.transaction_actions[txn] = "Under Review"
        txn_effect = "Case remains open under investigation"
    elif action == "Reviewed":
        if txn not in st.session_state.transaction_actions:
            st.session_state.transaction_actions[txn] = "Reviewed"
        txn_effect = txn_effect if playbook_action else "Case reviewed by analyst"

    final_account_status = st.session_state.account_actions.get(account_id, "Active") if account_id else ""
    st.session_state.audit_log.append({
        "Timestamp": jordan_now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionID": txn,
        "AccountID": account_id,
        "Analyst": "Risk Analyst",
        "Decision": action,
        "Playbook_Action": playbook_action if playbook_action else "No playbook action selected",
        "Transaction_Action": st.session_state.transaction_actions.get(txn, "No action yet"),
        "Account_Action": final_account_status,
        "Operational_Effect": txn_effect,
        "Note": note,
    })
    try:
        st.toast(f"Action saved: {txn_effect}", icon="✅")
    except Exception:
        st.success(f"Action saved: {txn_effect}")


def open_case(txn):
    st.session_state.selected_txn = txn
    st.session_state.current_page = "▣  Investigation Workspace"
    st.rerun()

# =========================================================
# UI HELPERS
# =========================================================
def safe_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def status_class(status):
    if status == "Escalated": return "status-escalated"
    if status == "High Priority": return "status-high"
    if status == "Needs Review": return "status-review"
    return "status-safe"


def badge_class(value):
    if value == 0: return "badge-green"
    if value < 25: return "badge-orange"
    return "badge-red"



def jordan_now():
    return datetime.now(ZoneInfo("Asia/Amman"))


def render_topbar(title, subtitle, show_export=True, df=None):
    now = jordan_now()
    today_text = now.strftime("%b %d, %Y")
    time_text = now.strftime("%I:%M:%S %p")
    st.markdown(f"""
    <div class="topbar">
        <div class="page-title">
            <h1>{safe_html(title)}</h1>
            <p>{safe_html(subtitle)}</p>
        </div>
        <div class="top-actions">
            <div class="action-chip">🗓️ {today_text}<br>🕒 {time_text}<br>Amman, Jordan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label, value, icon, note="Today", trend="", tone="blue", primary=False):
    colors = {
        "blue": ("#DBEAFE", "#0B5BD3"),
        "orange": ("#FFEDD5", "#F97316"),
        "red": ("#FEE2E2", "#EF4444"),
        "green": ("#DCFCE7", "#16A34A"),
        "cyan": ("#CFFAFE", "#0891B2"),
        "navy": ("#E0E7FF", "#0F2D5C"),
        "purple": ("#EDE9FE", "#7C3AED"),
    }
    bg, fg = colors.get(tone, colors["blue"])
    trend_class = "trend-neutral"
    if "↑" in str(trend) or "+" in str(trend): trend_class = "trend-up"
    if "↓" in str(trend) or "Critical" in str(trend) or "Urgent" in str(trend) or tone == "red": trend_class = "trend-red"
    extra = "kpi-decision" if label in ["Decision", "Account Status", "Txn Action"] else ""
    wrapper = "primary-kpi" if primary else ""
    st.markdown(f"""
    <div class="{wrapper}">
        <div class="kpi-card {extra}">
            <div class="kpi-head">
                <div class="kpi-label">{safe_html(label)}</div>
                <div class="kpi-icon" style="background:{bg};color:{fg};">{icon}</div>
            </div>
            <div class="kpi-value">{safe_html(value)}</div>
            <div class="kpi-foot"><span>{safe_html(note)}</span><span class="{trend_class}">{safe_html(trend)}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def chart_wrapper(title, subtitle=""):
    st.markdown(f"""
    <div class="chart-header">
        <div class="chart-title"><span>{safe_html(title)}</span><span class="chart-sub">{safe_html(subtitle)}</span></div>
    </div>
    """, unsafe_allow_html=True)


def end_chart_wrapper():
    # Kept for compatibility. No closing HTML is needed because chart headers are self-contained.
    return None


def clean_fig(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=8, b=8),
        font=dict(family="Inter", color="#071226", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DDE6F0")
    fig.update_yaxes(showgrid=True, gridcolor="#EEF3F9", zeroline=False, linecolor="#DDE6F0")
    try:
        fig.update_traces(hovertemplate=None)
    except Exception:
        pass
    return fig


def chart_config(filename="fraud_chart"):
    # Plotly toolbar appears only on hover, matching professional dashboard behavior.
    return {
        "displayModeBar": "hover",
        "displaylogo": False,
        "responsive": True,
        "scrollZoom": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d", "toggleSpikelines"],
        "modeBarButtonsToAdd": ["drawline", "eraseshape"],
        "toImageButtonOptions": {"format": "png", "filename": filename, "height": 900, "width": 1400, "scale": 2},
    }


def gauge_fig(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value),
        number={"font": {"size": 30, "color": "#071226"}},
        gauge={
            "axis": {"range": [0, 100], "tickvals": [0, 100], "tickfont": {"size": 11}},
            "bar": {"color": "#071A2D", "thickness": 0.16},
            "bgcolor": "#E5E7EB",
            "borderwidth": 0,
            "steps": [{"range": [0, value], "color": "#12B8C8"}],
            "threshold": {"line": {"color": "#071A2D", "width": 4}, "thickness": 0.75, "value": value},
        },
    ))
    fig.update_layout(height=118, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def sidebar(df=None):
    open_cases = 0
    critical = 0
    reviewed = 0
    if df is not None:
        active = df[df["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"]) & df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])]
        open_cases = len(active)
        critical = int((active["Case_Status"] == "Escalated").sum())
        reviewed = int((df["Analyst_Decision"] != "Pending Review").sum())

    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <div class="brand-shield">🛡️</div>
        <div class="brand-title">AI Fraud<br>Intelligence<br>Platform</div>
    </div>
    """, unsafe_allow_html=True)

    pages = ["▦  Command Center", "⌁  Live Monitoring", "▣  Investigation Workspace", "☷  Audit & Reports"]
    current = st.session_state.current_page if st.session_state.current_page in pages else pages[0]
    page = st.sidebar.radio("Navigation", pages, index=pages.index(current))
    st.session_state.current_page = page

    jordan_time = jordan_now()
    if "session_started_at" not in st.session_state:
        st.session_state.session_started_at = datetime.now().timestamp()
    runtime_seconds = max(0, int(datetime.now().timestamp() - st.session_state.session_started_at))
    runtime_h = runtime_seconds // 3600
    runtime_m = (runtime_seconds % 3600) // 60
    runtime_s = runtime_seconds % 60

    st.sidebar.markdown(f"""
    <div class="sidebar-pill"><span>Open Queue</span><span class="{badge_class(open_cases)}">{open_cases}</span></div>
    <div class="sidebar-pill"><span>Critical</span><span class="{badge_class(critical)}">{critical}</span></div>
    <div class="sidebar-user"><div class="avatar">👤</div><div><b>Risk Analyst</b><br><span class="small-muted">Fraud Operations</span></div></div>
    <div style="margin-top:18px" class="small-muted"><span class="dot"></span>Last Updated<br>{jordan_time.strftime('%b %d, %Y %I:%M:%S %p')}<br>Reviewed cases: {reviewed}<br><br>System Runtime<br>{runtime_h:02d}h {runtime_m:02d}m {runtime_s:02d}s</div>
    """, unsafe_allow_html=True)

    if df is not None:
        if st.sidebar.button("Change Dataset", use_container_width=True):
            st.session_state.data_loaded = False
            st.session_state.df = None
            st.session_state.selected_txn = None
            st.session_state.current_page = "▦  Command Center"
            st.rerun()
    return page


def alert_panel(df):
    critical = df[(df["Case_Status"] == "Escalated") & (df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))].sort_values("Final_Risk_Score", ascending=False)
    high = df[(df["Case_Status"] == "High Priority") & (df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))].sort_values("Final_Risk_Score", ascending=False)
    if not critical.empty:
        row = critical.iloc[0]
        st.markdown(f'<div class="alert-box alert-red">🚨 Critical alert detected — Transaction {safe_html(row["TransactionID"])} | Risk Score {row["Final_Risk_Score"]:.2f} | {safe_html(row["Risk_Reason"])}</div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.45, 1.45, 4.1])
        if c1.button("Open Critical Case", use_container_width=True): open_case(row["TransactionID"])
        if c2.button("Mark Reviewed", use_container_width=True):
            log_action(row["TransactionID"], "Reviewed", "Reviewed from alert panel", row)
            st.rerun()
    elif not high.empty:
        row = high.iloc[0]
        st.markdown(f'<div class="alert-box alert-orange">⚠️ High priority case — Transaction {safe_html(row["TransactionID"])} | Risk Score {row["Final_Risk_Score"]:.2f} | {safe_html(row["Risk_Reason"])}</div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.45, 1.45, 4.1])
        if c1.button("Open High Risk Case", use_container_width=True): open_case(row["TransactionID"])
        if c2.button("Mark Reviewed", use_container_width=True):
            log_action(row["TransactionID"], "Reviewed", "Reviewed from alert panel", row)
            st.rerun()
    else:
        st.markdown('<div class="alert-box alert-green">✅ No open critical alerts detected.</div>', unsafe_allow_html=True)


def filtered_df(df, key_prefix="main"):
    with st.expander("Filters", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        statuses = c1.multiselect("Case Status", sorted(df["Case_Status"].unique()), default=sorted(df["Case_Status"].unique()), key=f"{key_prefix}_status")
        channels = c2.multiselect("Channel", sorted(df["Channel"].astype(str).unique()), default=sorted(df["Channel"].astype(str).unique()), key=f"{key_prefix}_channel")
        locations = c3.multiselect("Location", sorted(df["Location"].astype(str).unique()), default=sorted(df["Location"].astype(str).unique()), key=f"{key_prefix}_location")
        risk_range = c4.slider("Risk Score", 0, 100, (0, 100), key=f"{key_prefix}_risk")
    return df[df["Case_Status"].isin(statuses) & df["Channel"].astype(str).isin(channels) & df["Location"].astype(str).isin(locations) & df["Final_Risk_Score"].between(risk_range[0], risk_range[1])].copy()



def interactive_table(data, key, filename, height=420, selectable=True, default_columns=None, max_default_rows=None, controls_mode="hidden", highlight_txn=None):
    """Reusable analyst table with optional popover customization controls."""
    table_df = data.copy()
    if default_columns is None:
        default_columns = list(table_df.columns)
    default_columns = [c for c in default_columns if c in table_df.columns]

    visible_cols = default_columns if default_columns else list(table_df.columns)
    row_limit = min(max_default_rows or len(table_df), len(table_df)) if len(table_df) else 1

    if controls_mode == "customize":
        if hasattr(st, "popover"):
            controls = st.popover("Customize Table")
        else:
            controls = st.expander("Customize Table", expanded=False)
        with controls:
            visible_cols = st.multiselect(
                "Visible columns",
                list(table_df.columns),
                default=default_columns,
                key=f"{key}_visible_cols",
            )
            if not visible_cols:
                visible_cols = default_columns if default_columns else list(table_df.columns)
            row_limit = st.number_input(
                "Rows to show",
                min_value=1,
                max_value=max(len(table_df), 1),
                value=max(row_limit, 1),
                step=1,
                key=f"{key}_row_limit",
            )
            st.download_button(
                "Download",
                table_df[visible_cols].head(int(row_limit)).to_csv(index=False).encode("utf-8"),
                filename,
                "text/csv",
                use_container_width=True,
                key=f"{key}_download",
            )

    shown = table_df[visible_cols].head(int(row_limit)).copy()
    display_data = shown
    if highlight_txn is not None and "TransactionID" in shown.columns:
        highlight_value = str(highlight_txn)
        def _highlight_selected(row):
            is_selected = str(row.get("TransactionID", "")) == highlight_value
            return [
                "background-color: #EAF3FF; color: #071226; font-weight: 900; border-top: 2px solid #0B5BD3; border-bottom: 2px solid #0B5BD3;"
                if is_selected else "" for _ in row
            ]
        display_data = shown.style.apply(_highlight_selected, axis=1)
    event = st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        height=height,
        on_select="rerun" if selectable else "ignore",
        selection_mode="single-row" if selectable else "multi-row",
        key=f"{key}_df",
    )
    return event, shown


def report_table(data, key, filename, height=560):
    """Clean final report table without Table options, with direct CSV export."""
    st.markdown('<div class="report-table-wrap">', unsafe_allow_html=True)
    st.dataframe(data, use_container_width=True, hide_index=True, height=height, key=key)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button(
        "Download Final Power BI CSV",
        data.to_csv(index=False).encode("utf-8"),
        filename,
        "text/csv",
        use_container_width=True,
        key=f"{key}_download",
    )


# =========================================================
# UPLOAD GATE
# =========================================================
def upload_gate():
    sidebar(None)
    render_topbar("AI Fraud Intelligence Platform", "Upload a bank transaction dataset to start operational fraud monitoring", show_export=False)
    st.markdown("""
    <div class="card" style="padding:34px;">
        <div style="font-size:28px;font-weight:950;color:#071226;margin-bottom:8px;">Secure Dataset Intake</div>
        <div style="color:#64748B;font-weight:750;margin-bottom:18px;line-height:1.8;">The system validates required columns, generates behavioral indicators, applies the Isolation Forest model, and opens the Command Center automatically.</div>
        <div class="pipeline-steps">
            <div class="pipeline-step"><div class="step-num">1</div><div class="step-title">Upload</div><div class="step-sub">CSV or Excel transaction dataset</div></div>
            <div class="pipeline-step"><div class="step-num">2</div><div class="step-title">Validate</div><div class="step-sub">Required banking columns check</div></div>
            <div class="pipeline-step"><div class="step-num">3</div><div class="step-title">Analyze</div><div class="step-sub">Feature engineering + ML risk scoring</div></div>
            <div class="pipeline-step"><div class="step-num">4</div><div class="step-title">Investigate</div><div class="step-sub">Command center and case workflow</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose transaction file", type=["csv", "xlsx", "xls"])
    if uploaded_file is None:
        st.stop()
    raw_df = read_file(uploaded_file)
    if raw_df is None:
        st.error("Unsupported file format.")
        st.stop()
    missing = [c for c in required_columns if c not in raw_df.columns]
    if missing:
        st.error(f"Dataset validation failed. Missing columns: {missing}")
        st.stop()

    progress = st.progress(0)
    status = st.empty()
    loading_steps = [
        "Validating transaction structure...",
        "Cleaning missing and duplicate records...",
        "Generating behavioral fraud indicators...",
        "Applying anomaly detection model...",
        "Calculating final risk scores...",
        "Preparing banking operations dashboard...",
    ]
    for i, msg in enumerate(loading_steps):
        status.info(msg)
        progress.progress(int(((i + 1) / len(loading_steps)) * 100))
        time.sleep(0.25)
    st.session_state.df = apply_decisions(process_data(raw_df))
    st.session_state.live_count = min(50, len(st.session_state.df))
    st.session_state.data_loaded = True
    st.session_state.last_loaded_at = jordan_now().strftime("%Y-%m-%d %H:%M:%S")
    st.success("Dataset analyzed successfully. Opening Command Center...")
    time.sleep(0.5)
    st.rerun()

# =========================================================
# CASE / ACTION WORKFLOW
# =========================================================
def render_action_playbook(selected, note_key="case_note"):
    current_account_action = st.session_state.account_actions.get(str(selected["AccountID"]), "Active")
    current_txn_action = st.session_state.transaction_actions.get(str(selected["TransactionID"]), "No action yet")
    st.markdown(f"""
    <div class="playbook-card">
        <div class="playbook-title">Operational Action Status</div>
        <div class="playbook-sub">Transaction: <b>{safe_html(current_txn_action)}</b> · Account: <b>{safe_html(current_account_action)}</b></div>
    </div>
    """, unsafe_allow_html=True)
    playbook = st.selectbox(
        "Fraud Playbook Action",
        [
            "Hold transaction and verify customer",
            "Temporarily block account",
            "Escalate to senior fraud investigator",
            "Request customer confirmation",
            "Release transaction / no restriction",
            "Close as false positive",
        ],
        key=f"playbook_{selected['TransactionID']}",
    )
    note = st.text_area("Analyst Note", placeholder="Write investigation note...", height=105, key=note_key)
    b1, b2, b3 = st.columns(3)
    if b1.button("Reviewed", use_container_width=True, key=f"rev_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Reviewed", note, selected, playbook); st.rerun()
    if b2.button("Under Investigation", use_container_width=True, key=f"und_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Under Investigation", note, selected, playbook); st.rerun()
    if b3.button("Escalate", use_container_width=True, key=f"esc_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Escalated", note, selected, playbook); st.rerun()
    b4, b5, b6 = st.columns(3)
    if b4.button("Mark Safe", use_container_width=True, key=f"safe_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Marked Safe", note, selected, playbook); st.rerun()
    if b5.button("False Positive", use_container_width=True, key=f"fp_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "False Positive", note, selected, playbook); st.rerun()
    if b6.button("Confirmed Fraud", use_container_width=True, key=f"fraud_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Confirmed Fraud", note, selected, playbook); st.rerun()


def render_case_block(df, selected):
    account_df = df[df["AccountID"] == selected["AccountID"]].copy()
    st.markdown('<div class="soft-divider"></div><div class="section-kicker">Selected Case Study</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:18px;">
        <div>
            <div style="font-size:13px;font-weight:950;color:#64748B;text-transform:uppercase;letter-spacing:.7px;">Transaction Case</div>
            <div style="font-size:28px;font-weight:950;color:#071226;line-height:1.15;margin-top:4px;">{safe_html(selected['TransactionID'])}</div>
            <div style="font-size:14px;color:#64748B;font-weight:800;margin-top:4px;">Account {safe_html(selected['AccountID'])} · {safe_html(selected['Channel'])} · {safe_html(selected['Location'])}</div>
        </div>
        <div style="text-align:right;">
            <div class="status-badge {status_class(selected['Case_Status'])}" style="font-size:13px;padding:7px 13px;">{safe_html(selected['Case_Status'])}</div>
            <div style="font-size:12px;color:#64748B;font-weight:850;margin-top:9px;">Analyst Decision: {safe_html(selected['Analyst_Decision'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Risk Score", f"{selected['Final_Risk_Score']:.2f}", "◌", "Final score", "", "red")
    with k2: kpi_card("Priority Score", f"{selected['Case_Priority_Score']:.2f}", "⇧", "Queue ranking", "", "orange")
    with k3: kpi_card("Amount", f"{selected['TransactionAmount']:,.2f}", "$", "Transaction value", "", "blue")
    with k4:
        current_txn_action = st.session_state.transaction_actions.get(str(selected["TransactionID"]), "No action yet")
        kpi_card("Txn Action", current_txn_action, "⚙", "Operational", "", "green")

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, .85])
    with left:
        chart_wrapper("Risk Explanation", "Why this case was prioritized")
        st.markdown(f'<div class="alert-box alert-orange"><b>Risk Reason</b><br>{safe_html(selected["Risk_Reason"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="playbook-card"><div class="playbook-title">Recommended Next Action</div><div class="playbook-sub">{safe_html(selected["Recommended_Action"])}</div></div>', unsafe_allow_html=True)
        account_status = st.session_state.account_actions.get(str(selected["AccountID"]), "Active")
        p1, p2, p3 = st.columns(3)
        with p1: kpi_card("Account Txns", f"{len(account_df):,}", "▣", "History", "", "blue")
        with p2: kpi_card("Avg Account Risk", f"{account_df['Final_Risk_Score'].mean():.2f}", "◌", "Account", "", "cyan")
        with p3: kpi_card("Account Status", account_status, "🛡", "Current action", "", "green" if account_status == "Active" else "red")
        trend = account_df.sort_values("TransactionDate")
        fig = px.line(trend, x="TransactionDate", y="Final_Risk_Score", markers=True, color_discrete_sequence=["#0B5BD3"])
        fig.update_yaxes(range=[0, 100], title="Risk")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 250), use_container_width=True, config=chart_config("account_risk_profile"))
    with right:
        chart_wrapper("Triggered Risk Evidence", "Behavioral + ML indicators")
        indicators = {
            "High Amount": selected["High_Amount_Flag"],
            "Rapid Transaction": selected["Rapid_Transaction_Flag"],
            "Night Activity": selected["Is_Night_Transaction"],
            "Login Risk": selected["High_Login_Attempts_Flag"],
            "Rare Location": selected["Rare_Location_Flag"],
            "Rare Device": selected["Rare_Device_Flag"],
            "Rare Merchant": selected["Rare_Merchant_Flag"],
            "ML Anomaly": selected["Anomaly_Flag"],
        }
        for name, val in indicators.items():
            color = "#EF4444" if val == 1 else "#16A34A"
            label = "Triggered" if val == 1 else "Normal"
            st.markdown(f'<div class="metric-mini"><div class="metric-dot" style="background:{color}14;color:{color};">{"!" if val == 1 else "✓"}</div><div class="metric-text">{safe_html(name)}</div><div class="metric-number" style="color:{color};">{safe_html(label)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-divider"></div><div class="section-kicker">Decision & Action Workflow</div>', unsafe_allow_html=True)
    ac1, ac2 = st.columns([1.05, .95])
    with ac1:
        chart_wrapper("Analyst Decision Panel", "Choose decision and operational action")
        render_action_playbook(selected, note_key=f"note_{selected['TransactionID']}")
    with ac2:
        chart_wrapper("Case Timeline", "Decision trace")
        timeline_rows = [
            ("Dataset uploaded", st.session_state.get("last_loaded_at") or "Current session"),
            ("Risk score generated", f"{selected['Final_Risk_Score']:.2f}"),
            ("Priority score", f"{selected['Case_Priority_Score']:.2f}"),
            ("System case status", selected["Case_Status"]),
            ("Analyst decision", selected["Analyst_Decision"]),
            ("Operational effect", st.session_state.transaction_actions.get(str(selected["TransactionID"]), "Waiting for analyst action")),
        ]
        for title, value in timeline_rows:
            st.markdown(f'<div class="metric-mini"><div class="metric-dot" style="background:#DBEAFE;color:#0B5BD3;">•</div><div class="metric-text">{safe_html(title)}</div><div class="metric-number" style="font-size:12px;max-width:52%;text-align:right;">{safe_html(value)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    chart_wrapper("Connected Account Transactions", "Same account history")
    account_show = account_df[["TransactionID","TransactionDate","TransactionAmount","TransactionType","Location","Channel","Final_Risk_Score","Case_Status","Analyst_Decision","Risk_Reason"]].sort_values("TransactionDate", ascending=False)
    event_acc, shown_acc = interactive_table(account_show, f"account_txns_{selected['TransactionID']}", "connected_account_transactions.csv", height=340, selectable=True, default_columns=["TransactionID","TransactionDate","TransactionAmount","TransactionType","Location","Channel","Final_Risk_Score","Case_Status","Analyst_Decision"], max_default_rows=min(len(account_show), 20) if len(account_show) else 1, highlight_txn=selected["TransactionID"])
    if event_acc.selection.rows:
        txn_acc = shown_acc.iloc[event_acc.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn_acc
        st.rerun()

# =========================================================
# PAGES
# =========================================================
def page_command_center(df):
    render_topbar("Command Center", "Real-time overview of fraud risk and operations", show_export=False)

    open_cases = df[
        df["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"]) &
        df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])
    ].copy()
    escalated = int((open_cases["Case_Status"] == "Escalated").sum())
    flagged = int((df["Risk_Category"] == "High").sum())
    avg_risk = float(df["Final_Risk_Score"].mean())
    pending = int((df["Analyst_Decision"] == "Pending Review").sum())
    handled = int((df["Analyst_Decision"] != "Pending Review").sum())

    # =====================================================
    # 1) OPERATIONS SNAPSHOT — first thing the analyst sees
    # =====================================================
    st.markdown('<div class="section-kicker">Operations Snapshot</div>', unsafe_allow_html=True)
    a, b, c, d, e = st.columns(5)
    with a:
        kpi_card("Total Transactions", f"{len(df):,}", "▣", "Uploaded", "Active", "blue")
    with b:
        kpi_card("Flagged Transactions", f"{flagged:,}", "⚑", "High risk", "Review", "orange")
    with c:
        kpi_card("Escalated Cases", f"{escalated:,}", "⇧", "Critical queue", "Urgent" if escalated else "Stable", "red")
    with d:
        kpi_card("Avg Risk Score", f"{avg_risk:.1f}", "◌", "Overall risk", "Score", "cyan")
    with e:
        decision_text = "Pending Review" if pending else "All Clear"
        kpi_card("Decision", decision_text, "✓", "Workflow", f"{handled:,} handled", "green" if not pending else "orange")

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

    # =====================================================
    # 2) MAIN RISK OVERVIEW — chart row directly under KPIs
    # =====================================================
    left, right = st.columns([1.08, .92])
    with left:
        chart_wrapper("Risk Score Trend")
        daily = df.copy()
        daily["Date"] = daily["TransactionDate"].dt.date
        trend = daily.groupby("Date", as_index=False)["Final_Risk_Score"].mean().tail(7)
        fig = px.line(
            trend,
            x="Date",
            y="Final_Risk_Score",
            markers=True,
            text=trend["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0B5BD3"],
        )
        fig.update_traces(line=dict(width=3.8), marker=dict(size=9), textposition="top center")
        fig.update_yaxes(range=[0, 100], title="")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 340), use_container_width=True, config=chart_config("risk_score_trend"))

    with right:
        chart_wrapper("Case Status Distribution")
        status = df["Case_Status"].value_counts().reset_index()
        status.columns = ["Case_Status", "Count"]
        color_map = {
            "Safe": "#16A34A",
            "Needs Review": "#F59E0B",
            "High Priority": "#F97316",
            "Escalated": "#EF4444",
        }
        fig = px.pie(
            status,
            values="Count",
            names="Case_Status",
            hole=.62,
            color="Case_Status",
            color_discrete_map=color_map,
        )
        fig.update_traces(textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=3)))
        fig.add_annotation(
            text=f"<b>{len(df):,}</b><br>Total Cases",
            x=.5,
            y=.5,
            showarrow=False,
            font=dict(size=17, color="#071226"),
        )
        st.plotly_chart(clean_fig(fig, 340), use_container_width=True, config=chart_config("case_status_distribution"))

    # =====================================================
    # 3) SUPPORTING RISK INTELLIGENCE — compact visual row
    # =====================================================
    c1, c2, c3 = st.columns([1, 1, .92])
    with c1:
        chart_wrapper("Average Risk by Channel")
        channel = df.groupby("Channel", as_index=False)["Final_Risk_Score"].mean().sort_values("Final_Risk_Score", ascending=False)
        fig = px.bar(
            channel,
            x="Channel",
            y="Final_Risk_Score",
            text=channel["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0F2D5C"],
        )
        fig.update_traces(textposition="outside", marker_line_width=0, width=.55)
        fig.update_yaxes(range=[0, 100], title="Avg Risk Score")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 320), use_container_width=True, config=chart_config("risk_by_channel"))

    with c2:
        chart_wrapper("Top Risk Locations")
        location = (
            df.groupby("Location", as_index=False)["Final_Risk_Score"]
            .mean()
            .sort_values("Final_Risk_Score", ascending=False)
            .head(5)
        )
        fig = px.bar(
            location,
            y="Location",
            x="Final_Risk_Score",
            orientation="h",
            text=location["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0F2D5C"],
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_xaxes(range=[0, 100], title="Avg Risk Score")
        fig.update_yaxes(title="")
        fig.update_traces(textposition="outside")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.plotly_chart(clean_fig(fig, 320), use_container_width=True, config=chart_config("top_risk_locations"))

    with c3:
        chart_wrapper("Top Risk Indicators")
        indicators = [
            ("⇧", "High Amount", int(df["High_Amount_Flag"].sum()), "#EF4444"),
            ("☾", "Night Transactions", int(df["Is_Night_Transaction"].sum()), "#0B5BD3"),
            ("ϟ", "Rapid Transactions", int(df["Rapid_Transaction_Flag"].sum()), "#0B5BD3"),
            ("▣", "Rare Device", int(df["Rare_Device_Flag"].sum()), "#0B5BD3"),
            ("●", "Rare Location", int(df["Rare_Location_Flag"].sum()), "#0B5BD3"),
        ]
        for icon, name, count, color in indicators:
            pct = (count / max(len(df), 1)) * 100
            st.markdown(
                f'<div class="metric-mini">'
                f'<div class="metric-dot" style="background:{color}14;color:{color};">{icon}</div>'
                f'<div class="metric-text">{safe_html(name)}</div>'
                f'<div class="metric-number">{count:,}<span style="color:#64748B;font-size:12px;"> ({pct:.1f}%)</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # =====================================================
    # 4) FINAL TABLE — only the most important operations
    # =====================================================
    chart_wrapper("Recent High Risk Transactions")
    # Shows only currently open action cases.
    # Once the analyst takes a closing action such as Reviewed, Marked Safe,
    # False Positive, or Confirmed Fraud, the transaction is removed from this
    # Command Center queue and the next highest-priority open case appears.
    top_source = open_cases.copy()
    top = (
        top_source.sort_values(["Case_Priority_Score", "Final_Risk_Score"], ascending=False)
        .head(10)[[
            "TransactionID", "AccountID", "TransactionAmount", "Channel", "Location",
            "Final_Risk_Score", "Case_Priority_Score", "Case_Status", "Analyst_Decision"
        ]]
        .copy()
    )
    if top.empty:
        st.success("No open high-risk cases in the Command Center queue.")
        return
    top["Final_Risk_Score"] = top["Final_Risk_Score"].round(2)
    top["Case_Priority_Score"] = top["Case_Priority_Score"].round(2)
    event, shown = interactive_table(
        top,
        "cmd_recent_high_risk",
        "recent_high_risk_transactions.csv",
        height=330,
        selectable=True,
        default_columns=[
            "TransactionID", "AccountID", "TransactionAmount", "Channel", "Location",
            "Final_Risk_Score", "Case_Status", "Analyst_Decision"
        ],
        max_default_rows=10,
    )
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
        open_case(txn)

def page_live_monitor(df):
    render_topbar("Live Monitoring", "Real-time simulation with live counters, alerts, and transaction feed", show_export=False)

    if "live_last_txn" not in st.session_state:
        st.session_state.live_last_txn = "Waiting"
    if "live_last_time" not in st.session_state:
        st.session_state.live_last_time = "--"

    sorted_all = df.sort_values("TransactionDate", ascending=False).reset_index(drop=True)

    c1, c2, c3, _ = st.columns([1, 1, 1, 4])
    if c1.button("▶ Start", use_container_width=True):
        st.session_state.monitoring_on = True
    if c2.button("⏸ Stop", use_container_width=True):
        st.session_state.monitoring_on = False
        st.session_state.live_manual_slider_version = st.session_state.get("live_manual_slider_version", 0) + 1
    if c3.button("↻ Reset", use_container_width=True):
        st.session_state.live_count = min(50, len(df))
        st.session_state.monitoring_on = False
        st.session_state.live_manual_slider_version = st.session_state.get("live_manual_slider_version", 0) + 1
        st.session_state.live_last_txn = "Waiting"
        st.session_state.live_last_time = "--"

    # One source of truth for the whole live page.
    # The slider, the big live card, KPI Feed Size, charts, and table all use this same value.
    if st.session_state.monitoring_on and st.session_state.live_count < len(df):
        st.session_state.live_count = min(int(st.session_state.live_count) + 1, len(df))
        new_idx = min(int(st.session_state.live_count) - 1, len(sorted_all) - 1)
        st.session_state.live_last_txn = str(sorted_all.iloc[new_idx]["TransactionID"])
        st.session_state.live_last_time = datetime.now().strftime("%H:%M:%S")

    live_count = min(max(int(st.session_state.live_count), 1), len(df))

    if st.session_state.monitoring_on:
        st.slider(
            "Visible feed size",
            1,
            len(df),
            live_count,
            1,
            key=f"live_visible_feed_size_auto_{live_count}",
            disabled=True,
        )
    else:
        live_count = st.slider(
            "Visible feed size",
            1,
            len(df),
            live_count,
            1,
            key=f"live_visible_feed_size_manual_{st.session_state.get('live_manual_slider_version', 0)}",
        )
        st.session_state.live_count = int(live_count)

    live_count = min(max(int(st.session_state.live_count), 1), len(df))
    live_df = sorted_all.head(live_count).copy()

    high_count = int((live_df["Risk_Category"] == "High").sum())
    open_alerts = int(((live_df["Case_Status"].isin(["Escalated", "High Priority"])) & (live_df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))).sum())
    avg_preview = float(live_df["Final_Risk_Score"].mean()) if not live_df.empty else 0

    st.markdown(f"""
    <div class="live-counter-card">
        <div class="live-metric-label">Live feed size</div>
        <div class="live-counter-number">{live_count:,}</div>
        <div style="color:#64748B;font-size:12px;font-weight:800;margin-top:8px;">
            Latest transaction: <b>{safe_html(st.session_state.live_last_txn)}</b> · Last update {safe_html(st.session_state.live_last_time)} · High risk {high_count:,} · Open alerts {open_alerts:,} · Avg risk {avg_preview:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    alert_panel(live_df)

    a, b, c, d = st.columns(4)
    with a:
        kpi_card("Feed Size", f"{live_count:,}", "⌁", "Visible records", "Live", "cyan")
    with b:
        kpi_card("High Risk", f"{high_count:,}", "⚑", "Detected", "Review", "orange")
    with c:
        kpi_card("Open Alerts", f"{open_alerts:,}", "!", "Need action", "Active", "red")
    with d:
        kpi_card("Avg Risk", f"{avg_preview:.2f}", "◌", "Current feed", "Score", "blue")

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    cchart1, cchart2 = st.columns([1.05, .95])
    with cchart1:
        chart_wrapper("Live Risk Movement")
        live_trend = live_df.sort_values("TransactionDate").tail(35).copy()
        if not live_trend.empty:
            fig = px.line(live_trend, x="TransactionDate", y="Final_Risk_Score", markers=True, color_discrete_sequence=["#0B5BD3"])
            fig.update_traces(line=dict(width=3.8), marker=dict(size=8))
            fig.update_yaxes(range=[0, 100], title="Risk")
            fig.update_xaxes(title="")
            st.plotly_chart(clean_fig(fig, 270), use_container_width=True, config=chart_config("live_risk_movement"))
    with cchart2:
        chart_wrapper("Live Status Mix")
        stat = live_df["Case_Status"].value_counts().reset_index()
        stat.columns = ["Case_Status", "Count"]
        if not stat.empty:
            fig = px.bar(stat, x="Case_Status", y="Count", text="Count", color_discrete_sequence=["#0F2D5C"])
            fig.update_traces(textposition="outside")
            fig.update_xaxes(title="")
            fig.update_yaxes(title="")
            st.plotly_chart(clean_fig(fig, 270), use_container_width=True, config=chart_config("live_status_mix"))

    chart_wrapper("Live Transaction Feed")
    live_show = live_df[["TransactionID", "AccountID", "TransactionDate", "TransactionAmount", "Location", "Channel", "Final_Risk_Score", "Case_Priority_Score", "Case_Status", "Analyst_Decision"]].sort_values("Final_Risk_Score", ascending=False).copy()
    live_show["Final_Risk_Score"] = live_show["Final_Risk_Score"].round(2)
    live_show["Case_Priority_Score"] = live_show["Case_Priority_Score"].round(2)
    event, shown = interactive_table(
        live_show,
        "live_feed_table",
        "live_transaction_feed.csv",
        height=520,
        selectable=True,
        default_columns=["TransactionID", "AccountID", "TransactionDate", "TransactionAmount", "Location", "Channel", "Final_Risk_Score", "Case_Status", "Analyst_Decision"],
        max_default_rows=min(len(live_show), 50) if len(live_show) else 1,
    )
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
        open_case(txn)

    # Keep Live Monitoring moving after Start.
    # This restores the one-by-one live counter update without affecting other pages.
    if st.session_state.monitoring_on and st.session_state.live_count < len(df):
        time.sleep(0.28)
        st.rerun()


def page_investigation_workspace(df):
    render_topbar("Investigation Workspace", "Prioritized queue, case review, account profile, and analyst actions", show_export=False)
    st.markdown('<div class="section-kicker">Investigation Queue</div>', unsafe_allow_html=True)
    fdf = filtered_df(df, "queue")
    open_only = st.toggle("Show open cases only", value=True)
    if open_only:
        fdf = fdf[fdf["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])]
        fdf = fdf[fdf["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"])]
    fdf = fdf.sort_values(["Case_Priority_Score", "Final_Risk_Score"], ascending=False)
    a,b,c,d = st.columns(4)
    with a: kpi_card("Cases in View", f"{len(fdf):,}", "▣", "Filtered", "")
    with b: kpi_card("Pending", f"{(fdf['Analyst_Decision']=='Pending Review').sum():,}", "◷", "Needs action", "")
    with c: kpi_card("Critical", f"{(fdf['Case_Status']=='Escalated').sum():,}", "!", "Escalated", "Critical", "red")
    with d: kpi_card("Handled", f"{(df['Analyst_Decision']!='Pending Review').sum():,}", "✓", "Reviewed", "")
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    chart_wrapper("Investigation Queue", "Select case")
    if fdf.empty:
        st.success("No cases match the selected filters.")
        return
    cols = ["TransactionID","AccountID","TransactionAmount","Location","Channel","Final_Risk_Score","Case_Priority_Score","Case_Status","Analyst_Decision"]
    qshow = fdf[cols].copy(); qshow["Final_Risk_Score"] = qshow["Final_Risk_Score"].round(2); qshow["Case_Priority_Score"] = qshow["Case_Priority_Score"].round(2)

    search_txn = st.text_input(
        "Search TransactionID",
        placeholder="Type TransactionID here, e.g. TX000275",
        key="investigation_txn_search",
    ).strip()
    if search_txn:
        matched = fdf[fdf["TransactionID"].astype(str).str.contains(search_txn, case=False, na=False)].copy()
        if matched.empty:
            st.warning("No matching TransactionID found in the current queue filters.")
        else:
            picked = st.selectbox(
                "Matching cases",
                matched["TransactionID"].astype(str).tolist(),
                key="investigation_txn_match_select",
            )
            st.session_state.selected_txn = picked
            qshow = matched[cols].copy()
            qshow["Final_Risk_Score"] = qshow["Final_Risk_Score"].round(2)
            qshow["Case_Priority_Score"] = qshow["Case_Priority_Score"].round(2)
    st.markdown('<div class="queue-search-note">Select a row from the queue or search by TransactionID above.</div>', unsafe_allow_html=True)
    event, shown = interactive_table(qshow, "investigation_queue", "investigation_queue.csv", height=430, selectable=True, default_columns=cols, max_default_rows=12, controls_mode="customize")
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
    elif st.session_state.selected_txn not in fdf["TransactionID"].astype(str).tolist():
        st.session_state.selected_txn = str(qshow.iloc[0]["TransactionID"])
    selected = df[df["TransactionID"].astype(str) == str(st.session_state.selected_txn)].iloc[0]
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    render_case_block(df, selected)

def build_powerbi_report(df):
    """Build the final CSV used by Power BI without changing the dashboard structure."""
    export_columns = [
        "TransactionID", "AccountID", "TransactionDate", "PreviousTransactionDate",
        "TransactionAmount", "TransactionType", "Location", "DeviceID", "IP Address",
        "MerchantID", "Channel", "CustomerAge", "CustomerOccupation", "TransactionDuration",
        "LoginAttempts", "AccountBalance", "TimeSincePreviousTransaction_Minutes",
        "Is_Night_Transaction", "Rapid_Transaction_Flag", "High_Amount_Flag",
        "High_Login_Attempts_Flag", "Rare_Location_Flag", "Rare_Device_Flag",
        "Rare_Merchant_Flag", "Anomaly_Flag", "ML_Risk_Score", "Behavioral_Risk_Score",
        "Final_Risk_Score", "Case_Priority_Score", "Fraud_Probability", "Fraud_Prediction",
        "Risk_Category", "Case_Status", "Analyst_Decision", "Risk_Reason", "Recommended_Action",
    ]
    export_columns = [c for c in export_columns if c in df.columns]
    report = df[export_columns].copy()
    report["Transaction_Action"] = report["TransactionID"].astype(str).map(st.session_state.transaction_actions).fillna("No action yet")
    report["Account_Action"] = report["AccountID"].astype(str).map(st.session_state.account_actions).fillna("Active")
    return report


def page_audit_reports(df):
    render_topbar("Audit & Reports", "Complete investigation record, operational actions, and exportable reports", show_export=False)
    st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
    tabs = st.tabs(["Audit Overview", "Audit Trail", "Investigation Report", "Operational Outputs"])
    audit = pd.DataFrame(st.session_state.audit_log)
    report = build_powerbi_report(df)

    with tabs[0]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        a, b, c, d, e = st.columns(5)
        pending_cases = int((df["Analyst_Decision"] == "Pending Review").sum())
        confirmed = int(audit["Decision"].eq("Confirmed Fraud").sum()) if not audit.empty and "Decision" in audit else 0
        false_positive = int(audit["Decision"].eq("False Positive").sum()) if not audit.empty and "Decision" in audit else 0
        blocked = sum(1 for v in st.session_state.account_actions.values() if v == "Temporarily Blocked")
        with a:
            kpi_card("Recorded Actions", f"{len(audit):,}", "☷", "Audit log", "")
        with b:
            kpi_card("Confirmed Fraud", f"{confirmed:,}", "!", "Analyst", "", "orange")
        with c:
            kpi_card("False Positives", f"{false_positive:,}", "✓", "Closed", "", "green")
        with d:
            kpi_card("Blocked Accounts", f"{blocked:,}", "🛡", "Actioned", "", "red")
        with e:
            kpi_card("Pending Cases", f"{pending_cases:,}", "◷", "Awaiting review", "", "orange")

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            chart_wrapper("Decision Breakdown")
            if audit.empty or "Decision" not in audit:
                st.info("No analyst decisions yet.")
            else:
                dec = audit["Decision"].value_counts().reset_index()
                dec.columns = ["Decision", "Count"]
                fig = px.bar(dec, x="Decision", y="Count", color_discrete_sequence=["#0F2D5C"], text="Count")
                fig.update_traces(textposition="outside")
                st.plotly_chart(clean_fig(fig, 300), use_container_width=True, config=chart_config("decision_breakdown"))
        with c2:
            chart_wrapper("Recent Operational Actions")
            if audit.empty:
                st.info("No recent actions yet.")
            else:
                recent = audit.tail(5).iloc[::-1]
                for _, r in recent.iterrows():
                    st.markdown(
                        f'<div class="metric-mini"><div class="metric-dot" style="background:#DBEAFE;color:#0B5BD3;">•</div>'
                        f'<div class="metric-text">{safe_html(r.get("Decision", "Action"))}</div>'
                        f'<div class="metric-number" style="font-size:12px;max-width:60%;">{safe_html(r.get("TransactionID", ""))}<br>{safe_html(r.get("Timestamp", ""))}</div></div>',
                        unsafe_allow_html=True,
                    )

    with tabs[1]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        if audit.empty:
            st.info("No analyst actions recorded yet.")
        else:
            interactive_table(
                audit,
                "audit_trail_table",
                "audit_trail.csv",
                height=460,
                selectable=False,
                default_columns=list(audit.columns),
                max_default_rows=min(len(audit), 100) if len(audit) else 1,
                controls_mode="customize",
            )

    with tabs[2]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="report-toolbar">
            <div>
                <div class="report-title">Final Investigation Report Dataset</div>
                <div class="report-sub">Power BI ready output. It keeps the same core fraud results structure, with analyst decisions and operational actions added as extra columns.</div>
            </div>
            <div class="status-badge status-review">{len(report):,} rows</div>
        </div>
        """, unsafe_allow_html=True)

        # No Table Options here on purpose: this is the final complete report table for Power BI.
        report_table(report, "final_powerbi_report_table", "fraud_results.csv", height=560)

        actioned = report[report["Analyst_Decision"] != "Pending Review"].copy()
        st.download_button(
            "Download Actioned Cases Only",
            actioned.to_csv(index=False).encode("utf-8"),
            "actioned_cases_only.csv",
            "text/csv",
            use_container_width=True,
        )

    with tabs[3]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        audit_rows = len(audit)
        actioned_rows = int((report["Analyst_Decision"] != "Pending Review").sum())
        output_html = (
            '<div class="output-grid">'
            '<div class="output-card"><div class="output-card-title">fraud_results.csv</div>'
            '<div class="output-card-sub">Final Power BI source file with risk scores, case status, analyst decisions, and operational actions.</div>'
            f'<div class="output-chip">{len(report):,} rows</div></div>'
            '<div class="output-card"><div class="output-card-title">audit_trail.csv</div>'
            '<div class="output-card-sub">Chronological record of analyst decisions, notes, playbook actions, and case effects.</div>'
            f'<div class="output-chip">{audit_rows:,} actions</div></div>'
            '<div class="output-card"><div class="output-card-title">actioned_cases_only.csv</div>'
            '<div class="output-card-sub">Filtered export for reviewed, escalated, confirmed fraud, false positive, or marked safe cases.</div>'
            f'<div class="output-chip">{actioned_rows:,} cases</div></div>'
            '</div>'
        )
        st.markdown(output_html, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("Download fraud_results.csv", report.to_csv(index=False).encode("utf-8"), "fraud_results.csv", "text/csv", use_container_width=True)
        with c2:
            audit_export = audit if not audit.empty else pd.DataFrame(columns=["Timestamp", "TransactionID", "AccountID", "Analyst", "Decision", "Playbook_Action", "Transaction_Action", "Account_Action", "Operational_Effect", "Note"])
            st.download_button("Download audit_trail.csv", audit_export.to_csv(index=False).encode("utf-8"), "audit_trail.csv", "text/csv", use_container_width=True)
        with c3:
            actioned = report[report["Analyst_Decision"] != "Pending Review"].copy()
            st.download_button("Download actioned_cases_only.csv", actioned.to_csv(index=False).encode("utf-8"), "actioned_cases_only.csv", "text/csv", use_container_width=True)

        actions = pd.DataFrame([{"AccountID": k, "Account_Status": v} for k, v in st.session_state.account_actions.items()])
        if not actions.empty:
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            chart_wrapper("Account-Level Operational Status")
            st.dataframe(actions, use_container_width=True, hide_index=True, height=260)


# =========================================================
# RUN APP
# =========================================================
if not st.session_state.data_loaded:
    upload_gate()

# Run the clock refresh only after the dataset is fully loaded.
# This prevents the upload/analyze progress from restarting every second.
st_autorefresh(interval=1000, key="live_clock_refresh")

df = apply_decisions(st.session_state.df)
page = sidebar(df)

if page == "▦  Command Center":
    page_command_center(df)
elif page == "⌁  Live Monitoring":
    page_live_monitor(df)
elif page == "▣  Investigation Workspace":
    page_investigation_workspace(df)
elif page == "☷  Audit & Reports":
    page_audit_reports(df)
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# AI FRAUD INTELLIGENCE PLATFORM - FINAL BANK-STYLE VERSION
# =========================================================

st.set_page_config(
    page_title="AI Fraud Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS / DESIGN SYSTEM
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --bg:#F6F8FC;
    --card:#FFFFFF;
    --text:#071226;
    --muted:#64748B;
    --border:#E2E8F0;
    --soft:#EEF3F9;
    --navy:#06182A;
    --blue:#0B5BD3;
    --cyan:#12B8C8;
    --red:#EF4444;
    --orange:#F59E0B;
    --green:#16A34A;
    --purple:#7C3AED;
    --shadow:0 16px 38px rgba(15,23,42,.075);
    --shadow2:0 8px 22px rgba(15,23,42,.055);
}

html, body, [class*="css"]{font-family:'Inter',sans-serif !important;}
.stApp{background:var(--bg);color:var(--text);}
.block-container{
    padding-top:1.2rem !important;
    padding-left:2.05rem !important;
    padding-right:2.05rem !important;
    padding-bottom:3rem !important;
    max-width:1540px !important;
}
/* Keep Streamlit sidebar controls visible. Do not hide header/toolbar because the
   sidebar expand button lives there in recent Streamlit versions. */
#MainMenu, footer{visibility:hidden;}
header{visibility:visible !important;background:transparent !important;}
div[data-testid="stToolbar"]{visibility:visible !important;height:auto !important;position:relative !important;}
[data-testid="collapsedControl"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    z-index:9999999 !important;
    position:fixed !important;
    top:.65rem !important;
    left:.65rem !important;
    background:#FFFFFF !important;
    border:1px solid #CBD5E1 !important;
    border-radius:12px !important;
    box-shadow:0 10px 24px rgba(15,23,42,.18) !important;
}
button[kind="header"], button[data-testid="baseButton-header"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
}
section[data-testid="stSidebar"]{
    display:block !important;
    visibility:visible !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:radial-gradient(circle at top left,#17466F 0%,#081D33 38%,#020B16 100%) !important;
    border-right:1px solid rgba(255,255,255,.08);
}
section[data-testid="stSidebar"] > div{padding-top:1.25rem !important;}
section[data-testid="stSidebar"] *{color:#F8FAFC !important;}
section[data-testid="stSidebar"] .stRadio > label{display:none;}
section[data-testid="stSidebar"] div[role="radiogroup"] label{
    padding:.72rem .82rem !important;
    margin:.18rem 0 !important;
    border-radius:14px !important;
    min-height:44px;
    transition:all .18s ease;
    color:#DDE7F3 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(14,165,233,.14) !important;
    transform:translateX(2px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
    background:linear-gradient(135deg,#0B5BD3 0%,#07508F 100%) !important;
    box-shadow:0 12px 28px rgba(14,165,233,.24);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{
    font-weight:800 !important;
    font-size:14px !important;
}
.sidebar-brand{display:flex;gap:13px;align-items:center;margin:6px 2px 26px 2px;}
.brand-shield{width:54px;height:60px;border-radius:18px;border:2px solid rgba(226,232,240,.28);display:flex;align-items:center;justify-content:center;font-size:29px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 22px rgba(255,255,255,.05);}
.brand-title{font-size:21px;font-weight:900;line-height:1.16;letter-spacing:-.3px;}
.sidebar-pill{display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.075);border:1px solid rgba(255,255,255,.10);border-radius:16px;padding:12px 13px;margin-top:14px;}
.sidebar-user{display:flex;gap:10px;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10);border-radius:18px;padding:13px 12px;margin-top:24px;}
.avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(255,255,255,.25),rgba(255,255,255,.06));font-size:20px;}
.dot{width:8px;height:8px;border-radius:50%;background:#22C55E;display:inline-block;margin-right:8px;box-shadow:0 0 10px rgba(34,197,94,.8);}
.small-muted{font-size:12px;color:#90A4B9 !important;line-height:1.55;}
.badge-red,.badge-orange,.badge-green{color:white;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:900;}
.badge-red{background:#EF4444;}.badge-orange{background:#F59E0B;}.badge-green{background:#16A34A;}

/* Top */
.topbar{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;gap:18px;}
.page-title h1{margin:0;color:var(--text);font-weight:900;letter-spacing:-1px;font-size:35px;}
.page-title p{margin:7px 0 0 0;color:var(--muted);font-size:15px;font-weight:500;}
.top-actions{display:flex;gap:12px;align-items:center;}
.action-chip{background:#fff;border:1px solid var(--border);border-radius:13px;padding:12px 15px;color:#0F172A;font-weight:800;box-shadow:var(--shadow2);white-space:nowrap;}
.export-chip{background:linear-gradient(135deg,#0B5BD3,#1687FF);color:#fff;border-radius:13px;padding:12px 16px;font-weight:900;box-shadow:0 14px 28px rgba(11,91,211,.22);white-space:nowrap;}

/* Main cards */
.card{background:rgba(255,255,255,.96);border:1px solid var(--border);border-radius:22px;box-shadow:var(--shadow);padding:20px;margin-bottom:18px;transition:all .22s ease;}
.chart-header{background:rgba(255,255,255,.96);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow);padding:17px 20px;margin-bottom:16px;transition:all .22s ease;}
.chart-header:hover,.card:hover{box-shadow:0 20px 48px rgba(15,23,42,.10);}
.chart-title{display:flex;align-items:center;justify-content:space-between;color:#071226;font-weight:900;font-size:17px;gap:14px;}
.chart-sub{color:var(--muted);font-size:12px;font-weight:700;text-align:right;}
.kpi-card{position:relative;overflow:hidden;background:rgba(255,255,255,.97);border:1px solid var(--border);border-radius:18px;box-shadow:var(--shadow);padding:17px 18px;min-height:132px;transition:all .22s ease;}
.kpi-card:hover{transform:translateY(-4px);box-shadow:0 24px 55px rgba(15,23,42,.12);}
.kpi-card:after{content:"";position:absolute;right:-30px;top:-34px;width:86px;height:86px;background:radial-gradient(circle,rgba(14,165,233,.13),transparent 70%);}
.kpi-head{display:flex;align-items:center;justify-content:space-between;gap:10px;}
.kpi-label{font-size:13.5px;font-weight:900;color:#0F172A;}
.kpi-icon{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:inset 0 0 18px rgba(255,255,255,.55);}
.kpi-value{font-size:26px;font-weight:950;color:#071226;margin-top:10px;letter-spacing:-.6px;word-break:break-word;line-height:1.05;}
.kpi-foot{display:flex;justify-content:space-between;align-items:center;margin-top:16px;color:var(--muted);font-weight:750;font-size:12.5px;gap:10px;}
.kpi-decision .kpi-value{font-size:21px !important;letter-spacing:-.45px;line-height:1.08;}
.primary-kpi .kpi-card{min-height:158px;border-color:#CBD5E1;}
.primary-kpi .kpi-value{font-size:40px !important;}
.trend-up{color:#16A34A;font-weight:900;}.trend-red{color:#EF4444;font-weight:900;}.trend-neutral{color:#64748B;font-weight:900;}

.metric-mini{display:flex;gap:10px;align-items:center;border:1px solid var(--border);border-radius:16px;padding:12px 14px;background:#fff;box-shadow:var(--shadow2);margin-bottom:10px;transition:all .22s ease;}
.metric-mini:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(15,23,42,.09);}
.metric-dot{width:34px;height:34px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;flex:0 0 auto;}
.metric-text{font-weight:900;color:#0F172A;font-size:13.5px;}
.metric-number{margin-left:auto;font-weight:950;color:#0F172A;text-align:right;}

.status-badge{display:inline-block;border-radius:999px;padding:6px 11px;font-size:12px;font-weight:950;border:1px solid transparent;}
.status-escalated{background:#7F1D1D;color:white;border-color:#DC2626;}
.status-high{background:#FFF7ED;color:#EA580C;border-color:#FDBA74;}
.status-review{background:#FFFBEB;color:#D97706;border-color:#FDE68A;}
.status-safe{background:#ECFDF5;color:#16A34A;border-color:#A7F3D0;}

.alert-box{border-radius:18px;padding:16px 18px;margin-bottom:14px;font-weight:850;box-shadow:var(--shadow2);line-height:1.65;transition:all .22s ease;}
.alert-red{background:#FFF1F2;border:1px solid #FDA4AF;color:#9F1239;}
.alert-orange{background:#FFFBEB;border:1px solid #FDE68A;color:#92400E;}
.alert-green{background:#ECFDF5;border:1px solid #A7F3D0;color:#065F46;}
.table-hint{font-size:12px;font-weight:900;color:#0B5BD3;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:7px 12px;display:inline-block;margin:0 0 12px 0;}
.page-purpose{background:#FFFFFF;border:1px solid #E2E8F0;border-left:6px solid #0B5BD3;border-radius:18px;padding:14px 16px;margin:0 0 18px 0;box-shadow:0 8px 22px rgba(15,23,42,.045);color:#334155;font-size:13px;font-weight:750;line-height:1.65;}
.page-purpose b{color:#071226;}
.connected-workspace{border:1px solid #DDE6F0;border-radius:26px;background:linear-gradient(180deg,#FFFFFF 0%,#F7FAFF 100%);box-shadow:0 18px 45px rgba(15,23,42,.08);padding:18px;margin-top:8px;margin-bottom:24px;}
.analysis-block{border:1px solid #DDE6F0;border-radius:24px;background:linear-gradient(180deg,#FFFFFF 0%,#F8FBFF 100%);box-shadow:0 18px 44px rgba(15,23,42,.08);padding:18px;margin:18px 0 22px 0;}
.section-kicker{font-size:15px;font-weight:950;color:#071226;text-transform:uppercase;letter-spacing:.9px;margin:8px 0 12px 0;}
.soft-divider{height:1px;background:linear-gradient(90deg,transparent,#DDE6F0,transparent);margin:24px 0 18px 0;}
.section-gap{height:24px;}
.queue-search-note{font-size:12px;color:#64748B;font-weight:750;margin-top:-4px;margin-bottom:8px;}
.playbook-card{background:#F8FAFC;border:1px solid #DDE6F0;border-radius:16px;padding:13px 14px;margin-bottom:10px;}
.playbook-title{font-weight:950;color:#071226;font-size:14px;}
.playbook-sub{color:#64748B;font-size:12px;font-weight:750;margin-top:4px;line-height:1.55;}

.live-counter-card{background:linear-gradient(135deg,#FFFFFF 0%,#EEF7FF 100%);border:1px solid #BFDBFE;border-radius:22px;box-shadow:0 18px 42px rgba(11,91,211,.10);padding:18px 22px;margin:10px 0 16px 0;}
.live-counter-number{font-size:46px;font-weight:950;color:#071226;line-height:1;margin-top:8px;letter-spacing:-1.5px;}
.pipeline-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px;}
.pipeline-step{background:#fff;border:1px solid #E2E8F0;border-radius:18px;padding:16px;box-shadow:var(--shadow2);}
.step-num{width:30px;height:30px;border-radius:10px;background:#DBEAFE;color:#0B5BD3;display:flex;align-items:center;justify-content:center;font-weight:950;margin-bottom:10px;}
.step-title{font-weight:950;color:#071226;font-size:14px;}.step-sub{font-size:12px;color:#64748B;font-weight:700;margin-top:4px;line-height:1.5;}

/* Controls */
.stButton>button,.stDownloadButton>button{border-radius:13px !important;border:1px solid var(--border) !important;font-weight:850 !important;min-height:42px;box-shadow:var(--shadow2);transition:all .22s ease;}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#0B5BD3 !important;color:#0B5BD3 !important;transform:translateY(-1px);}
div[data-testid="stFileUploader"] section{border:1.5px dashed #C8D4E4;background:#fff;border-radius:22px;padding:28px;box-shadow:var(--shadow);}
div[data-testid="stDataFrame"]{border-radius:16px;overflow:visible !important;border:1px solid var(--border);box-shadow:var(--shadow2);}
/* Plotly and dataframe toolbars: hidden by default, visible on hover */
.js-plotly-plot .modebar{opacity:0 !important;visibility:hidden !important;transition:opacity .16s ease !important;}
.js-plotly-plot:hover .modebar{opacity:1 !important;visibility:visible !important;}
div[data-testid="stElementToolbar"]{opacity:0 !important;visibility:hidden !important;transition:opacity .16s ease !important;}
div[data-testid="stElementContainer"]:hover div[data-testid="stElementToolbar"],
div[data-testid="stDataFrame"]:hover ~ div[data-testid="stElementToolbar"],
div[data-testid="stDataFrame"]:hover div[data-testid="stElementToolbar"]{opacity:1 !important;visibility:visible !important;}
.stTabs [data-baseweb="tab-list"]{gap:14px;background:#EDF3FA;border-radius:16px;padding:8px;}
.stTabs [data-baseweb="tab"]{border-radius:13px;font-weight:850;color:#334155;min-height:44px;padding:10px 14px !important;}
.stTabs [aria-selected="true"]{background:#fff;color:#0B5BD3;box-shadow:var(--shadow2);min-height:48px;padding:12px 17px !important;border-radius:14px !important;}

/* Sidebar dataset button should stay visible without hover */
section[data-testid="stSidebar"] .stButton>button{
    background:#FFFFFF !important;
    color:#0B5BD3 !important;
    border:1px solid rgba(255,255,255,.85) !important;
    box-shadow:0 10px 24px rgba(0,0,0,.18) !important;
}
section[data-testid="stSidebar"] .stButton>button p,
section[data-testid="stSidebar"] .stButton>button span{
    color:#0B5BD3 !important;
    font-weight:900 !important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:#EFF6FF !important;
    border-color:#93C5FD !important;
    color:#07508F !important;
}

@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:1100px){
    .topbar{flex-direction:column}.page-title h1{font-size:30px}.block-container{padding-left:1rem !important;padding-right:1rem !important}.top-actions{flex-wrap:wrap}.pipeline-steps{grid-template-columns:1fr 1fr}.kpi-card{min-height:124px}
}


/* Compact professional controls */
.tools-panel{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin:8px 0 14px 0;box-shadow:0 8px 22px rgba(15,23,42,.045);}
.live-ticker{background:linear-gradient(135deg,#FFFFFF 0%,#F8FBFF 100%);border:1px solid #DDE6F0;border-radius:22px;padding:18px 20px;margin:12px 0 18px 0;box-shadow:0 18px 42px rgba(15,23,42,.075);}
.live-ticker-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:center;}
.live-metric-label{color:#64748B;font-size:12px;font-weight:900;letter-spacing:.7px;text-transform:uppercase;}
.live-counter-number{font-size:44px;font-weight:950;color:#071226;line-height:1;margin-top:8px;}
.live-event-strip{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:13px 14px;color:#0F172A;font-weight:850;}
.live-dot{width:10px;height:10px;border-radius:50%;display:inline-block;background:#22C55E;margin-right:8px;box-shadow:0 0 0 6px rgba(34,197,94,.13);}
@media(max-width:1100px){.live-ticker-grid{grid-template-columns:1fr;}}


.chart-header{min-height:64px;display:flex;align-items:center;}
.chart-title{width:100%;}
.chart-title .chart-sub:empty{display:none;}
.live-counter-card{max-width:100%;}

/* Final spacing polish */
.section-divider{height:2px;background:#CBD5E1;border-radius:999px;margin:28px 0 24px 0;box-shadow:0 1px 0 rgba(255,255,255,.55);}
.audit-tab-spacer{height:12px;}
.report-toolbar{display:flex;justify-content:space-between;align-items:center;gap:16px;background:#FFFFFF;border:1px solid #D6E0EC;border-radius:18px;padding:14px 16px;margin:10px 0 16px 0;box-shadow:0 10px 26px rgba(15,23,42,.055);}
.report-title{font-weight:950;color:#071226;font-size:16px;}
.report-sub{font-size:12px;font-weight:750;color:#64748B;margin-top:3px;}
.report-table-wrap div[data-testid="stDataFrame"]{border:1px solid #CBD5E1;box-shadow:0 14px 32px rgba(15,23,42,.07);}

/* Audit outputs cards */
.output-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:12px 0 18px 0;}
.output-card{background:#FFFFFF;border:1px solid #D6E0EC;border-radius:18px;padding:16px 17px;box-shadow:0 10px 26px rgba(15,23,42,.055);min-height:112px;}
.output-card-title{font-weight:950;color:#071226;font-size:14px;margin-bottom:6px;}
.output-card-sub{font-weight:750;color:#64748B;font-size:12px;line-height:1.55;}
.output-chip{display:inline-block;margin-top:10px;background:#EFF6FF;border:1px solid #BFDBFE;color:#0B5BD3;border-radius:999px;padding:5px 9px;font-size:11px;font-weight:950;}
@media(max-width:1100px){.output-grid{grid-template-columns:1fr;}}


/* SAFE MOBILE LIGHT MODE FIX */
html, body, [class*="css"] {
    color-scheme: light !important;
}
.stApp {
    background: #F6F8FC !important;
    color: #071226 !important;
}
.card,
.chart-header,
.kpi-card,
.metric-mini,
.playbook-card,
.live-counter-card,
.pipeline-step,
.report-toolbar,
.output-card,
div[data-testid="stDataFrame"],
div[data-baseweb="select"] > div,
input,
textarea {
    background-color: #FFFFFF !important;
    color: #071226 !important;
}
.stButton > button,
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #071226 !important;
    border-color: #D6E0EC !important;
}


/* =========================================================
   STRONG MOBILE DARK MODE FIX
   Forces Streamlit widgets to stay light on mobile browsers
   ========================================================= */
html, body, [class*="css"], .stApp {
    color-scheme: light !important;
    background: #F6F8FC !important;
    color: #071226 !important;
}

/* General widget surfaces */
div[data-testid="stAppViewContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="stForm"],
div[data-testid="stExpander"],
div[data-testid="stFileUploader"],
div[data-testid="stDataFrame"],
div[data-testid="stElementContainer"] {
    color-scheme: light !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button,
button[kind],
button[data-testid],
div[data-testid="stBaseButton-secondary"] button {
    background: #FFFFFF !important;
    color: #071226 !important;
    border: 1px solid #D6E0EC !important;
    box-shadow: 0 8px 22px rgba(15,23,42,.055) !important;
}

/* Button text */
.stButton > button *,
.stDownloadButton > button *,
button[kind] *,
button[data-testid] * {
    color: #071226 !important;
}

/* Inputs, text areas, number inputs */
input,
textarea,
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #FFFFFF !important;
    color: #071226 !important;
    -webkit-text-fill-color: #071226 !important;
    border-color: #D6E0EC !important;
}

/* Selectbox / multiselect */
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background: #FFFFFF !important;
    color: #071226 !important;
}

div[data-baseweb="select"] *,
div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
ul[role="listbox"] *,
li[role="option"] * {
    color: #071226 !important;
}

/* File uploader */
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] section *,
div[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploaderDropzone"] * {
    background: #FFFFFF !important;
    color: #071226 !important;
}

/* Tables / dataframes */
div[data-testid="stDataFrame"],
div[data-testid="stDataFrame"] *,
div[data-testid="stTable"],
div[data-testid="stTable"] * {
    color-scheme: light !important;
}

/* Streamlit dataframe canvas/table wrappers */
div[data-testid="stDataFrame"] [class*="row"],
div[data-testid="stDataFrame"] [class*="cell"],
div[data-testid="stDataFrame"] [class*="header"] {
    background-color: #FFFFFF !important;
    color: #071226 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] * {
    background: #FFFFFF !important;
    color: #071226 !important;
}

.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] * {
    background: #FFFFFF !important;
    color: #0B5BD3 !important;
}

/* Sliders */
div[data-testid="stSlider"] *,
div[data-baseweb="slider"] * {
    color: #071226 !important;
}

/* Alerts/messages */
div[data-testid="stAlert"],
div[data-testid="stAlert"] * {
    background-color: #DBEAFE !important;
    color: #07508F !important;
}

/* Keep custom dark sidebar dark by design */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] * {
    color-scheme: dark !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background:#FFFFFF !important;
    color:#0B5BD3 !important;
}
section[data-testid="stSidebar"] .stButton > button * {
    color:#0B5BD3 !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# MODEL AND DATA LOGIC
# =========================================================
@st.cache_resource
def load_assets():
    model = joblib.load("isolation_forest_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_assets()

required_columns = [
    "TransactionID", "AccountID", "TransactionAmount", "TransactionDate",
    "TransactionType", "Location", "DeviceID", "IP Address", "MerchantID",
    "Channel", "CustomerAge", "CustomerOccupation", "TransactionDuration",
    "LoginAttempts", "AccountBalance", "PreviousTransactionDate"
]

numerical_features = [
    "TransactionAmount", "CustomerAge", "TransactionDuration", "LoginAttempts",
    "AccountBalance", "TransactionHour", "TransactionDay", "TransactionMonth",
    "TransactionDayOfWeek", "TimeSincePreviousTransaction_Minutes",
    "Is_Night_Transaction", "Account_Avg_Amount", "Account_Amount_Deviation",
    "Amount_ZScore_By_Account", "Amount_To_Balance_Ratio",
    "Rapid_Transaction_Flag", "High_Amount_Flag", "High_Login_Attempts_Flag",
    "Rare_Location_Flag", "Rare_Device_Flag", "Rare_Merchant_Flag"
]

categorical_features = [
    "TransactionType", "Location", "DeviceID", "MerchantID", "Channel", "CustomerOccupation"
]


def init_state():
    defaults = {
        "data_loaded": False,
        "df": None,
        "current_page": "▦  Command Center",
        "selected_txn": None,
        "case_decisions": {},
        "audit_log": [],
        "live_count": 50,
        "monitoring_on": False,
        "live_manual_slider_version": 0,
        "last_loaded_at": None,
        "account_actions": {},
        "transaction_actions": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()


def read_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    if file.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    return None


def create_features(df):
    df = df.copy().dropna().drop_duplicates().reset_index(drop=True)
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["PreviousTransactionDate"] = pd.to_datetime(df["PreviousTransactionDate"])
    df["TransactionHour"] = df["TransactionDate"].dt.hour
    df["TransactionDay"] = df["TransactionDate"].dt.day
    df["TransactionMonth"] = df["TransactionDate"].dt.month
    df["TransactionDayOfWeek"] = df["TransactionDate"].dt.dayofweek
    df["TimeSincePreviousTransaction_Minutes"] = (
        df["TransactionDate"] - df["PreviousTransactionDate"]
    ).dt.total_seconds() / 60
    df["Is_Night_Transaction"] = df["TransactionHour"].apply(lambda x: 1 if x < 6 or x > 22 else 0)

    avg = df.groupby("AccountID")["TransactionAmount"].transform("mean")
    std = df.groupby("AccountID")["TransactionAmount"].transform("std").fillna(0)
    df["Account_Avg_Amount"] = avg
    df["Account_Amount_Deviation"] = df["TransactionAmount"] - avg
    df["Amount_ZScore_By_Account"] = (df["TransactionAmount"] - avg) / (std + 1e-6)
    df["Amount_To_Balance_Ratio"] = df["TransactionAmount"] / (df["AccountBalance"] + 1e-6)
    df["Rapid_Transaction_Flag"] = df["TimeSincePreviousTransaction_Minutes"].apply(lambda x: 1 if x < 5 else 0)
    amount_95 = df["TransactionAmount"].quantile(0.95)
    df["High_Amount_Flag"] = df["TransactionAmount"].apply(lambda x: 1 if x > amount_95 else 0)
    df["High_Login_Attempts_Flag"] = df["LoginAttempts"].apply(lambda x: 1 if x >= 3 else 0)
    df["Rare_Location_Flag"] = df.groupby(["AccountID", "Location"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    df["Rare_Device_Flag"] = df.groupby(["AccountID", "DeviceID"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    df["Rare_Merchant_Flag"] = df.groupby(["AccountID", "MerchantID"])["TransactionID"].transform("count").apply(lambda x: 1 if x == 1 else 0)
    return df


def risk_category(score):
    if score < 30:
        return "Low"
    if score < 60:
        return "Medium"
    return "High"


def case_status(score):
    if score >= 80:
        return "Escalated"
    if score >= 60:
        return "High Priority"
    if score >= 30:
        return "Needs Review"
    return "Safe"


def recommended_action(row):
    if row["Case_Status"] == "Escalated":
        return "Temporarily hold transaction and escalate to fraud investigation team."
    if row["Case_Status"] == "High Priority":
        return "Verify customer activity and assign to analyst review queue."
    if row["Case_Status"] == "Needs Review":
        return "Monitor account activity and review related transactions."
    return "No immediate action required."


def risk_reason(row):
    reasons = []
    if row["High_Amount_Flag"] == 1: reasons.append("High transaction amount")
    if row["Rapid_Transaction_Flag"] == 1: reasons.append("Rapid transaction behavior")
    if row["Is_Night_Transaction"] == 1: reasons.append("Night-time activity")
    if row["High_Login_Attempts_Flag"] == 1: reasons.append("Multiple login attempts")
    if row["Rare_Location_Flag"] == 1: reasons.append("Unusual location")
    if row["Rare_Device_Flag"] == 1: reasons.append("Unusual device")
    if row["Rare_Merchant_Flag"] == 1: reasons.append("Rare merchant")
    if row["Anomaly_Flag"] == 1: reasons.append("ML anomaly detected")
    return " | ".join(reasons) if reasons else "Normal behavior"


def case_priority_score(row):
    triggered = (
        int(row.get("High_Amount_Flag", 0)) + int(row.get("Rapid_Transaction_Flag", 0)) +
        int(row.get("Is_Night_Transaction", 0)) + int(row.get("High_Login_Attempts_Flag", 0)) +
        int(row.get("Rare_Location_Flag", 0)) + int(row.get("Rare_Device_Flag", 0)) +
        int(row.get("Rare_Merchant_Flag", 0)) + int(row.get("Anomaly_Flag", 0))
    )
    return round((float(row["Final_Risk_Score"]) * 0.8) + (triggered * 2.5), 2)


@st.cache_data(show_spinner=False)
def process_data(raw_df):
    df = create_features(raw_df)
    X = df[numerical_features + categorical_features].copy()
    Xp = preprocessor.transform(X)
    pred = model.predict(Xp)
    score = model.decision_function(Xp)
    df["Anomaly_Flag"] = np.where(pred == -1, 1, 0)
    raw_risk = -score
    df["ML_Risk_Score"] = ((raw_risk - raw_risk.min()) / (raw_risk.max() - raw_risk.min() + 1e-6)) * 100
    df["Behavioral_Risk_Score"] = 0
    df["Behavioral_Risk_Score"] += df["High_Amount_Flag"] * 20
    df["Behavioral_Risk_Score"] += df["Rapid_Transaction_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Is_Night_Transaction"] * 10
    df["Behavioral_Risk_Score"] += df["High_Login_Attempts_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Location_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Device_Flag"] * 15
    df["Behavioral_Risk_Score"] += df["Rare_Merchant_Flag"] * 10
    df["Behavioral_Risk_Score"] = df["Behavioral_Risk_Score"].clip(0, 100)
    df["Final_Risk_Score"] = df["ML_Risk_Score"] * 0.6 + df["Behavioral_Risk_Score"] * 0.4
    df["Risk_Category"] = df["Final_Risk_Score"].apply(risk_category)
    df["Case_Status"] = df["Final_Risk_Score"].apply(case_status)
    df["Fraud_Probability"] = df["Final_Risk_Score"] / 100
    df["Fraud_Prediction"] = df["Risk_Category"].apply(lambda x: 1 if x == "High" else 0)
    df["Risk_Reason"] = df.apply(risk_reason, axis=1)
    df["Recommended_Action"] = df.apply(recommended_action, axis=1)
    df["Case_Priority_Score"] = df.apply(case_priority_score, axis=1)
    return df


def apply_decisions(df):
    df = df.copy()
    df["Analyst_Decision"] = df["TransactionID"].astype(str).map(st.session_state.case_decisions).fillna("Pending Review")
    return df


def log_action(txn, action, note="", row=None, playbook_action=None):
    txn = str(txn)
    st.session_state.case_decisions[txn] = action
    account_id = ""
    if row is not None:
        account_id = str(row.get("AccountID", ""))

    txn_effect = "Recorded analyst decision"
    if playbook_action == "Hold transaction and verify customer":
        st.session_state.transaction_actions[txn] = "Transaction Held - Customer Verification Required"
        txn_effect = "Transaction held and customer verification requested"
    elif playbook_action == "Temporarily block account":
        st.session_state.transaction_actions[txn] = "Transaction Held"
        if account_id:
            st.session_state.account_actions[account_id] = "Temporarily Blocked"
        txn_effect = "Transaction held and account temporarily blocked"
    elif playbook_action == "Escalate to senior fraud investigator":
        st.session_state.transaction_actions[txn] = "Escalated to Senior Investigator"
        txn_effect = "Case escalated to senior fraud investigator"
    elif playbook_action == "Request customer confirmation":
        st.session_state.transaction_actions[txn] = "Customer Confirmation Requested"
        txn_effect = "Customer confirmation requested before release"
    elif playbook_action == "Release transaction / no restriction":
        st.session_state.transaction_actions[txn] = "Released"
        txn_effect = "Transaction released with no account restriction"
    elif playbook_action == "Close as false positive":
        st.session_state.transaction_actions[txn] = "Closed as False Positive"
        txn_effect = "Alert closed as false positive"

    if action == "Confirmed Fraud":
        st.session_state.transaction_actions[txn] = "Transaction Held - Confirmed Fraud"
        if account_id:
            st.session_state.account_actions[account_id] = "Temporarily Blocked"
        txn_effect = "Confirmed fraud: transaction held, account blocked, case escalated"
    elif action == "False Positive":
        st.session_state.transaction_actions[txn] = "Released - False Positive"
        txn_effect = "False positive: alert closed and transaction released"
    elif action == "Marked Safe":
        st.session_state.transaction_actions[txn] = "Cleared"
        if account_id and st.session_state.account_actions.get(account_id) == "Temporarily Blocked":
            st.session_state.account_actions[account_id] = "Active"
        txn_effect = "Marked safe: case closed with no restriction"
    elif action == "Escalated":
        st.session_state.transaction_actions[txn] = "Escalated"
        txn_effect = "Case escalated for further investigation"
    elif action == "Under Investigation":
        st.session_state.transaction_actions[txn] = "Under Review"
        txn_effect = "Case remains open under investigation"
    elif action == "Reviewed":
        if txn not in st.session_state.transaction_actions:
            st.session_state.transaction_actions[txn] = "Reviewed"
        txn_effect = txn_effect if playbook_action else "Case reviewed by analyst"

    final_account_status = st.session_state.account_actions.get(account_id, "Active") if account_id else ""
    st.session_state.audit_log.append({
        "Timestamp": jordan_now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionID": txn,
        "AccountID": account_id,
        "Analyst": "Risk Analyst",
        "Decision": action,
        "Playbook_Action": playbook_action if playbook_action else "No playbook action selected",
        "Transaction_Action": st.session_state.transaction_actions.get(txn, "No action yet"),
        "Account_Action": final_account_status,
        "Operational_Effect": txn_effect,
        "Note": note,
    })
    try:
        st.toast(f"Action saved: {txn_effect}", icon="✅")
    except Exception:
        st.success(f"Action saved: {txn_effect}")


def open_case(txn):
    st.session_state.selected_txn = txn
    st.session_state.current_page = "▣  Investigation Workspace"
    st.rerun()

# =========================================================
# UI HELPERS
# =========================================================
def safe_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def status_class(status):
    if status == "Escalated": return "status-escalated"
    if status == "High Priority": return "status-high"
    if status == "Needs Review": return "status-review"
    return "status-safe"


def badge_class(value):
    if value == 0: return "badge-green"
    if value < 25: return "badge-orange"
    return "badge-red"



def jordan_now():
    return datetime.now(ZoneInfo("Asia/Amman"))


def render_topbar(title, subtitle, show_export=True, df=None):
    now = jordan_now()
    today_text = now.strftime("%b %d, %Y")
    time_text = now.strftime("%I:%M:%S %p")
    st.markdown(f"""
    <div class="topbar">
        <div class="page-title">
            <h1>{safe_html(title)}</h1>
            <p>{safe_html(subtitle)}</p>
        </div>
        <div class="top-actions">
            <div class="action-chip">🗓️ {today_text}<br>🕒 {time_text}<br>Amman, Jordan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(label, value, icon, note="Today", trend="", tone="blue", primary=False):
    colors = {
        "blue": ("#DBEAFE", "#0B5BD3"),
        "orange": ("#FFEDD5", "#F97316"),
        "red": ("#FEE2E2", "#EF4444"),
        "green": ("#DCFCE7", "#16A34A"),
        "cyan": ("#CFFAFE", "#0891B2"),
        "navy": ("#E0E7FF", "#0F2D5C"),
        "purple": ("#EDE9FE", "#7C3AED"),
    }
    bg, fg = colors.get(tone, colors["blue"])
    trend_class = "trend-neutral"
    if "↑" in str(trend) or "+" in str(trend): trend_class = "trend-up"
    if "↓" in str(trend) or "Critical" in str(trend) or "Urgent" in str(trend) or tone == "red": trend_class = "trend-red"
    extra = "kpi-decision" if label in ["Decision", "Account Status", "Txn Action"] else ""
    wrapper = "primary-kpi" if primary else ""
    st.markdown(f"""
    <div class="{wrapper}">
        <div class="kpi-card {extra}">
            <div class="kpi-head">
                <div class="kpi-label">{safe_html(label)}</div>
                <div class="kpi-icon" style="background:{bg};color:{fg};">{icon}</div>
            </div>
            <div class="kpi-value">{safe_html(value)}</div>
            <div class="kpi-foot"><span>{safe_html(note)}</span><span class="{trend_class}">{safe_html(trend)}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def chart_wrapper(title, subtitle=""):
    st.markdown(f"""
    <div class="chart-header">
        <div class="chart-title"><span>{safe_html(title)}</span><span class="chart-sub">{safe_html(subtitle)}</span></div>
    </div>
    """, unsafe_allow_html=True)


def end_chart_wrapper():
    # Kept for compatibility. No closing HTML is needed because chart headers are self-contained.
    return None


def clean_fig(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=8, b=8),
        font=dict(family="Inter", color="#071226", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DDE6F0")
    fig.update_yaxes(showgrid=True, gridcolor="#EEF3F9", zeroline=False, linecolor="#DDE6F0")
    try:
        fig.update_traces(hovertemplate=None)
    except Exception:
        pass
    return fig


def chart_config(filename="fraud_chart"):
    # Plotly toolbar appears only on hover, matching professional dashboard behavior.
    return {
        "displayModeBar": "hover",
        "displaylogo": False,
        "responsive": True,
        "scrollZoom": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d", "toggleSpikelines"],
        "modeBarButtonsToAdd": ["drawline", "eraseshape"],
        "toImageButtonOptions": {"format": "png", "filename": filename, "height": 900, "width": 1400, "scale": 2},
    }


def gauge_fig(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value),
        number={"font": {"size": 30, "color": "#071226"}},
        gauge={
            "axis": {"range": [0, 100], "tickvals": [0, 100], "tickfont": {"size": 11}},
            "bar": {"color": "#071A2D", "thickness": 0.16},
            "bgcolor": "#E5E7EB",
            "borderwidth": 0,
            "steps": [{"range": [0, value], "color": "#12B8C8"}],
            "threshold": {"line": {"color": "#071A2D", "width": 4}, "thickness": 0.75, "value": value},
        },
    ))
    fig.update_layout(height=118, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def sidebar(df=None):
    open_cases = 0
    critical = 0
    reviewed = 0
    if df is not None:
        active = df[df["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"]) & df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])]
        open_cases = len(active)
        critical = int((active["Case_Status"] == "Escalated").sum())
        reviewed = int((df["Analyst_Decision"] != "Pending Review").sum())

    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <div class="brand-shield">🛡️</div>
        <div class="brand-title">AI Fraud<br>Intelligence<br>Platform</div>
    </div>
    """, unsafe_allow_html=True)

    pages = ["▦  Command Center", "⌁  Live Monitoring", "▣  Investigation Workspace", "☷  Audit & Reports"]
    current = st.session_state.current_page if st.session_state.current_page in pages else pages[0]
    page = st.sidebar.radio("Navigation", pages, index=pages.index(current))
    st.session_state.current_page = page

    jordan_time = jordan_now()
    if "session_started_at" not in st.session_state:
        st.session_state.session_started_at = datetime.now().timestamp()
    runtime_seconds = max(0, int(datetime.now().timestamp() - st.session_state.session_started_at))
    runtime_h = runtime_seconds // 3600
    runtime_m = (runtime_seconds % 3600) // 60
    runtime_s = runtime_seconds % 60

    st.sidebar.markdown(f"""
    <div class="sidebar-pill"><span>Open Queue</span><span class="{badge_class(open_cases)}">{open_cases}</span></div>
    <div class="sidebar-pill"><span>Critical</span><span class="{badge_class(critical)}">{critical}</span></div>
    <div class="sidebar-user"><div class="avatar">👤</div><div><b>Risk Analyst</b><br><span class="small-muted">Fraud Operations</span></div></div>
    <div style="margin-top:18px" class="small-muted"><span class="dot"></span>Last Updated<br>{jordan_time.strftime('%b %d, %Y %I:%M:%S %p')}<br>Reviewed cases: {reviewed}<br><br>System Runtime<br>{runtime_h:02d}h {runtime_m:02d}m {runtime_s:02d}s</div>
    """, unsafe_allow_html=True)

    if df is not None:
        if st.sidebar.button("Change Dataset", use_container_width=True):
            st.session_state.data_loaded = False
            st.session_state.df = None
            st.session_state.selected_txn = None
            st.session_state.current_page = "▦  Command Center"
            st.rerun()
    return page


def alert_panel(df):
    critical = df[(df["Case_Status"] == "Escalated") & (df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))].sort_values("Final_Risk_Score", ascending=False)
    high = df[(df["Case_Status"] == "High Priority") & (df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))].sort_values("Final_Risk_Score", ascending=False)
    if not critical.empty:
        row = critical.iloc[0]
        st.markdown(f'<div class="alert-box alert-red">🚨 Critical alert detected — Transaction {safe_html(row["TransactionID"])} | Risk Score {row["Final_Risk_Score"]:.2f} | {safe_html(row["Risk_Reason"])}</div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.45, 1.45, 4.1])
        if c1.button("Open Critical Case", use_container_width=True): open_case(row["TransactionID"])
        if c2.button("Mark Reviewed", use_container_width=True):
            log_action(row["TransactionID"], "Reviewed", "Reviewed from alert panel", row)
            st.rerun()
    elif not high.empty:
        row = high.iloc[0]
        st.markdown(f'<div class="alert-box alert-orange">⚠️ High priority case — Transaction {safe_html(row["TransactionID"])} | Risk Score {row["Final_Risk_Score"]:.2f} | {safe_html(row["Risk_Reason"])}</div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.45, 1.45, 4.1])
        if c1.button("Open High Risk Case", use_container_width=True): open_case(row["TransactionID"])
        if c2.button("Mark Reviewed", use_container_width=True):
            log_action(row["TransactionID"], "Reviewed", "Reviewed from alert panel", row)
            st.rerun()
    else:
        st.markdown('<div class="alert-box alert-green">✅ No open critical alerts detected.</div>', unsafe_allow_html=True)


def filtered_df(df, key_prefix="main"):
    with st.expander("Filters", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        statuses = c1.multiselect("Case Status", sorted(df["Case_Status"].unique()), default=sorted(df["Case_Status"].unique()), key=f"{key_prefix}_status")
        channels = c2.multiselect("Channel", sorted(df["Channel"].astype(str).unique()), default=sorted(df["Channel"].astype(str).unique()), key=f"{key_prefix}_channel")
        locations = c3.multiselect("Location", sorted(df["Location"].astype(str).unique()), default=sorted(df["Location"].astype(str).unique()), key=f"{key_prefix}_location")
        risk_range = c4.slider("Risk Score", 0, 100, (0, 100), key=f"{key_prefix}_risk")
    return df[df["Case_Status"].isin(statuses) & df["Channel"].astype(str).isin(channels) & df["Location"].astype(str).isin(locations) & df["Final_Risk_Score"].between(risk_range[0], risk_range[1])].copy()



def interactive_table(data, key, filename, height=420, selectable=True, default_columns=None, max_default_rows=None, controls_mode="hidden", highlight_txn=None):
    """Reusable analyst table with optional popover customization controls."""
    table_df = data.copy()
    if default_columns is None:
        default_columns = list(table_df.columns)
    default_columns = [c for c in default_columns if c in table_df.columns]

    visible_cols = default_columns if default_columns else list(table_df.columns)
    row_limit = min(max_default_rows or len(table_df), len(table_df)) if len(table_df) else 1

    if controls_mode == "customize":
        if hasattr(st, "popover"):
            controls = st.popover("Customize Table")
        else:
            controls = st.expander("Customize Table", expanded=False)
        with controls:
            visible_cols = st.multiselect(
                "Visible columns",
                list(table_df.columns),
                default=default_columns,
                key=f"{key}_visible_cols",
            )
            if not visible_cols:
                visible_cols = default_columns if default_columns else list(table_df.columns)
            row_limit = st.number_input(
                "Rows to show",
                min_value=1,
                max_value=max(len(table_df), 1),
                value=max(row_limit, 1),
                step=1,
                key=f"{key}_row_limit",
            )
            st.download_button(
                "Download",
                table_df[visible_cols].head(int(row_limit)).to_csv(index=False).encode("utf-8"),
                filename,
                "text/csv",
                use_container_width=True,
                key=f"{key}_download",
            )

    shown = table_df[visible_cols].head(int(row_limit)).copy()
    display_data = shown
    if highlight_txn is not None and "TransactionID" in shown.columns:
        highlight_value = str(highlight_txn)
        def _highlight_selected(row):
            is_selected = str(row.get("TransactionID", "")) == highlight_value
            return [
                "background-color: #EAF3FF; color: #071226; font-weight: 900; border-top: 2px solid #0B5BD3; border-bottom: 2px solid #0B5BD3;"
                if is_selected else "" for _ in row
            ]
        display_data = shown.style.apply(_highlight_selected, axis=1)
    event = st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
        height=height,
        on_select="rerun" if selectable else "ignore",
        selection_mode="single-row" if selectable else "multi-row",
        key=f"{key}_df",
    )
    return event, shown


def report_table(data, key, filename, height=560):
    """Clean final report table without Table options, with direct CSV export."""
    st.markdown('<div class="report-table-wrap">', unsafe_allow_html=True)
    st.dataframe(data, use_container_width=True, hide_index=True, height=height, key=key)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button(
        "Download Final Power BI CSV",
        data.to_csv(index=False).encode("utf-8"),
        filename,
        "text/csv",
        use_container_width=True,
        key=f"{key}_download",
    )


# =========================================================
# UPLOAD GATE
# =========================================================
def upload_gate():
    sidebar(None)
    render_topbar("AI Fraud Intelligence Platform", "Upload a bank transaction dataset to start operational fraud monitoring", show_export=False)
    st.markdown("""
    <div class="card" style="padding:34px;">
        <div style="font-size:28px;font-weight:950;color:#071226;margin-bottom:8px;">Secure Dataset Intake</div>
        <div style="color:#64748B;font-weight:750;margin-bottom:18px;line-height:1.8;">The system validates required columns, generates behavioral indicators, applies the Isolation Forest model, and opens the Command Center automatically.</div>
        <div class="pipeline-steps">
            <div class="pipeline-step"><div class="step-num">1</div><div class="step-title">Upload</div><div class="step-sub">CSV or Excel transaction dataset</div></div>
            <div class="pipeline-step"><div class="step-num">2</div><div class="step-title">Validate</div><div class="step-sub">Required banking columns check</div></div>
            <div class="pipeline-step"><div class="step-num">3</div><div class="step-title">Analyze</div><div class="step-sub">Feature engineering + ML risk scoring</div></div>
            <div class="pipeline-step"><div class="step-num">4</div><div class="step-title">Investigate</div><div class="step-sub">Command center and case workflow</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose transaction file", type=["csv", "xlsx", "xls"])
    if uploaded_file is None:
        st.stop()
    raw_df = read_file(uploaded_file)
    if raw_df is None:
        st.error("Unsupported file format.")
        st.stop()
    missing = [c for c in required_columns if c not in raw_df.columns]
    if missing:
        st.error(f"Dataset validation failed. Missing columns: {missing}")
        st.stop()

    progress = st.progress(0)
    status = st.empty()
    loading_steps = [
        "Validating transaction structure...",
        "Cleaning missing and duplicate records...",
        "Generating behavioral fraud indicators...",
        "Applying anomaly detection model...",
        "Calculating final risk scores...",
        "Preparing banking operations dashboard...",
    ]
    for i, msg in enumerate(loading_steps):
        status.info(msg)
        progress.progress(int(((i + 1) / len(loading_steps)) * 100))
        time.sleep(0.25)
    st.session_state.df = apply_decisions(process_data(raw_df))
    st.session_state.live_count = min(50, len(st.session_state.df))
    st.session_state.data_loaded = True
    st.session_state.last_loaded_at = jordan_now().strftime("%Y-%m-%d %H:%M:%S")
    st.success("Dataset analyzed successfully. Opening Command Center...")
    time.sleep(0.5)
    st.rerun()

# =========================================================
# CASE / ACTION WORKFLOW
# =========================================================
def render_action_playbook(selected, note_key="case_note"):
    current_account_action = st.session_state.account_actions.get(str(selected["AccountID"]), "Active")
    current_txn_action = st.session_state.transaction_actions.get(str(selected["TransactionID"]), "No action yet")
    st.markdown(f"""
    <div class="playbook-card">
        <div class="playbook-title">Operational Action Status</div>
        <div class="playbook-sub">Transaction: <b>{safe_html(current_txn_action)}</b> · Account: <b>{safe_html(current_account_action)}</b></div>
    </div>
    """, unsafe_allow_html=True)
    playbook = st.selectbox(
        "Fraud Playbook Action",
        [
            "Hold transaction and verify customer",
            "Temporarily block account",
            "Escalate to senior fraud investigator",
            "Request customer confirmation",
            "Release transaction / no restriction",
            "Close as false positive",
        ],
        key=f"playbook_{selected['TransactionID']}",
    )
    note = st.text_area("Analyst Note", placeholder="Write investigation note...", height=105, key=note_key)
    b1, b2, b3 = st.columns(3)
    if b1.button("Reviewed", use_container_width=True, key=f"rev_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Reviewed", note, selected, playbook); st.rerun()
    if b2.button("Under Investigation", use_container_width=True, key=f"und_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Under Investigation", note, selected, playbook); st.rerun()
    if b3.button("Escalate", use_container_width=True, key=f"esc_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Escalated", note, selected, playbook); st.rerun()
    b4, b5, b6 = st.columns(3)
    if b4.button("Mark Safe", use_container_width=True, key=f"safe_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Marked Safe", note, selected, playbook); st.rerun()
    if b5.button("False Positive", use_container_width=True, key=f"fp_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "False Positive", note, selected, playbook); st.rerun()
    if b6.button("Confirmed Fraud", use_container_width=True, key=f"fraud_{selected['TransactionID']}"):
        log_action(selected["TransactionID"], "Confirmed Fraud", note, selected, playbook); st.rerun()


def render_case_block(df, selected):
    account_df = df[df["AccountID"] == selected["AccountID"]].copy()
    st.markdown('<div class="soft-divider"></div><div class="section-kicker">Selected Case Study</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:18px;">
        <div>
            <div style="font-size:13px;font-weight:950;color:#64748B;text-transform:uppercase;letter-spacing:.7px;">Transaction Case</div>
            <div style="font-size:28px;font-weight:950;color:#071226;line-height:1.15;margin-top:4px;">{safe_html(selected['TransactionID'])}</div>
            <div style="font-size:14px;color:#64748B;font-weight:800;margin-top:4px;">Account {safe_html(selected['AccountID'])} · {safe_html(selected['Channel'])} · {safe_html(selected['Location'])}</div>
        </div>
        <div style="text-align:right;">
            <div class="status-badge {status_class(selected['Case_Status'])}" style="font-size:13px;padding:7px 13px;">{safe_html(selected['Case_Status'])}</div>
            <div style="font-size:12px;color:#64748B;font-weight:850;margin-top:9px;">Analyst Decision: {safe_html(selected['Analyst_Decision'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Risk Score", f"{selected['Final_Risk_Score']:.2f}", "◌", "Final score", "", "red")
    with k2: kpi_card("Priority Score", f"{selected['Case_Priority_Score']:.2f}", "⇧", "Queue ranking", "", "orange")
    with k3: kpi_card("Amount", f"{selected['TransactionAmount']:,.2f}", "$", "Transaction value", "", "blue")
    with k4:
        current_txn_action = st.session_state.transaction_actions.get(str(selected["TransactionID"]), "No action yet")
        kpi_card("Txn Action", current_txn_action, "⚙", "Operational", "", "green")

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, .85])
    with left:
        chart_wrapper("Risk Explanation", "Why this case was prioritized")
        st.markdown(f'<div class="alert-box alert-orange"><b>Risk Reason</b><br>{safe_html(selected["Risk_Reason"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="playbook-card"><div class="playbook-title">Recommended Next Action</div><div class="playbook-sub">{safe_html(selected["Recommended_Action"])}</div></div>', unsafe_allow_html=True)
        account_status = st.session_state.account_actions.get(str(selected["AccountID"]), "Active")
        p1, p2, p3 = st.columns(3)
        with p1: kpi_card("Account Txns", f"{len(account_df):,}", "▣", "History", "", "blue")
        with p2: kpi_card("Avg Account Risk", f"{account_df['Final_Risk_Score'].mean():.2f}", "◌", "Account", "", "cyan")
        with p3: kpi_card("Account Status", account_status, "🛡", "Current action", "", "green" if account_status == "Active" else "red")
        trend = account_df.sort_values("TransactionDate")
        fig = px.line(trend, x="TransactionDate", y="Final_Risk_Score", markers=True, color_discrete_sequence=["#0B5BD3"])
        fig.update_yaxes(range=[0, 100], title="Risk")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 250), use_container_width=True, config=chart_config("account_risk_profile"))
    with right:
        chart_wrapper("Triggered Risk Evidence", "Behavioral + ML indicators")
        indicators = {
            "High Amount": selected["High_Amount_Flag"],
            "Rapid Transaction": selected["Rapid_Transaction_Flag"],
            "Night Activity": selected["Is_Night_Transaction"],
            "Login Risk": selected["High_Login_Attempts_Flag"],
            "Rare Location": selected["Rare_Location_Flag"],
            "Rare Device": selected["Rare_Device_Flag"],
            "Rare Merchant": selected["Rare_Merchant_Flag"],
            "ML Anomaly": selected["Anomaly_Flag"],
        }
        for name, val in indicators.items():
            color = "#EF4444" if val == 1 else "#16A34A"
            label = "Triggered" if val == 1 else "Normal"
            st.markdown(f'<div class="metric-mini"><div class="metric-dot" style="background:{color}14;color:{color};">{"!" if val == 1 else "✓"}</div><div class="metric-text">{safe_html(name)}</div><div class="metric-number" style="color:{color};">{safe_html(label)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-divider"></div><div class="section-kicker">Decision & Action Workflow</div>', unsafe_allow_html=True)
    ac1, ac2 = st.columns([1.05, .95])
    with ac1:
        chart_wrapper("Analyst Decision Panel", "Choose decision and operational action")
        render_action_playbook(selected, note_key=f"note_{selected['TransactionID']}")
    with ac2:
        chart_wrapper("Case Timeline", "Decision trace")
        timeline_rows = [
            ("Dataset uploaded", st.session_state.get("last_loaded_at") or "Current session"),
            ("Risk score generated", f"{selected['Final_Risk_Score']:.2f}"),
            ("Priority score", f"{selected['Case_Priority_Score']:.2f}"),
            ("System case status", selected["Case_Status"]),
            ("Analyst decision", selected["Analyst_Decision"]),
            ("Operational effect", st.session_state.transaction_actions.get(str(selected["TransactionID"]), "Waiting for analyst action")),
        ]
        for title, value in timeline_rows:
            st.markdown(f'<div class="metric-mini"><div class="metric-dot" style="background:#DBEAFE;color:#0B5BD3;">•</div><div class="metric-text">{safe_html(title)}</div><div class="metric-number" style="font-size:12px;max-width:52%;text-align:right;">{safe_html(value)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    chart_wrapper("Connected Account Transactions", "Same account history")
    account_show = account_df[["TransactionID","TransactionDate","TransactionAmount","TransactionType","Location","Channel","Final_Risk_Score","Case_Status","Analyst_Decision","Risk_Reason"]].sort_values("TransactionDate", ascending=False)
    event_acc, shown_acc = interactive_table(account_show, f"account_txns_{selected['TransactionID']}", "connected_account_transactions.csv", height=340, selectable=True, default_columns=["TransactionID","TransactionDate","TransactionAmount","TransactionType","Location","Channel","Final_Risk_Score","Case_Status","Analyst_Decision"], max_default_rows=min(len(account_show), 20) if len(account_show) else 1, highlight_txn=selected["TransactionID"])
    if event_acc.selection.rows:
        txn_acc = shown_acc.iloc[event_acc.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn_acc
        st.rerun()

# =========================================================
# PAGES
# =========================================================
def page_command_center(df):
    render_topbar("Command Center", "Real-time overview of fraud risk and operations", show_export=False)

    open_cases = df[
        df["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"]) &
        df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])
    ].copy()
    escalated = int((open_cases["Case_Status"] == "Escalated").sum())
    flagged = int((df["Risk_Category"] == "High").sum())
    avg_risk = float(df["Final_Risk_Score"].mean())
    pending = int((df["Analyst_Decision"] == "Pending Review").sum())
    handled = int((df["Analyst_Decision"] != "Pending Review").sum())

    # =====================================================
    # 1) OPERATIONS SNAPSHOT — first thing the analyst sees
    # =====================================================
    st.markdown('<div class="section-kicker">Operations Snapshot</div>', unsafe_allow_html=True)
    a, b, c, d, e = st.columns(5)
    with a:
        kpi_card("Total Transactions", f"{len(df):,}", "▣", "Uploaded", "Active", "blue")
    with b:
        kpi_card("Flagged Transactions", f"{flagged:,}", "⚑", "High risk", "Review", "orange")
    with c:
        kpi_card("Escalated Cases", f"{escalated:,}", "⇧", "Critical queue", "Urgent" if escalated else "Stable", "red")
    with d:
        kpi_card("Avg Risk Score", f"{avg_risk:.1f}", "◌", "Overall risk", "Score", "cyan")
    with e:
        decision_text = "Pending Review" if pending else "All Clear"
        kpi_card("Decision", decision_text, "✓", "Workflow", f"{handled:,} handled", "green" if not pending else "orange")

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

    # =====================================================
    # 2) MAIN RISK OVERVIEW — chart row directly under KPIs
    # =====================================================
    left, right = st.columns([1.08, .92])
    with left:
        chart_wrapper("Risk Score Trend")
        daily = df.copy()
        daily["Date"] = daily["TransactionDate"].dt.date
        trend = daily.groupby("Date", as_index=False)["Final_Risk_Score"].mean().tail(7)
        fig = px.line(
            trend,
            x="Date",
            y="Final_Risk_Score",
            markers=True,
            text=trend["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0B5BD3"],
        )
        fig.update_traces(line=dict(width=3.8), marker=dict(size=9), textposition="top center")
        fig.update_yaxes(range=[0, 100], title="")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 340), use_container_width=True, config=chart_config("risk_score_trend"))

    with right:
        chart_wrapper("Case Status Distribution")
        status = df["Case_Status"].value_counts().reset_index()
        status.columns = ["Case_Status", "Count"]
        color_map = {
            "Safe": "#16A34A",
            "Needs Review": "#F59E0B",
            "High Priority": "#F97316",
            "Escalated": "#EF4444",
        }
        fig = px.pie(
            status,
            values="Count",
            names="Case_Status",
            hole=.62,
            color="Case_Status",
            color_discrete_map=color_map,
        )
        fig.update_traces(textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=3)))
        fig.add_annotation(
            text=f"<b>{len(df):,}</b><br>Total Cases",
            x=.5,
            y=.5,
            showarrow=False,
            font=dict(size=17, color="#071226"),
        )
        st.plotly_chart(clean_fig(fig, 340), use_container_width=True, config=chart_config("case_status_distribution"))

    # =====================================================
    # 3) SUPPORTING RISK INTELLIGENCE — compact visual row
    # =====================================================
    c1, c2, c3 = st.columns([1, 1, .92])
    with c1:
        chart_wrapper("Average Risk by Channel")
        channel = df.groupby("Channel", as_index=False)["Final_Risk_Score"].mean().sort_values("Final_Risk_Score", ascending=False)
        fig = px.bar(
            channel,
            x="Channel",
            y="Final_Risk_Score",
            text=channel["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0F2D5C"],
        )
        fig.update_traces(textposition="outside", marker_line_width=0, width=.55)
        fig.update_yaxes(range=[0, 100], title="Avg Risk Score")
        fig.update_xaxes(title="")
        st.plotly_chart(clean_fig(fig, 320), use_container_width=True, config=chart_config("risk_by_channel"))

    with c2:
        chart_wrapper("Top Risk Locations")
        location = (
            df.groupby("Location", as_index=False)["Final_Risk_Score"]
            .mean()
            .sort_values("Final_Risk_Score", ascending=False)
            .head(5)
        )
        fig = px.bar(
            location,
            y="Location",
            x="Final_Risk_Score",
            orientation="h",
            text=location["Final_Risk_Score"].round(1),
            color_discrete_sequence=["#0F2D5C"],
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig.update_xaxes(range=[0, 100], title="Avg Risk Score")
        fig.update_yaxes(title="")
        fig.update_traces(textposition="outside")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.plotly_chart(clean_fig(fig, 320), use_container_width=True, config=chart_config("top_risk_locations"))

    with c3:
        chart_wrapper("Top Risk Indicators")
        indicators = [
            ("⇧", "High Amount", int(df["High_Amount_Flag"].sum()), "#EF4444"),
            ("☾", "Night Transactions", int(df["Is_Night_Transaction"].sum()), "#0B5BD3"),
            ("ϟ", "Rapid Transactions", int(df["Rapid_Transaction_Flag"].sum()), "#0B5BD3"),
            ("▣", "Rare Device", int(df["Rare_Device_Flag"].sum()), "#0B5BD3"),
            ("●", "Rare Location", int(df["Rare_Location_Flag"].sum()), "#0B5BD3"),
        ]
        for icon, name, count, color in indicators:
            pct = (count / max(len(df), 1)) * 100
            st.markdown(
                f'<div class="metric-mini">'
                f'<div class="metric-dot" style="background:{color}14;color:{color};">{icon}</div>'
                f'<div class="metric-text">{safe_html(name)}</div>'
                f'<div class="metric-number">{count:,}<span style="color:#64748B;font-size:12px;"> ({pct:.1f}%)</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # =====================================================
    # 4) FINAL TABLE — only the most important operations
    # =====================================================
    chart_wrapper("Recent High Risk Transactions")
    # Shows only currently open action cases.
    # Once the analyst takes a closing action such as Reviewed, Marked Safe,
    # False Positive, or Confirmed Fraud, the transaction is removed from this
    # Command Center queue and the next highest-priority open case appears.
    top_source = open_cases.copy()
    top = (
        top_source.sort_values(["Case_Priority_Score", "Final_Risk_Score"], ascending=False)
        .head(10)[[
            "TransactionID", "AccountID", "TransactionAmount", "Channel", "Location",
            "Final_Risk_Score", "Case_Priority_Score", "Case_Status", "Analyst_Decision"
        ]]
        .copy()
    )
    if top.empty:
        st.success("No open high-risk cases in the Command Center queue.")
        return
    top["Final_Risk_Score"] = top["Final_Risk_Score"].round(2)
    top["Case_Priority_Score"] = top["Case_Priority_Score"].round(2)
    event, shown = interactive_table(
        top,
        "cmd_recent_high_risk",
        "recent_high_risk_transactions.csv",
        height=330,
        selectable=True,
        default_columns=[
            "TransactionID", "AccountID", "TransactionAmount", "Channel", "Location",
            "Final_Risk_Score", "Case_Status", "Analyst_Decision"
        ],
        max_default_rows=10,
    )
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
        open_case(txn)

def page_live_monitor(df):
    render_topbar("Live Monitoring", "Real-time simulation with live counters, alerts, and transaction feed", show_export=False)

    if "live_last_txn" not in st.session_state:
        st.session_state.live_last_txn = "Waiting"
    if "live_last_time" not in st.session_state:
        st.session_state.live_last_time = "--"

    sorted_all = df.sort_values("TransactionDate", ascending=False).reset_index(drop=True)

    c1, c2, c3, _ = st.columns([1, 1, 1, 4])
    if c1.button("▶ Start", use_container_width=True):
        st.session_state.monitoring_on = True
    if c2.button("⏸ Stop", use_container_width=True):
        st.session_state.monitoring_on = False
        st.session_state.live_manual_slider_version = st.session_state.get("live_manual_slider_version", 0) + 1
    if c3.button("↻ Reset", use_container_width=True):
        st.session_state.live_count = min(50, len(df))
        st.session_state.monitoring_on = False
        st.session_state.live_manual_slider_version = st.session_state.get("live_manual_slider_version", 0) + 1
        st.session_state.live_last_txn = "Waiting"
        st.session_state.live_last_time = "--"

    # One source of truth for the whole live page.
    # The slider, the big live card, KPI Feed Size, charts, and table all use this same value.
    if st.session_state.monitoring_on and st.session_state.live_count < len(df):
        st.session_state.live_count = min(int(st.session_state.live_count) + 1, len(df))
        new_idx = min(int(st.session_state.live_count) - 1, len(sorted_all) - 1)
        st.session_state.live_last_txn = str(sorted_all.iloc[new_idx]["TransactionID"])
        st.session_state.live_last_time = datetime.now().strftime("%H:%M:%S")

    live_count = min(max(int(st.session_state.live_count), 1), len(df))

    if st.session_state.monitoring_on:
        st.slider(
            "Visible feed size",
            1,
            len(df),
            live_count,
            1,
            key=f"live_visible_feed_size_auto_{live_count}",
            disabled=True,
        )
    else:
        live_count = st.slider(
            "Visible feed size",
            1,
            len(df),
            live_count,
            1,
            key=f"live_visible_feed_size_manual_{st.session_state.get('live_manual_slider_version', 0)}",
        )
        st.session_state.live_count = int(live_count)

    live_count = min(max(int(st.session_state.live_count), 1), len(df))
    live_df = sorted_all.head(live_count).copy()

    high_count = int((live_df["Risk_Category"] == "High").sum())
    open_alerts = int(((live_df["Case_Status"].isin(["Escalated", "High Priority"])) & (live_df["Analyst_Decision"].isin(["Pending Review", "Under Investigation"]))).sum())
    avg_preview = float(live_df["Final_Risk_Score"].mean()) if not live_df.empty else 0

    st.markdown(f"""
    <div class="live-counter-card">
        <div class="live-metric-label">Live feed size</div>
        <div class="live-counter-number">{live_count:,}</div>
        <div style="color:#64748B;font-size:12px;font-weight:800;margin-top:8px;">
            Latest transaction: <b>{safe_html(st.session_state.live_last_txn)}</b> · Last update {safe_html(st.session_state.live_last_time)} · High risk {high_count:,} · Open alerts {open_alerts:,} · Avg risk {avg_preview:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    alert_panel(live_df)

    a, b, c, d = st.columns(4)
    with a:
        kpi_card("Feed Size", f"{live_count:,}", "⌁", "Visible records", "Live", "cyan")
    with b:
        kpi_card("High Risk", f"{high_count:,}", "⚑", "Detected", "Review", "orange")
    with c:
        kpi_card("Open Alerts", f"{open_alerts:,}", "!", "Need action", "Active", "red")
    with d:
        kpi_card("Avg Risk", f"{avg_preview:.2f}", "◌", "Current feed", "Score", "blue")

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    cchart1, cchart2 = st.columns([1.05, .95])
    with cchart1:
        chart_wrapper("Live Risk Movement")
        live_trend = live_df.sort_values("TransactionDate").tail(35).copy()
        if not live_trend.empty:
            fig = px.line(live_trend, x="TransactionDate", y="Final_Risk_Score", markers=True, color_discrete_sequence=["#0B5BD3"])
            fig.update_traces(line=dict(width=3.8), marker=dict(size=8))
            fig.update_yaxes(range=[0, 100], title="Risk")
            fig.update_xaxes(title="")
            st.plotly_chart(clean_fig(fig, 270), use_container_width=True, config=chart_config("live_risk_movement"))
    with cchart2:
        chart_wrapper("Live Status Mix")
        stat = live_df["Case_Status"].value_counts().reset_index()
        stat.columns = ["Case_Status", "Count"]
        if not stat.empty:
            fig = px.bar(stat, x="Case_Status", y="Count", text="Count", color_discrete_sequence=["#0F2D5C"])
            fig.update_traces(textposition="outside")
            fig.update_xaxes(title="")
            fig.update_yaxes(title="")
            st.plotly_chart(clean_fig(fig, 270), use_container_width=True, config=chart_config("live_status_mix"))

    chart_wrapper("Live Transaction Feed")
    live_show = live_df[["TransactionID", "AccountID", "TransactionDate", "TransactionAmount", "Location", "Channel", "Final_Risk_Score", "Case_Priority_Score", "Case_Status", "Analyst_Decision"]].sort_values("Final_Risk_Score", ascending=False).copy()
    live_show["Final_Risk_Score"] = live_show["Final_Risk_Score"].round(2)
    live_show["Case_Priority_Score"] = live_show["Case_Priority_Score"].round(2)
    event, shown = interactive_table(
        live_show,
        "live_feed_table",
        "live_transaction_feed.csv",
        height=520,
        selectable=True,
        default_columns=["TransactionID", "AccountID", "TransactionDate", "TransactionAmount", "Location", "Channel", "Final_Risk_Score", "Case_Status", "Analyst_Decision"],
        max_default_rows=min(len(live_show), 50) if len(live_show) else 1,
    )
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
        open_case(txn)

    # Keep Live Monitoring moving after Start.
    # This restores the one-by-one live counter update without affecting other pages.
    if st.session_state.monitoring_on and st.session_state.live_count < len(df):
        time.sleep(0.28)
        st.rerun()


def page_investigation_workspace(df):
    render_topbar("Investigation Workspace", "Prioritized queue, case review, account profile, and analyst actions", show_export=False)
    st.markdown('<div class="section-kicker">Investigation Queue</div>', unsafe_allow_html=True)
    fdf = filtered_df(df, "queue")
    open_only = st.toggle("Show open cases only", value=True)
    if open_only:
        fdf = fdf[fdf["Analyst_Decision"].isin(["Pending Review", "Under Investigation"])]
        fdf = fdf[fdf["Case_Status"].isin(["Escalated", "High Priority", "Needs Review"])]
    fdf = fdf.sort_values(["Case_Priority_Score", "Final_Risk_Score"], ascending=False)
    a,b,c,d = st.columns(4)
    with a: kpi_card("Cases in View", f"{len(fdf):,}", "▣", "Filtered", "")
    with b: kpi_card("Pending", f"{(fdf['Analyst_Decision']=='Pending Review').sum():,}", "◷", "Needs action", "")
    with c: kpi_card("Critical", f"{(fdf['Case_Status']=='Escalated').sum():,}", "!", "Escalated", "Critical", "red")
    with d: kpi_card("Handled", f"{(df['Analyst_Decision']!='Pending Review').sum():,}", "✓", "Reviewed", "")
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    chart_wrapper("Investigation Queue", "Select case")
    if fdf.empty:
        st.success("No cases match the selected filters.")
        return
    cols = ["TransactionID","AccountID","TransactionAmount","Location","Channel","Final_Risk_Score","Case_Priority_Score","Case_Status","Analyst_Decision"]
    qshow = fdf[cols].copy(); qshow["Final_Risk_Score"] = qshow["Final_Risk_Score"].round(2); qshow["Case_Priority_Score"] = qshow["Case_Priority_Score"].round(2)

    search_txn = st.text_input(
        "Search TransactionID",
        placeholder="Type TransactionID here, e.g. TX000275",
        key="investigation_txn_search",
    ).strip()
    if search_txn:
        matched = fdf[fdf["TransactionID"].astype(str).str.contains(search_txn, case=False, na=False)].copy()
        if matched.empty:
            st.warning("No matching TransactionID found in the current queue filters.")
        else:
            picked = st.selectbox(
                "Matching cases",
                matched["TransactionID"].astype(str).tolist(),
                key="investigation_txn_match_select",
            )
            st.session_state.selected_txn = picked
            qshow = matched[cols].copy()
            qshow["Final_Risk_Score"] = qshow["Final_Risk_Score"].round(2)
            qshow["Case_Priority_Score"] = qshow["Case_Priority_Score"].round(2)
    st.markdown('<div class="queue-search-note">Select a row from the queue or search by TransactionID above.</div>', unsafe_allow_html=True)
    event, shown = interactive_table(qshow, "investigation_queue", "investigation_queue.csv", height=430, selectable=True, default_columns=cols, max_default_rows=12, controls_mode="customize")
    if event.selection.rows:
        txn = shown.iloc[event.selection.rows[0]]["TransactionID"]
        st.session_state.selected_txn = txn
    elif st.session_state.selected_txn not in fdf["TransactionID"].astype(str).tolist():
        st.session_state.selected_txn = str(qshow.iloc[0]["TransactionID"])
    selected = df[df["TransactionID"].astype(str) == str(st.session_state.selected_txn)].iloc[0]
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    render_case_block(df, selected)

def build_powerbi_report(df):
    """Build the final CSV used by Power BI without changing the dashboard structure."""
    export_columns = [
        "TransactionID", "AccountID", "TransactionDate", "PreviousTransactionDate",
        "TransactionAmount", "TransactionType", "Location", "DeviceID", "IP Address",
        "MerchantID", "Channel", "CustomerAge", "CustomerOccupation", "TransactionDuration",
        "LoginAttempts", "AccountBalance", "TimeSincePreviousTransaction_Minutes",
        "Is_Night_Transaction", "Rapid_Transaction_Flag", "High_Amount_Flag",
        "High_Login_Attempts_Flag", "Rare_Location_Flag", "Rare_Device_Flag",
        "Rare_Merchant_Flag", "Anomaly_Flag", "ML_Risk_Score", "Behavioral_Risk_Score",
        "Final_Risk_Score", "Case_Priority_Score", "Fraud_Probability", "Fraud_Prediction",
        "Risk_Category", "Case_Status", "Analyst_Decision", "Risk_Reason", "Recommended_Action",
    ]
    export_columns = [c for c in export_columns if c in df.columns]
    report = df[export_columns].copy()
    report["Transaction_Action"] = report["TransactionID"].astype(str).map(st.session_state.transaction_actions).fillna("No action yet")
    report["Account_Action"] = report["AccountID"].astype(str).map(st.session_state.account_actions).fillna("Active")
    return report


def page_audit_reports(df):
    render_topbar("Audit & Reports", "Complete investigation record, operational actions, and exportable reports", show_export=False)
    st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
    tabs = st.tabs(["Audit Overview", "Audit Trail", "Investigation Report", "Operational Outputs"])
    audit = pd.DataFrame(st.session_state.audit_log)
    report = build_powerbi_report(df)

    with tabs[0]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        a, b, c, d, e = st.columns(5)
        pending_cases = int((df["Analyst_Decision"] == "Pending Review").sum())
        confirmed = int(audit["Decision"].eq("Confirmed Fraud").sum()) if not audit.empty and "Decision" in audit else 0
        false_positive = int(audit["Decision"].eq("False Positive").sum()) if not audit.empty and "Decision" in audit else 0
        blocked = sum(1 for v in st.session_state.account_actions.values() if v == "Temporarily Blocked")
        with a:
            kpi_card("Recorded Actions", f"{len(audit):,}", "☷", "Audit log", "")
        with b:
            kpi_card("Confirmed Fraud", f"{confirmed:,}", "!", "Analyst", "", "orange")
        with c:
            kpi_card("False Positives", f"{false_positive:,}", "✓", "Closed", "", "green")
        with d:
            kpi_card("Blocked Accounts", f"{blocked:,}", "🛡", "Actioned", "", "red")
        with e:
            kpi_card("Pending Cases", f"{pending_cases:,}", "◷", "Awaiting review", "", "orange")

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            chart_wrapper("Decision Breakdown")
            if audit.empty or "Decision" not in audit:
                st.info("No analyst decisions yet.")
            else:
                dec = audit["Decision"].value_counts().reset_index()
                dec.columns = ["Decision", "Count"]
                fig = px.bar(dec, x="Decision", y="Count", color_discrete_sequence=["#0F2D5C"], text="Count")
                fig.update_traces(textposition="outside")
                st.plotly_chart(clean_fig(fig, 300), use_container_width=True, config=chart_config("decision_breakdown"))
        with c2:
            chart_wrapper("Recent Operational Actions")
            if audit.empty:
                st.info("No recent actions yet.")
            else:
                recent = audit.tail(5).iloc[::-1]
                for _, r in recent.iterrows():
                    st.markdown(
                        f'<div class="metric-mini"><div class="metric-dot" style="background:#DBEAFE;color:#0B5BD3;">•</div>'
                        f'<div class="metric-text">{safe_html(r.get("Decision", "Action"))}</div>'
                        f'<div class="metric-number" style="font-size:12px;max-width:60%;">{safe_html(r.get("TransactionID", ""))}<br>{safe_html(r.get("Timestamp", ""))}</div></div>',
                        unsafe_allow_html=True,
                    )

    with tabs[1]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        if audit.empty:
            st.info("No analyst actions recorded yet.")
        else:
            interactive_table(
                audit,
                "audit_trail_table",
                "audit_trail.csv",
                height=460,
                selectable=False,
                default_columns=list(audit.columns),
                max_default_rows=min(len(audit), 100) if len(audit) else 1,
                controls_mode="customize",
            )

    with tabs[2]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="report-toolbar">
            <div>
                <div class="report-title">Final Investigation Report Dataset</div>
                <div class="report-sub">Power BI ready output. It keeps the same core fraud results structure, with analyst decisions and operational actions added as extra columns.</div>
            </div>
            <div class="status-badge status-review">{len(report):,} rows</div>
        </div>
        """, unsafe_allow_html=True)

        # No Table Options here on purpose: this is the final complete report table for Power BI.
        report_table(report, "final_powerbi_report_table", "fraud_results.csv", height=560)

        actioned = report[report["Analyst_Decision"] != "Pending Review"].copy()
        st.download_button(
            "Download Actioned Cases Only",
            actioned.to_csv(index=False).encode("utf-8"),
            "actioned_cases_only.csv",
            "text/csv",
            use_container_width=True,
        )

    with tabs[3]:
        st.markdown('<div class="audit-tab-spacer"></div>', unsafe_allow_html=True)
        audit_rows = len(audit)
        actioned_rows = int((report["Analyst_Decision"] != "Pending Review").sum())
        output_html = (
            '<div class="output-grid">'
            '<div class="output-card"><div class="output-card-title">fraud_results.csv</div>'
            '<div class="output-card-sub">Final Power BI source file with risk scores, case status, analyst decisions, and operational actions.</div>'
            f'<div class="output-chip">{len(report):,} rows</div></div>'
            '<div class="output-card"><div class="output-card-title">audit_trail.csv</div>'
            '<div class="output-card-sub">Chronological record of analyst decisions, notes, playbook actions, and case effects.</div>'
            f'<div class="output-chip">{audit_rows:,} actions</div></div>'
            '<div class="output-card"><div class="output-card-title">actioned_cases_only.csv</div>'
            '<div class="output-card-sub">Filtered export for reviewed, escalated, confirmed fraud, false positive, or marked safe cases.</div>'
            f'<div class="output-chip">{actioned_rows:,} cases</div></div>'
            '</div>'
        )
        st.markdown(output_html, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("Download fraud_results.csv", report.to_csv(index=False).encode("utf-8"), "fraud_results.csv", "text/csv", use_container_width=True)
        with c2:
            audit_export = audit if not audit.empty else pd.DataFrame(columns=["Timestamp", "TransactionID", "AccountID", "Analyst", "Decision", "Playbook_Action", "Transaction_Action", "Account_Action", "Operational_Effect", "Note"])
            st.download_button("Download audit_trail.csv", audit_export.to_csv(index=False).encode("utf-8"), "audit_trail.csv", "text/csv", use_container_width=True)
        with c3:
            actioned = report[report["Analyst_Decision"] != "Pending Review"].copy()
            st.download_button("Download actioned_cases_only.csv", actioned.to_csv(index=False).encode("utf-8"), "actioned_cases_only.csv", "text/csv", use_container_width=True)

        actions = pd.DataFrame([{"AccountID": k, "Account_Status": v} for k, v in st.session_state.account_actions.items()])
        if not actions.empty:
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            chart_wrapper("Account-Level Operational Status")
            st.dataframe(actions, use_container_width=True, hide_index=True, height=260)


# =========================================================
# RUN APP
# =========================================================
if not st.session_state.data_loaded:
    upload_gate()

# Run the clock refresh only after the dataset is fully loaded.
# This prevents the upload/analyze progress from restarting every second.
st_autorefresh(interval=1000, key="live_clock_refresh")

df = apply_decisions(st.session_state.df)
page = sidebar(df)

if page == "▦  Command Center":
    page_command_center(df)
elif page == "⌁  Live Monitoring":
    page_live_monitor(df)
elif page == "▣  Investigation Workspace":
    page_investigation_workspace(df)
elif page == "☷  Audit & Reports":
    page_audit_reports(df)
