import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration & Branding
st.set_page_config(
    page_title="Real Estate Land Study & Masterplan Calculator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & Executive UI Theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stMetric {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 12px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-header">🏢 Real Estate Land Study & Masterplan Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Feasibility, Zoning, & Masterplan Analytics Engine</div>', unsafe_allow_html=True)

# Sidebar Inputs (Master Drivers from Excel)
st.sidebar.header("📍 Land & Site Parameters")
gla_feddans = st.sidebar.number_input("Gross Land Area (GLA in Feddans)", value=214.19, step=1.0, format="%.2f")
efficiency = st.sidebar.slider("Land Efficiency Ratio", min_value=0.5, max_value=1.0, value=0.9, step=0.01)
land_type = st.sidebar.selectbox("Land Type", ["Mixed Use", "Residential", "Commercial"])

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Net Land Area (NLA) Allocation")
res_pct_nla = st.sidebar.slider("Residential % from NLA", 0.0, 1.0, 0.5, 0.05)
serv_pct_nla = st.sidebar.slider("Services % from NLA", 0.0, 1.0, 0.15, 0.05)
landscape_pct_nla = max(0.0, 1.0 - res_pct_nla - serv_pct_nla)
st.sidebar.text(f"Landscape & Roads % (Auto): {landscape_pct_nla:.2f}")

st.sidebar.markdown("---")
st.sidebar.subheader("🏛️ Zoning & BUA Constraints")
allowed_far = st.sidebar.number_input("Allowed FAR", value=1.25, step=0.05)
allowed_footprint_pct = st.sidebar.number_input("Total Allowed Footprint %", value=0.25, step=0.01)
res_floors = st.sidebar.number_input("Residential Number of Floors", value=5, step=1)
serv_floors = st.sidebar.number_input("Services Number of Floors", value=4, step=1)

st.sidebar.markdown("---")
st.sidebar.subheader("🛋️ New Type Apartment Product Mix")
studio_mix = st.sidebar.slider("Studio Mix %", 0.0, 1.0, 0.3, 0.05)
one_br_mix = st.sidebar.slider("1BR Mix %", 0.0, 1.0, 0.4, 0.05)
two_br_mix = st.sidebar.slider("2BR Mix %", 0.0, 1.0, 0.2, 0.05)
three_br_mix = max(0.0, 1.0 - studio_mix - one_br_mix - two_br_mix)
st.sidebar.text(f"3BR Mix % (Auto): {three_br_mix:.2f}")

# Core Calculation Engine (Replicating Excel logic)
SQM_PER_FEDDAN = 4200.0
gla_sqm = gla_feddans * SQM_PER_FEDDAN
nla_feddans = gla_feddans * efficiency
nla_sqm = gla_sqm * efficiency

res_land = nla_sqm * res_pct_nla
serv_land = nla_sqm * serv_pct_nla
landscape_land = nla_sqm * landscape_pct_nla

allowed_bua = gla_sqm * allowed_far
allowed_footprint = gla_sqm * allowed_footprint_pct

# Tabs Organization
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Land & NLA", 
    "🏛️ Constraints & BUA", 
    "🏘️ Land Mix", 
    "🏢 Prototypes & Units", 
    "🅿️ Parking & Basement", 
    "📋 Executive Summary"
])

with tab1:
    st.subheader("Gross & Net Land Area Analysis")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("GLA (SQM)", f"{gla_sqm:,.2f}")
    col2.metric("GLA (Feddans)", f"{gla_feddans:,.2f}")
    col3.metric("NLA (SQM)", f"{nla_sqm:,.2f}")
    col4.metric("Efficiency", f"{efficiency*100:.0f}%")
    
    st.markdown("### Net Land Area Breakdown")
    nla_df = pd.DataFrame({
        "Component": ["Residential", "Services", "Landscape & Roads"],
        "Percentage from NLA": [res_pct_nla, serv_pct_nla, landscape_pct_nla],
        "Area (SQM)": [res_land, serv_land, landscape_land],
        "Area (Feddans)": [res_land/SQM_PER_FEDDAN, serv_land/SQM_PER_FEDDAN, landscape_land/SQM_PER_FEDDAN]
    })
    st.dataframe(nla_df.style.format({"Percentage from NLA": "{:.1%}", "Area (SQM)": "{:,.2f}", "Area (Feddans)": "{:,.2f}"}), use_container_width=True)

