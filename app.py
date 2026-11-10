import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Madinet Masr - Land Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme CSS & Typography Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    .stSidebar {
        background-color: #0A0A0A !important;
        border-right: 1px solid #222222 !important;
    }

    /* Input Fields Styling (Pitch Black Background with Crisp White Text) */
    div[data-baseweb="input"] input, 
    div[data-baseweb="select"] div,
    div[aria-haspopup="listbox"],
    input[type="number"], 
    select {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="popover"], div[role="listbox"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* Hide Raw Text Leakage for Icon Button */
    button[data-testid="stSidebarCollapseButton"]::before {
        content: "" !important;
    }

    /* Centered Header & Branding Elements */
    .brand-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-top: -1rem;
        margin-bottom: 0.5rem;
    }
    .brand-title {
        font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 1.8rem;
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }
    .stMetric {
        background-color: #111111 !important;
        border: 1px solid #222222 !important;
        padding: 14px !important;
        border-radius: 8px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    .dataframe {
        color: #FFFFFF !important;
        background-color: #111111 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header & Branding Section (Perfectly Centered Logo & Title)
# ---------------------------------------------------------
col_l, col_center, col_r = st.columns([1, 2, 1])
with col_center:
    try:
        st.image("LOGO.png", width=160)
    except Exception:
        st.markdown('<div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; text-align: center; letter-spacing: 2px;">Madinet Masr</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# Shared Session State Initialization
# ---------------------------------------------------------
SQM_PER_FEDDAN = 4200.0

if "area_mode" not in st.session_state:
    st.session_state.area_mode = "GLA"
if "unit_mode" not in st.session_state:
    st.session_state.unit_mode = "Feddans"
if "gla_sqm_val" not in st.session_state:
    st.session_state.gla_sqm_val = 899612.57
if "efficiency_val" not in st.session_state:
    st.session_state.efficiency_val = 0.9

def update_efficiency():
    st.session_state.efficiency_val = st.session_state.efficiency_slider

# Tab Selection Radio directly in Sidebar for reliable active state switching
st.sidebar.markdown("### 📌 Navigation Section")
active_tab = st.sidebar.radio(
    "Select Section to View & Edit",
    [
        "Land Data", 
        "Land Analysis", 
        "Land Constraints", 
        "Residential Mix", 
        "Services Mix", 
        "Prototypes Analysis", 
        "New Type Analysis", 
        "Parking Calculations", 
        "Summary Results"
    ],
    key="active_tab_selection"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### 🔴 {active_tab} Inputs")

# Initialize Default Parameter Variables
res_pct_nla = 0.50
serv_pct_nla = 0.15
landscape_pct_nla = 0.35
res_plot_pct = 0.50
serv_plot_pct = 0.30
res_floors = 5
serv_floors = 4
allowed_fp_pct = 0.25
allowed_far = 1.25
design_contingency = 0.0
apt_mix = 0.60
villa_mix = 0.10
th_mix = 0.30
admin_mix = 0.50
comm_mix = 0.50
studio_pct = 0.30
one_br_pct = 0.40
two_br_pct = 0.20
three_br_pct = 0.10
land_type = "Mixed Use"
surface_parking = 5000

# ---------------------------------------------------------
# Dynamic Sidebar Inputs Driven by Selected Navigation Section
# ---------------------------------------------------------
if active_tab == "Land Data":
    st.sidebar.subheader("1. Land Data Controls")
    input_type = st.sidebar.radio("Primary Area Input", ["GLA", "NLA"], key="area_mode_radio", index=0 if st.session_state.area_mode == "GLA" else 1, horizontal=True)
    unit_type = st.sidebar.radio("Unit Type", ["Feddans", "SQM"], key="unit_mode_radio", index=0 if st.session_state.unit_mode == "Feddans" else 1, horizontal=True)

    efficiency = st.sidebar.slider(
        "Efficiency Ratio", 
        min_value=0.1, 
        max_value=1.0, 
        value=st.session_state.efficiency_val, 
        step=0.01,
        key="efficiency_slider",
        on_change=update_efficiency
    )

    if input_type == "GLA":
        if unit_type == "Feddans":
            current_gla_feddans = st.session_state.gla_sqm_val / SQM_PER_FEDDAN
            gla_feddans = st.sidebar.number_input("GLA in feddans", value=float(current_gla_feddans), step=1.0, format="%.2f")
            gla_sqm = gla_feddans * SQM_PER_FEDDAN
        else:
            gla_sqm = st.sidebar.number_input("GLA in SQM", value=float(st.session_state.gla_sqm_val), step=1000.0, format="%.2f")
            gla_feddans = gla_sqm / SQM_PER_FEDDAN
        
        st.session_state.gla_sqm_val = gla_sqm
        nla_sqm = gla_sqm * efficiency
        nla_feddans = gla_feddans * efficiency
    else:
        current_nla_sqm = st.session_state.gla_sqm_val * efficiency
        if unit_type == "Feddans":
            current_nla_feddans = current_nla_sqm / SQM_PER_FEDDAN
            nla_feddans = st.sidebar.number_input("NLA in feddans", value=float(current_nla_feddans), step=1.0, format="%.2f")
            nla_sqm = nla_feddans * SQM_PER_FEDDAN
        else:
            nla_sqm = st.sidebar.number_input("NLA in SQM", value=float(current_nla_sqm), step=1000.0, format="%.2f")
            nla_feddans = nla_sqm / SQM_PER_FEDDAN
        
        gla_sqm = nla_sqm / efficiency if efficiency > 0 else 0
        gla_feddans = nla_feddans / efficiency if efficiency > 0 else 0
        st.session_state.gla_sqm_val = gla_sqm

    st.session_state.area_mode = input_type
    st.session_state.unit_mode = unit_type
    land_type = st.sidebar.selectbox("Land Type", ["Mixed Use", "Residential", "Commercial"])

else:
    efficiency = st.session_state.efficiency_val
    gla_sqm = st.session_state.gla_sqm_val
    gla_feddans = gla_sqm / SQM_PER_FEDDAN
    nla_sqm = gla_sqm * efficiency
    nla_feddans = gla_feddans * efficiency

if active_tab == "Land Analysis":
    st.sidebar.subheader("2. Land Analysis Controls")
    res_pct_nla = st.sidebar.slider("Residential % from NLA", 0.0, 1.0, 0.50, 0.01)
    serv_pct_nla = st.sidebar.slider("Services % from NLA", 0.0, 1.0, 0.15, 0.01)
    landscape_pct_nla = max(0.0, 1.0 - res_pct_nla - serv_pct_nla)

    res_plot_pct = st.sidebar.slider("Residential Plot % from Land", 0.0, 1.0, 0.50, 0.01)
    serv_plot_pct = st.sidebar.slider("Services Plot % from Land", 0.0, 1.0, 0.30, 0.01)

elif active_tab == "Land Constraints":
    st.sidebar.subheader("3. Land Constraints Controls")
    res_floors = st.sidebar.number_input("Residential Floors", value=5, step=1)
    serv_floors = st.sidebar.number_input("Services Floors", value=4, step=1)
    allowed_fp_pct = st.sidebar.number_input("Allowed Footprint %", value=0.25, step=0.01, format="%.2f")
    allowed_far = st.sidebar.number_input("Allowed FAR", value=1.25, step=0.05, format="%.2f")
    design_contingency = st.sidebar.number_input("Design Contingency", value=0.0, step=0.01, format="%.2f")

elif active_tab == "Residential Mix":
    st.sidebar.subheader("4. Residential Mix Controls")
    apt_mix = st.sidebar.slider("Apartments Mix %", 0.0, 1.0, 0.60, 0.05)
    villa_mix = st.sidebar.slider("Villas Mix %", 0.0, 1.0, 0.10, 0.05)
    th_mix = st.sidebar.slider("Townhouses Mix %", 0.0, 1.0, 0.30, 0.05)

elif active_tab == "Services Mix":
    st.sidebar.subheader("5. Services Mix Controls")
    admin_mix = st.sidebar.slider("Admin Mix %", 0.0, 1.0, 0.50, 0.05)
    comm_mix = 1.0 - admin_mix

elif active_tab == "New Type Analysis":
    st.sidebar.subheader("6. New Type Mix Controls")
    studio_pct = st.sidebar.slider("Studio Mix %", 0.0, 1.0, 0.30, 0.05)
    one_br_pct = st.sidebar.slider("1BR Mix %", 0.0, 1.0, 0.40, 0.05)
    two_br_pct = st.sidebar.slider("2BR Mix %", 0.0, 1.0, 0.20, 0.05)
    three_br_pct = max(0.0, 1.0 - studio_pct - one_br_pct - two_br_pct)

elif active_tab == "Parking Calculations":
    st.sidebar.subheader("7. Parking Controls")
    surface_parking = st.sidebar.number_input("Surface Level Parking Slots", value=5000, step=500)

elif active_tab in ["Prototypes Analysis", "Summary Results"]:
    st.sidebar.info("ℹ️ This section presents calculated outputs. Select an editable tab to adjust input parameters.")

# ---------------------------------------------------------
# Core Real-Time Calculation Engine
# ---------------------------------------------------------
<!-- ... existing code -->
# ---------------------------------------------------------
# Populate Content inside Main Tabs
# ---------------------------------------------------------
tab_index = [
    "Land Data", 
    "Land Analysis", 
    "Land Constraints", 
    "Residential Mix", 
    "Services Mix", 
    "Prototypes Analysis", 
    "New Type Analysis", 
    "Parking Calculations", 
    "Summary Results"
].index(active_tab)

# Render Section Header based on Navigation Selection
st.subheader(active_tab)

if active_tab == "Land Data":
    c1, c2, c3 = st.columns(3)
    c1.metric("GLA (Feddans)", f"{gla_feddans:,.2f}")
    c2.metric("GLA (SQM)", f"{gla_sqm:,.2f}")
    c3.metric("Efficiency Ratio", f"{efficiency*100:.1f}%")
    
    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    c4.metric("NLA (Feddans)", f"{nla_feddans:,.2f}")
    c5.metric("NLA (SQM)", f"{nla_sqm:,.2f}")
    c6.metric("Land Type", land_type)

elif active_tab == "Land Analysis":
    df_la = pd.DataFrame({
        "Component": ["Residential Land", "Services Land", "Landscape & Roads"],
        "% from NLA": [res_pct_nla, serv_pct_nla, landscape_pct_nla],
        "Total Land (SQM)": [total_res_land, total_serv_land, total_landscape_land],
        "% Plots from Land": [res_plot_pct, serv_plot_pct, 0.0],
        "Total Plots (SQM)": [total_res_plots, total_serv_plots, 0.0]
    })
    st.dataframe(df_la.style.format({
        "% from NLA": "{:.1%}",
        "Total Land (SQM)": "{:,.2f}",
        "% Plots from Land": "{:.1%}",
        "Total Plots (SQM)": "{:,.2f}"
    }), use_container_width=True)

elif active_tab == "Land Constraints":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Allowed Footprint %", f"{allowed_fp_pct*100:.1f}%")
    c2.metric("Allowed Footprint (SQM)", f"{allowed_footprint:,.2f}")
    c3.metric("Allowed BUA (SQM)", f"{allowed_bua:,.2f}")
    c4.metric("Allowed FAR", f"{allowed_far:.2f}")

elif active_tab == "Residential Mix":
    df_res = pd.DataFrame({
        "Type": ["Apartments", "Villas", "Townhouses", "Local Services"],
        "Plot Mix %": [apt_mix, villa_mix, th_mix, 0.02],
        "Mix Plots (SQM)": [apt_plots, villa_plots, th_plots, local_services_land],
        "Coverage": [0.5, 0.4, 0.4, 1.0],
        "Actual Footprint (SQM)": [apt_fp, villa_fp, th_fp, local_services_land],
        "Floors": [res_floors, 2.25, 2.5, 1],
        "Mix BUA (SQM)": [apt_bua, villa_bua, th_bua, local_services_land]
    })
    st.dataframe(df_res.style.format({
        "Plot Mix %": "{:.1%}",
        "Mix Plots (SQM)": "{:,.2f}",
        "Coverage": "{:.1%}",
        "Actual Footprint (SQM)": "{:,.2f}",
        "Mix BUA (SQM)": "{:,.2f}"
    }), use_container_width=True)

elif active_tab == "Services Mix":
    df_serv = pd.DataFrame({
        "Type": ["Admin", "Commercial"],
        "Plot Mix %": [admin_mix, comm_mix],
        "Mix Plots (SQM)": [admin_plots, comm_plots],
        "Coverage": [0.3, 0.3],
        "Actual Footprint (SQM)": [admin_fp, comm_fp],
        "Floors": [serv_floors, serv_floors],
        "Mix BUA (SQM)": [admin_bua, comm_bua]
    })
    st.dataframe(df_serv.style.format({
        "Plot Mix %": "{:.1%}",
        "Mix Plots (SQM)": "{:,.2f}",
        "Coverage": "{:.1%}",
        "Actual Footprint (SQM)": "{:,.2f}",
        "Mix BUA (SQM)": "{:,.2f}"
    }), use_container_width=True)

elif active_tab == "Prototypes Analysis":
    df_proto = pd.DataFrame({
        "Building Prototype": ["Type Solo Homes", "Type T", "New Type"],
        "Prototype %": [0.0, 0.30, 0.70],
        "Footprint (SQM)": [486, 1059, 1200],
        "Floors": [5, 5, 5],
        "BUA per Unit": [2430, 5295, 6000]
    })
    st.dataframe(df_proto, use_container_width=True)

elif active_tab == "New Type Analysis":
    net_bua = apt_bua * 0.70
    df_nt = pd.DataFrame({
        "Product Mix": ["Studio", "1BR", "2BR", "3BR", "4BR"],
        "Mix %": [studio_pct, one_br_pct, two_br_pct, three_br_pct, 0.0],
        "Avg Net Area (SQM)": [50, 100, 130, 160, 200],
        "Estimated Keys": [
            (net_bua * studio_pct) / 50 if studio_pct > 0 else 0,
            (net_bua * one_br_pct) / 100 if one_br_pct > 0 else 0,
            (net_bua * two_br_pct) / 130 if two_br_pct > 0 else 0,
            (net_bua * three_br_pct) / 160 if three_br_pct > 0 else 0,
            0
        ]
    })
    st.dataframe(df_nt.style.format({"Mix %": "{:.1%}", "Estimated Keys": "{:,.1f}"}), use_container_width=True)

elif active_tab == "Parking Calculations":
    col1, col2 = st.columns(2)
    surface_parking = col1.number_input("Surface Level Parking Slots", value=5000, step=500)
    req_basement_pct = (nla_sqm * 0.0272) / nla_sqm if nla_sqm > 0 else 0
    col2.metric("Required Basement Ratio %", f"{req_basement_pct*100:.2f}%")
    st.info(f"Surface Parking Capacity: {surface_parking:,} slots | Estimated Basement Requirement: {nla_sqm * 2.72:,.2f} SQM")

elif active_tab == "Summary Results":
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("### BUA Performance")
        st.metric("Total Achieved BUA", f"{total_achieved_bua:,.2f} SQM")
        st.metric("Total Remaining BUA", f"{rem_bua:,.2f} SQM")
        st.metric("Achieved % from Allowed BUA", f"{achieved_bua_pct*100:.2f}%")

    with res_col2:
        st.markdown("### Footprint & FAR Performance")
        st.metric("Total Achieved Footprint", f"{total_achieved_fp:,.2f} SQM")
        st.metric("Total Remaining Footprint", f"{rem_fp:,.2f} SQM")
        st.metric("Achieved FAR", f"{achieved_far:.2f}")
```

---

### What to do next:
1. Apply the diff above to your `app.py` file.
2. Commit and push `app.py` to your GitHub repository.
3. Streamlit Cloud will update automatically. Selecting any section in the sidebar will immediately filter the inputs and display the relevant calculations on screen!
