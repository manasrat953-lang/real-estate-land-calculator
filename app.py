import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Land Engine | Madinet Masr",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Global Styling (Pure Black, Montserrat Font, Dark Inputs, High Contrast Text)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* Global Base */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Centered Header Container */
    .header-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: #FFFFFF !important;
        margin-top: 12px;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid #222222 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Dark Input Fields & Dropdowns with White Text */
    input, select, textarea, 
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    .stNumberInput input, .stTextInput input {
        background-color: #161616 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #111111;
        border: 1px solid #222222;
        padding: 16px;
        border-radius: 8px;
    }
    div[data-testid="stMetric"] label {
        color: #AAAAAA !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Centered Logo & Title Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="header-box">', unsafe_allow_html=True)
    try:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Madinet_Masr_Logo.png", width=160)
    except Exception:
        pass
    st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Land Data"

FEDDAN_TO_SQM = 4200.0

# 5. Section Navigation Bar
tab_names = [
    "Land Data", "Land Analysis", "Land Constraints", 
    - "Residential Mix", "Services Mix", "Prototypes Analysis", 
    "New Type Analysis", "Parking Calculations", "Summary Results"
]

# Use a clean horizontal radio button group as our tab bar
selected_tab = st.radio(
    "Navigation", 
    tab_names, 
    index=tab_names.index(st.session_state.active_tab) if st.session_state.active_tab in tab_names else 0,
    horizontal=True, 
    label_visibility="collapsed"
)
st.session_state.active_tab = selected_tab

st.markdown("<br>", unsafe_allow_html=True)

# 6. Context-Aware Dynamic Sidebar Controls
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
        st.session_state.far_val = st.number_input(
            "Floor Area Ratio (FAR)", 
            value=float(st.session_state.far_val), 
            format="%.2f"
        )
        st.session_state.max_height = st.number_input(
            "Max Building Height (Floors)", 
            value=float(st.session_state.max_height), 
            format="%.2f"
        )

    elif selected_tab == "Residential Mix":
        st.session_state.res_pct = st.slider(
            "Residential % from NLA", 
            0.0, 1.0, 
            float(st.session_state.res_pct), 
            0.01, 
            format="%.2f"
        )

    elif selected_tab == "Services Mix":
        st.session_state.serv_pct = st.slider(
            "Services % from NLA", 
            0.0, 1.0, 
            float(st.session_state.serv_pct), 
            0.01, 
            format="%.2f"
        )

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
    col3.metric("Landscape & Roads (SQM)", f"{landscape_area:,.2f}")

elif selected_tab == "Land Constraints":
    st.markdown("### Land Zoning & Constraints")
    bua_allowable = gla_sqm * st.session_state.far_val
    col1, col2 = st.columns(2)
    col1.metric("Allowable BUA (SQM)", f"{bua_allowable:,.2f}")
    col2.metric("Max Building Height", f"{st.session_state.max_height:.2f} Floors")

else:
    st.markdown(f"### {selected_tab}")
    st.write(f"Parameters and analytics for **{selected_tab}** are active and synchronized.")