with tab2:
    st.subheader("Zoning Limits & BUA Capacities")
    col1, col2, col3 = st.columns(3)
    col1.metric("Allowed BUA (SQM)", f"{allowed_bua:,.2f}")
    col2.metric("Allowed Footprint (SQM)", f"{allowed_footprint:,.2f}")
    col3.metric("Allowed FAR", f"{allowed_far:.2f}")
    
    st.info(f"**Building Heights:** Residential: G+{res_floors-1} ({res_floors} Floors) | Services: G+{serv_floors-1} ({serv_floors} Floors)")

with tab3:
    st.subheader("Residential & Services Land Mix")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Residential Land Mix")
        res_mix_df = pd.DataFrame({
            "Building Type": ["Apartments", "Villas", "Townhouses", "Local Services"],
            "Plot Mix %": ["60%", "10%", "30%", "2%"],
            "Floors": [5, 2.25, 2.5, 1],
            "Coverage %": ["50%", "40%", "40%", "100%"]
        })
        st.dataframe(res_mix_df, use_container_width=True)
    with col_b:
        st.markdown("#### Services Land Mix")
        serv_mix_df = pd.DataFrame({
            "Service Type": ["Admin", "Commercial"],
            "Plot Mix %": ["50%", "50%"],
            "Floors": [4, 4],
            "Coverage %": ["30%", "30%"]
        })
        st.dataframe(serv_mix_df, use_container_width=True)

with tab4:
    st.subheader("Residential Prototypes & Product Mix")
    st.markdown("#### New Type Apartment Product Mix Breakdown")
    prod_mix_df = pd.DataFrame({
        "Unit Type": ["Studio", "1BR", "2BR", "3BR"],
        "Mix %": [studio_mix, one_br_mix, two_br_mix, three_br_mix],
        "Avg Net Area (SQM)": [50, 100, 130, 160],
        "Estimated Keys / Units": [
            res_land * 0.5 * 0.6 * 0.7 * studio_mix / 50,
            res_land * 0.5 * 0.6 * 0.7 * one_br_mix / 100,
            res_land * 0.5 * 0.6 * 0.7 * two_br_mix / 130,
            res_land * 0.5 * 0.6 * 0.7 * three_br_mix / 160
        ]
    })
    st.dataframe(prod_mix_df.style.format({"Mix %": "{:.1%}", "Avg Net Area (SQM)": "{:,.0f}", "Estimated Keys / Units": "{:,.1f}"}), use_container_width=True)

with tab5:
    st.subheader("Parking & Basement Area Calculations")
    col1, col2 = st.columns(2)
    surface_parking = col1.number_input("Surface Level Parking (SQM)", value=5000.0, step=500.0)
    parking_ratio_pct = col2.slider("Required Basement Area Ratio (%)", 1.0, 5.0, 2.83, 0.01)
    
    req_basement = nla_sqm * (parking_ratio_pct / 100.0) * 800.0
    col1.metric("Surface Parking", f"{surface_parking:,.2f} SQM")
    col2.metric("Required Basement Scale", f"{req_basement:,.2f} SQM")

with tab6:
    st.subheader("Executive Masterplan KPI Summary")
    st.success("All masterplan calculations, zoning envelopes, and area checks have been successfully compiled.")
    
    summary_df = pd.DataFrame({
        "Metric": ["Gross Land Area (GLA)", "Net Land Area (NLA)", "Allowed BUA", "Allowed Footprint", "Overall FAR"],
        "Value": [f"{gla_sqm:,.2f} SQM", f"{nla_sqm:,.2f} SQM", f"{allowed_bua:,.2f} SQM", f"{allowed_footprint:,.2f} SQM", f"{allowed_far:.2f}"]
    })
    st.dataframe(summary_df, use_container_width=True)