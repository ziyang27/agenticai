import streamlit as st
from components.savings_recommender import render_savings_recommender
from components.income_expense_tracker import render_income_expense_tracker
from components.visualization import render_visualization
from components.tips_review import render_tips_review

# Page config
st.set_page_config(page_title="BudgetBuddy Pro", page_icon="💸", layout="wide")

st.title("💰 BudgetBuddy Pro")
st.caption("Complete Financial Planning for Test User")

# Create tabs for the 4 sections
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Savings Target", 
    "📊 Monthly Tracking", 
    "📈 Visualization", 
    "💡 Tips & Review"
])

with tab1:
    render_savings_recommender()

with tab2:
    render_income_expense_tracker()

with tab3:
    render_visualization()

with tab4:
    render_tips_review()