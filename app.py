import streamlit as st
import pandas as pd

st.set_page_config(page_title="Land Engine | Madinet Masr", page_icon="🏙️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Montserrat', sans-serif !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown { color: #FFFFFF !important; font-family: 'Montserrat', sans-serif !important; }
    .header-box { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-top: 10px; margin-bottom: 20px; }
    .brand-title { font-size: 2rem; font-weight: 600; letter-spacing: 2px; color: #FFFFFF !important; margin-top: 12px; font-family: 'Montserrat', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0A0A0A !important; border-right: 1px solid #222222 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-family: 'Montserrat', sans-serif !important; }
    input, select, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stNumberInput input, .stTextInput input { background-color: #161616 !important; color: #FFFFFF !important; border: 1px solid #333333 !important; border-radius: 6px !important; font-family: 'Montserrat', sans-serif !important; }
    div[data-testid="stMetric"] { background-color: #111111; border: 1px solid #222222; padding: 16px; border-radius: 8px; }
    div[data-testid="stMetric"] label { color: #AAAAAA !important; font-size: 0.85rem !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.6rem !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="header-box"><h2 style="letter-spacing: 3px; font-weight: 700; margin:0; color:#FFFFFF;">MADINET MASR</h2><div class="brand-title">Land Engine</div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222222; margin-bottom: 2rem;'>", unsafe_allow_html=True)

if "gla_sqm" not in st.session_state: st.session_state.gla_sqm = 899612.57
if "efficiency" not in st.session_state: st.session_state.efficiency = 0.90
if "input_mode" not in st.session_state: st.session_state.input_mode = "GLA"
if "unit_mode" not in st.session_state: st.session_state.unit_mode = "Feddans"
if "land_type" not in st.session_state: st.session_state.land_type = "Mixed Use"
if "res_pct" not in st.session_state: st.session_state.res_pct = 0.50
if "serv_pct" not in st.session_state: st
