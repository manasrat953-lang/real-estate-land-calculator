import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Land Engine | Madinet Masr",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Global Styling (Pure Black, Pure White Text, Montserrat Font, Dark Inputs)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* Global Base */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Typography & Headers */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Header Container Alignment */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 2rem;
    }
    .brand-title {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 2px;
        margin-top: 10px;
        color: #FFFFFF !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid #222222 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Dark Input Fields & Dropdowns */
    input, select, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #121212 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
    }
    
    /* Metrics & Cards */
    div[data-testid="stMetric"] {
        background-color: #111111;
        border: 1px solid #222222;
        padding: 15px;
        border-radius: 6px;
    }
    div[data-testid="stMetric"] label {
        color: #AAAAAA !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #000000;
        border-bottom: 1px solid #222222;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #0A0A0A;
        border-radius: 4px 4px 0px 0px;
        color: #AAAAAA;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border-bottom: 2px solid #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header & Logo Integration
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    try:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Madinet_Masr_Logo.png", width=160)
    except:
        pass
    st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222222; margin-bottom: 2rem;'>", unsafe_allow_html=True)

# 4. Session State Initialization
if "gla_sqm" not in st.session_state:
    st.session_state.gla_sqm = 899612.57  # ~214.19 Feddans
if "efficiency" not in st.session_state:
    st.session_state.efficiency = 0.90
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "GLA"
if "unit_mode" not in st.session_state:
    st.session_state.unit_mode = "Feddans"
if "land_type" not in st.session_state:
    st.session_state.land_type = "Mixed Use"
if "res_pct" not in st.session_state:
    st.session_state.res_pct = 0.50
if "serv_pct" not in st.session_state:
    st.session_state.serv_pct = 0.15
if "far_val" not in st.session_state:
    st.session_state.far_val = 1.25
if "max_height" not in st.session_state:
    st.session_state.max_height = 4.0

# Conversion factor: 1 Feddan = 4,200 SQM
FEDDAN_TO_SQM = 4200.0

# 5. Main Tab Navigation
tab_names = [
    "Land Data", "Land Analysis", "Land Constraints", 
    "Residential Mix", "Services Mix", "Prototypes Analysis", 
    "New Type Analysis", "Parking Calculations", "Summary Results"
]

selected_tab = st.selectbox("Select Active Section:", tab_names, label_visibility="collapsed")

# 6. Context-Aware Dynamic Sidebar Inputs
with st.sidebar:
    st.markdown(f"### ⚙️ {selected_tab} Controls")
    st.markdown("<hr style='border: 0.5px solid #333333;'>", unsafe_allow_html=True)

    if selected_tab == "Land Data":
        st.session_state.input_mode = st.radio("Primary Area Input", ["GLA", "NLA"], index=0 if
