import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Page Configuration & Dark Executive Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Madinet Masr - Land Feasibility Calculator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Force all text white for maximum readability on dark background */
    .stApp, .stText, .stMarkdown, p, span, label, div, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    .stApp {
        background-color: #000000 !important;
    }
    .stSidebar {
        background-color: #111111 !important;
        border-right: 1px solid #222222 !important;
    }
    .brand-title {
        font-size: 1.8rem;
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    .stMetric {
        background-color: #111111 !important;
        border: 1px solid #222222 !important;
        padding: 12px !important;
        border-radius: 8px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
    }
    .dataframe {
        color: #FFFFFF !important;
        background-color: #111111 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header & Branding Section (Centered Logo & Land Engine Title)
# ---------------------------------------------------------
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    try:
        st.image("LOGO.png", width=280)
    except Exception:
        st.markdown('<div style="font-size: 2rem; font-weight: 800; color: #FFFFFF; text-align: center;">MADINET MASR</div>', unsafe_allow_html=True)

st.markdown('<div class="brand-title">Land Engine</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------------
# Sidebar Inputs (RED CELLS ONLY from Excel)
# ---------------------------------------------------------
st.sidebar.markdown("### 🔴 Input Parameters (Red Cells)")

# Dynamic Area Conversions Engine with Session State Persistence
st.sidebar.subheader("1. Land Data Input Mode")

SQM_PER_FEDDAN = 4200.0

# Initialize persistent session state variables
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

# Handle persistent values during mode toggles
if input_type == "GLA":
    if unit_type == "Feddans":
        current_gla_feddans = st.session_state.gla_sqm_val / SQM_PER_FEDDAN
        gla_feddans = st.sidebar.number_input("GLA in feddans", value=float(current_gla_feddans), step=1.0, format="%.5f")
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
        nla_feddans = st.sidebar.number_input("NLA in feddans", value=float(current_nla_feddans), step=1.0, format="%.5f")
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

st.sidebar.subheader("2. Land Analysis Breakdown")
res_pct_nla = st.sidebar.slider("Residential % from NLA", 0.0, 1.0, 0.50, 0.01)
serv_pct_nla = st.sidebar.slider("Services % from NLA", 0.0, 1.0, 0.15, 0.01)
landscape_pct_nla = max(0.0, 1.0 - res_pct_nla - serv_pct_nla)

res_plot_pct = st.sidebar.slider("Residential Plot % from Total Land", 0.0, 1.0, 0.50, 0.01)
serv_plot_pct = st.sidebar.slider("Services Plot % from Total Land", 0.0, 1.0, 0.30, 0.01)

st.sidebar.subheader("3. Land Constraints")
res_floors = st.sidebar.number_input("Residential Floors", value=5, step=1)
serv_floors = st.sidebar.number_input("Services Floors", value=4, step=1)
allowed_fp_pct = st.sidebar.number_input("Allowed Footprint %", value=0.25, step=0.01)
allowed_far = st.sidebar.number_input("Allowed FAR", value=1.25, step=0.05)
design_contingency = st.sidebar.number_input("Design Contingency", value=0.0, step=0.01)

st.sidebar.subheader("4. Residential Plot Mix")
apt_mix = st.sidebar.slider("Apartments Mix %", 0.0, 1.0, 0.60, 0.05)
villa_mix = st.sidebar.slider("Villas Mix %", 0.0, 1.0, 0.10, 0.05)
th_mix = st.sidebar.slider("Townhouses Mix %", 0.0, 1.0, 0.30, 0.05)

st.sidebar.subheader("5. Services Plot Mix")
admin_mix = st.sidebar.slider("Admin Mix %", 0.0, 1.0, 0.50, 0.05)
comm_mix = 1.0 - admin_mix

st.sidebar.subheader("6. New Type Product Mix")
studio_pct = st.sidebar.slider("Studio Mix %", 0.0, 1.0, 0.30, 0.05)
one_br_pct = st.sidebar.slider("1BR Mix %", 0.0, 1.0, 0.40, 0.05)
two_br_pct = st.sidebar.slider("2BR Mix %", 0.0, 1.0, 0.20, 0.05)
three_br_pct = max(0.0, 1.0 - studio_pct - one_br_pct - two_br_pct)

# ---------------------------------------------------------
# Core Real-Time Calculation Engine
# ---------------------------------------------------------
total_res_land = nla_sqm * res_pct_nla
total_res_plots = total_res_land * res_plot_pct
total_serv_land = nla_sqm * serv_pct_nla
total_serv_plots = total_serv_land * serv_plot_pct
total_landscape_land = nla_sqm * landscape_pct_nla

allowed_footprint = gla_sqm * allowed_fp_pct
allowed_bua = gla_sqm * allowed_far

res_plots_after_cont = total_res_plots * (1.0 - design_contingency)
serv_plots_after_cont = total_serv_plots * (1.0 - design_contingency)

apt_plots = res_plots_after_cont * apt_mix
villa_plots = res_plots_after_cont * villa_mix
th_plots = res_plots_after_cont * th_mix

apt_fp = apt_plots * 0.5
villa_fp = villa_plots * 0.4
th_fp = th_plots * 0.4

apt_bua = apt_fp * res_floors
villa_bua = villa_fp * 2.25
th_bua = th_fp * 2.5

res_subtotal_bua = apt_bua + villa_bua + th_bua
local_services_land = total_res_land * 0.02
total_res_achieved_bua = res_subtotal_bua + local_services_land

admin_plots = serv_plots_after_cont * admin_mix
comm_plots = serv_plots_after_cont * comm_mix

admin_fp = admin_plots * 0.3
comm_fp = comm_plots * 0.3

admin_bua = admin_fp * serv_floors
comm_bua = comm_fp * serv_floors

total_serv_achieved_bua = admin_bua + comm_bua
total_serv_achieved_fp = admin_fp + comm_fp

total_achieved_bua = total_res_achieved_bua + total_serv_achieved_bua
total_achieved_fp = (apt_fp + villa_fp + th_fp + local_services_land) + total_serv_achieved_fp

rem_bua = allowed_bua - total_achieved_bua
rem_fp = allowed_footprint - total_achieved_fp
achieved_bua_pct = total_achieved_bua / allowed_bua if allowed_bua > 0 else 0
achieved_fp_pct = total_achieved_fp / allowed_footprint if allowed_footprint > 0 else 0
achieved_far = total_achieved_bua / gla_sqm if gla_sqm > 0 else 0

# ---------------------------------------------------------
# Real-Time Validation & Checker Alerts
# ---------------------------------------------------------
nla_sum = res_pct_nla + serv_pct_nla + landscape_pct_nla
res_mix_sum = apt_mix + villa_mix + th_mix
new_type_sum = studio_pct + one_br_pct + two_br_pct + three_br_pct

if abs(nla_sum - 1.0) > 0.001:
    st.error(f"⚠️ **NLA Allocation Error:** The sum of Residential, Services, and Landscape percentages is **{nla_sum*100:.1f}%**. It must equal 100%.")

if abs(res_mix_sum - 1.0) > 0.001:
    st.warning(f"⚠️ **Residential Mix Constraint:** Current residential plot mix sum is **{res_mix_sum*100:.1f}%**. Adjust sliders to total 100%.")

if abs(new_type_sum - 1.0) > 0.001:
    st.warning(f"⚠️ **New Type Mix Constraint:** Apartment mix sum is **{new_type_sum*100:.1f}%**. Adjust to hit 100%.")

if total_achieved_bua > allowed_bua:
    st.error(f"🚨 **Zoning Constraint Violation:** Achieved BUA ({total_achieved_bua:,.0f} SQM) exceeds Allowed BUA ({allowed_bua:,.0f} SQM)!")

# ---------------------------------------------------------
# Dynamic Excel-Aligned Navigation Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Land Data", 
    "Land Analysis", 
    "Land Constraints", 
    "Residential Mix", 
    "Services Mix", 
    "Prototypes Analysis", 
    "New Type Analysis", 
    "Parking Calculations", 
    "Summary Results"
])

with tab1:
    st.subheader("Land Data")
    c1, c2, c3 = st.columns(3)
    c1.metric("GLA (Feddans)", f"{gla_feddans:,.2f}")
    c2.metric("GLA (SQM)", f"{gla_sqm:,.2f}")
    c3.metric("Efficiency Ratio", f"{efficiency*100:.1f}%")
    
    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    c4.metric("NLA (Feddans)", f"{nla_feddans:,.2f}")
    c5.metric("NLA (SQM)", f"{nla_sqm:,.2f}")
    c6.metric("Land Type", land_type)

with tab2:
    st.subheader("Land Analysis")
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

with tab3:
    st.subheader("Land Constraints")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Allowed Footprint %", f"{allowed_fp_pct*100:.1f}%")
    c2.metric("Allowed Footprint (SQM)", f"{allowed_footprint:,.2f}")
    c3.metric("Allowed BUA (SQM)", f"{allowed_bua:,.2f}")
    c4.metric("Allowed FAR", f"{allowed_far:.2f}")

with tab4:
    st.subheader("Residential Mix")
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

with tab5:
    st.subheader("Services Mix")
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

with tab6:
    st.subheader("Residential Prototypes Analysis")
    df_proto = pd.DataFrame({
        "Building Prototype": ["Type Solo Homes", "Type T", "New Type"],
        "Prototype %": [0.0, 0.30, 0.70],
        "Footprint (SQM)": [486, 1059, 1200],
        "Floors": [5, 5, 5],
        "BUA per Unit": [2430, 5295, 6000]
    })
    st.dataframe(df_proto, use_container_width=True)

with tab7:
    st.subheader("New Type Analysis")
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

with tab8:
    st.subheader("Residential Parking Calculations")
    col1, col2 = st.columns(2)
    surface_parking = col1.number_input("Surface Level Parking Slots", value=5000, step=500)
    req_basement_pct = (nla_sqm * 0.0272) / nla_sqm if nla_sqm > 0 else 0
    col2.metric("Required Basement Ratio %", f"{req_basement_pct*100:.2f}%")
    st.info(f"Surface Parking Capacity: {surface_parking:,} slots | Estimated Basement Requirement: {nla_sqm * 2.72:,.2f} SQM")

with tab9:
    st.subheader("🔴 Calculation Results (Dark Red Summary)")
    
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
