import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
from .utils.storage import get_all_months_data, get_profile

def render_visualization():
    st.header("📈 Savings Visualization & Progress Tracking")
    
    profile = get_profile()
    monthly_target = profile.get("monthly_savings_target", 0)
    all_months = get_all_months_data()
    
    # Prepare data for visualization
    months = list(calendar.month_name[1:])
    current_year = "2024"
    
    data = []
    for month in months:
        month_key = f"{month.lower()}_{current_year}"
        month_data = all_months.get(month_key, {})
        savings_data = month_data.get("savings", {})
        
        actual = savings_data.get("actual", 0)
        target = savings_data.get("target", monthly_target)
        difference = actual - target
        
        data.append({
            'Month': month,
            'Target Savings': target,
            'Actual Savings': actual,
            'Difference': difference,
            'Status': 'On Target' if actual >= target else 'Below Target',
            'Completed': month_data.get("completed", False)
        })
    
    df = pd.DataFrame(data)
    
    # Summary metrics
    total_target = df['Target Savings'].sum()
    total_actual = df['Actual Savings'].sum()
    yearly_difference = total_actual - total_target
    completion_rate = (df['Completed'].sum() / len(df)) * 100
    
    # Display summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Yearly Target", f"${total_target:,.2f}")
    with col2:
        st.metric("Yearly Actual", f"${total_actual:,.2f}")
    with col3:
        st.metric("Yearly Difference", f"${yearly_difference:,.2f}", 
                 delta_color="inverse" if yearly_difference < 0 else "normal")
    with col4:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = px.bar(df, x='Month', y=['Target Savings', 'Actual Savings'],
                    title='Monthly Savings: Target vs Actual', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Difference chart
        fig = px.bar(df, x='Month', y='Difference', color='Status',
                    title='Monthly Savings Difference',
                    color_discrete_map={'On Target': 'green', 'Below Target': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Progress table
    st.subheader("Monthly Progress Overview")
    display_df = df.copy()
    display_df['Target Savings'] = display_df['Target Savings'].apply(lambda x: f"${x:,.2f}")
    display_df['Actual Savings'] = display_df['Actual Savings'].apply(lambda x: f"${x:,.2f}")
    display_df['Difference'] = display_df['Difference'].apply(lambda x: f"${x:,.2f}")
    display_df['Status'] = display_df['Status'].apply(lambda x: f"✅ {x}" if x == 'On Target' else f"⚠️ {x}")
    
    st.dataframe(display_df, use_container_width=True)