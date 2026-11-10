import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Land Engine | Madinet Masr",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Clean Dark Theme & Typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #0A0A0A;
        border-right: 1px solid #222222;
    }

    .brand-title {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: #FFFFFF;
        margin-top: 10px;
        text-align: center;
        font-family: 'Montserrat', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header & Corporate Title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h2 style="letter-spacing: 3px; font-weight: 700; text-align: center; color: #FFFFFF; margin:0;">MADINET MASR</h2>', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222222; margin: 2rem 0;'>", unsafe_allow_html=True)

# 4. Initialize Session State Variables
if "gla_sqm" not in st.session_state: st.session_state.gla_sqm = 899612.57
if "efficiency" not in st.session_state: st.session_state.efficiency = 0.90
if "input_mode" not in st.session_state: st.session_state.input_mode = "GLA"
if "unit_mode" not in st.session_state: st.session_state.unit_mode = "Feddans"
if "land_type" not in st.session_state: st.session_state.land_type = "Mixed Use"
if "res_pct" not in st.session_state: st.session_state.res_pct = 0.50
if "serv_pct" not in st.session_state: st.session_state.serv_pct = 0.15
if "far_val" not in st.session_state: st.session_state.far_val = 1.25
if "max_height" not in st.session_state: st.session_state.max_height = 4.0
if "res_apt_pct" not in st.session_state: st.session_state.res_apt_pct = 0.60
if "retail_pct" not in st.session_state: st.session_state.retail_pct = 0.70
if "parking_ratio" not in st.session_state: st.session_state.parking_ratio = 1.50

FEDDAN_TO_SQM = 4200.0

# 5. Tab Navigation
tab_names = [
    "Land Data", "Land Analysis", "Land Constraints", 
    "Residential Mix", "Services Mix", "Prototypes Analysis", 
    "New Type Analysis", "Parking Calculations", "Summary Results"
]

selected_tab = st.selectbox("Select Active Section", tab_names, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

# 6. Sidebar Inputs Filtered by Selected Tab
with st.sidebar:
    st.markdown(f"### ⚙️ {selected_tab} Controls")
    st.markdown("---")

    if selected_tab == "Land Data":
        st.session_state.input_mode = st.radio("Primary Area Input", ["GLA", "NLA"], index=0 if st.session_state.input_mode == "GLA" else 1)
        st.session_state.unit_mode = st.radio("Unit Type", ["Feddans", "SQM"], index=0 if st.session_state.unit_mode == "Feddans" else 1)
        st.session_state.efficiency = st.slider("Efficiency Ratio (NLA / GLA)", 0.50, 1.00, float(st.session_state.efficiency), 0.01, format="%.2f")
        
        curr_val = (st.session_state.gla_sqm / FEDDAN_TO_SQM) if st.session_state.unit_mode == "Feddans" else st.session_state.gla_sqm
        entered_val = st.number_input(f"Enter {st.session_state.input_mode} in {st.session_state.unit_mode}", value=float(curr_val), format="%.2f")
        
        base_sqm = entered_val * FEDDAN_TO_SQM if st.session_state.unit_mode == "Feddans" else entered_val
        st.session_state.gla_sqm = base_sqm / max(0.01, st.session_state.efficiency) if st.session_state.input_mode == "NLA" else base_sqm
        st.session_state.land_type = st.selectbox("Land Type", ["Mixed Use", "Residential", "Commercial", "Hospitality"], index=0)

    elif selected_tab == "Land Analysis":
        st.session_state.res_pct = st.slider("Residential % from NLA", 0.0, 1.0, float(st.session_state.res_pct), 0.01, format="%.2f")
        st.session_state.serv_pct = st.slider("Services % from NLA", 0.0, 1.0, float(st.session_state.serv_pct), 0.01, format="%.2f")

    elif selected_tab == "Land Constraints":
        st.session_state.far_val = st.number_input("Floor Area Ratio (FAR)", value=float(st.session_state.far_val), format="%.2f")
        st.session_state.max_height = st.number_input("Max Building Height (Floors)", value=float(st.session_state.max_height), format="%.2f")

    elif selected_tab == "Residential Mix":
        st.session_state.res_apt_pct = st.slider("Apartments Ratio", 0.0, 1.0, float(st.session_state.res_apt_pct), 0.01, format="%.2f")

    elif selected_tab == "Services Mix":
        st.session_state.retail_pct = st.slider("Retail & Commercial Ratio", 0.0, 1.0, float(st.session_state.retail_pct), 0.01, format="%.2f")

    elif selected_tab == "Prototypes Analysis":
        st.session_state.prototype_bua = st.number_input("Avg Unit BUA (SQM)", value=180.00, format="%.2f")
        st.session_state.prototype_price = st.number_
