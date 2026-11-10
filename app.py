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
        
        # Recalculate GLA SQM based on input
        if st.session_state.unit_mode == "Feddans":
            base_sqm = entered_val * FEDDAN_TO_SQM
        else:
            base_sqm = entered_val

        if st.session_state.input_mode == "NLA":
            st.session_state.gla_sqm = base_sqm / max(0.01, st.session_state.efficiency)
        else:
            st.session_state.gla_sqm = base_sqm

        st.session_state.land_type = st.selectbox(
            "Land Type", 
            ["Mixed Use", "Residential", "Commercial", "Hospitality"], 
            index=0
        )
