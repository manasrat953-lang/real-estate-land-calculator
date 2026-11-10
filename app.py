import streamlit as st
import pandas as pd

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="Land Engine | Madinet Masr",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Global CSS Styling (Pure Black Background, Montserrat Typography, White Text)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }
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
    [data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid #222222 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    input, select, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #121212 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
    }
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
</style>
""", unsafe_allow_html=True)

# 3. Logo & Centered Title Header
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    try:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Madinet_Masr_Logo.png", width=160)
    except Exception:
        pass
    st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222222; margin-bottom: 2rem;'>", unsafe_allow_html=True)

# 4. Session State Defaults
if "gla_sqm" not in st.session_state:
    st.session_state.gla_sqm = 899612.57
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

FEDDAN_TO_SQM = 4200.0

# 5. Define Tab Navigation BEFORE using selected_tab
tab_names = [
    "Land Data", "Land Analysis", "Land Constraints", 
    "Residential Mix", "Services Mix", "Prototypes Analysis", 
    "New Type Analysis", "Parking Calculations", "Summary Results"
]

selected_tab = st.radio("Navigation", tab_names, horizontal=True, label_visibility="collapsed")

# 6. Dynamic Sidebar Controls (NOW selected_tab is defined)
with st.sidebar:
    st.markdown(f"### ⚙️ {selected_tab} Controls")
    st.markdown("<hr style='border: 0.5px solid #333333;'>", unsafe_allow_html=True)

    if selected_tab == "Land Data":
        st.session_state.input_mode = st.radio(
            "Primary Area Input", 
            ["GLA", "NLA"], 
            index=0 if st.session_state.input_mode == "GLA" else 1
        )
        st.session_state.unit_mode = st.radio(
            "Unit Type", 
            ["Feddans", "SQM"], 
            index=0 if st.session_state.unit_mode == "Feddans" else 1
        )
        
        st.session_state.efficiency = st.slider(
            "Efficiency Ratio (NLA / GLA)", 
            0.50, 1.00, 
            float(st.session_state.efficiency), 
            0.01, 
            format="%.2f"
        )

        current_val_display = (st.session_state.gla_sqm / FEDDAN_TO_SQM) if st.session_state.unit_mode == "Feddans" else st.session_state.gla_sqm
        entered_val = st.number_input(
            f"Enter {st.session_state.input_mode} in {st.session_state.unit_mode}", 
            value=float(current_val_display), 
            format="%.2f"
        )
        
        base_sqm = entered_val * FEDDAN_TO_SQM if st.session_state.unit_mode == "Feddans" else entered_val

        if st.session_state.input_mode == "NLA":
            st.session_state.gla_sqm = base_sqm / max(0.01, st.session_state.efficiency)
        else:
            st.session_state.gla_sqm = base_sqm

        st.session_state.land_type = st.selectbox(
            "Land Type", 
            ["Mixed Use", "Residential", "Commercial", "Hospitality"], 
            index=0
        )

    elif selected_tab == "Land Constraints":
        st.session_state.far_val = st.number_input("Floor Area Ratio (FAR)", value=float(st.session_state.far_val), format="%.2f")
        st.session_state.max_height = st.number_input("Max Building Height (Floors)", value=float(st.session_state.max_height), format="%.2f")

    elif selected_tab == "Residential Mix":
        st.session_state.res_pct = st.slider("Residential % from NLA", 0.0, 1.0, float(st.session_state.res_pct), 0.01, format="%.2f")

    elif selected_tab == "Services Mix":
        st.session_state.serv_pct = st.slider("Services % from NLA", 0.0, 1.0, float(st.session_state.serv_pct), 0.01, format="%.2f")

    else:
        st.info(f"Controls for **{selected_tab}** are synchronized with active masterplan parameters.")

# 7. Core Calculations & Output Display
gla_sqm = st.session_state.gla_sqm
gla_feddans = gla_sqm / FEDDAN_TO_SQM
nla_sqm = gla_sqm * st.session_state.efficiency
nla_feddans = nla_sqm / FEDDAN_TO_SQM

if selected_tab == "Land Data":
    st.markdown("### Land Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("GLA (Feddans)", f"{gla_feddans:,.2f}")
    col2.metric("GLA (SQM)", f"{gla_sqm:,.2f}")
    col3.metric("Efficiency Ratio", f"{st.session_state.efficiency * 100:.1f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("NLA (Feddans)", f"{nla_feddans:,.2f}")
    col5.metric("NLA (SQM)", f"{nla_sqm:,.2f}")
    col6.metric("Land Type", st.session_state.land_type)

elif selected_tab == "Land Analysis":
    st.markdown("### Land Area Breakdown Analysis")
    res_area = nla_sqm * st.session_state.res_pct
    serv_area = nla_sqm * st.session_state.serv_pct
    landscape_area = nla_sqm - (res_area + serv_area)

    col1, col2, col3 = st.columns(3)
    col1.metric("Residential NLA (SQM)", f"{res_area:,.2f}")
    col2.metric("Services NLA (SQM)", f"{serv_area:,.2f}")
    col3.metric
