import streamlit as st
from .utils.storage import get_profile, update_profile

def render_savings_recommender():
    st.header("🎯 Recommended Monthly Savings")
    
    # Load profile data
    profile = get_profile()
    
    with st.form("savings_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            current_age = st.number_input("Current Age", min_value=18, max_value=70, 
                                        value=profile.get("current_age", 25))
            retirement_age = st.number_input("Target Retirement Age", min_value=50, max_value=80, 
                                           value=profile.get("retirement_age", 65))
            current_income = st.number_input("Current Monthly Income ($)", min_value=0, 
                                           value=profile.get("current_income", 5000), step=500)
        
        with col2:
            current_savings = st.number_input("Current Total Savings ($)", min_value=0, 
                                            value=profile.get("current_savings", 10000), step=1000)
            risk_tolerance = st.selectbox("Risk Tolerance", 
                                        ["Conservative", "Moderate", "Aggressive"],
                                        index=["Conservative", "Moderate", "Aggressive"].index(
                                            profile.get("risk_tolerance", "Moderate")))
            inflation_rate = st.number_input("Expected Inflation Rate (%)", min_value=0.0, 
                                           value=profile.get("inflation_rate", 2.5), step=0.1)
        
        # Calculate recommended savings (simplified)
        years_to_retirement = retirement_age - current_age
        recommended_monthly = current_income * 0.20  # 20% of income
        
        # Button to calculate based on a simple rule of thumb
        if st.form_submit_button("Calculate Recommended Savings"):
            st.metric("Recommended Monthly Savings", f"${recommended_monthly:,.2f}")
        
        # User can adjust the target
        monthly_target = st.number_input("Your Monthly Savings Target ($)", min_value=0, 
                                    value=profile.get("monthly_savings_target", int(recommended_monthly)), 
                                    step=100)
        
        if st.form_submit_button("Save Profile & Target"):
            updated_profile = {
                "current_age": current_age,
                "retirement_age": retirement_age,
                "current_income": current_income,
                "current_savings": current_savings,
                "risk_tolerance": risk_tolerance,
                "inflation_rate": inflation_rate,
                "monthly_savings_target": monthly_target
            }
        
            update_profile(updated_profile)
            st.success("Profile and savings target updated successfully!")