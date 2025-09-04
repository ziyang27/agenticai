import streamlit as st
import sys
import os
import re

# Add the parent directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agent import BudgetBuddyAgent
from .utils.storage import get_profile, get_all_months_data, update_profile

def render_tips_review():
    st.header("💡 AI-Powered Financial Analysis")
    
    # Initialize session state for persistent data
    if 'analysis_generated' not in st.session_state:
        st.session_state.analysis_generated = False
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'show_adjustment' not in st.session_state:
        st.session_state.show_adjustment = False
    
    # Initialize agent
    @st.cache_resource
    def load_agent():
        try:
            return BudgetBuddyAgent()
        except Exception as e:
            st.error(f"❌ Failed to initialize AI agent: {str(e)}")
            return None
    
    agent = load_agent()
    
    # Get available data
    try:
        profile = get_profile() or {}
        all_months = get_all_months_data() or {}
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        profile = {}
        all_months = {}
    
    # Check what data we have
    has_profile = bool(profile and any(profile.values()))
    has_monthly_data = bool(all_months and any(
        month.get('completed', False) for month in all_months.values()
    ))
    
    # Display current target
    current_target = profile.get('monthly_savings_target', 0)
    if current_target > 0:
        st.metric("Current Monthly Savings Target", f"${current_target:,.2f}")
    
    if not has_profile and not has_monthly_data:
        st.info("""
        📋 **Get started:**
        1. Set up your savings target in the **🎯 Savings Target** tab
        2. Track your income/expenses in the **📊 Monthly Tracking** tab
        3. Return here for personalized AI analysis!
        """)
        return
    
    # Analysis options
    st.subheader("🔍 Select Analysis Type")
    analysis_type = st.radio(
        "Choose analysis focus:",
        ["Comprehensive Review", "Savings Strategy", "Expense Optimization", "Retirement Planning"],
        horizontal=True,
        key="analysis_type_selector"
    )
    
    # Generate analysis button
    if st.button("🚀 Generate AI Analysis", type="primary", use_container_width=True, key="generate_analysis_btn"):
        with st.spinner("🧠 Analyzing your financial situation..."):
            analysis_result = generate_analysis_content(agent, analysis_type, profile, all_months)
            st.session_state.analysis_generated = True
            st.session_state.current_analysis = analysis_result
            st.session_state.show_adjustment = analysis_result.get('has_recommendation', False)
            st.rerun()
    
    # Display analysis results if they exist
    if st.session_state.analysis_generated and st.session_state.current_analysis:
        display_analysis_results(st.session_state.current_analysis)
        
        # Show adjustment section if recommended
        if st.session_state.show_adjustment:
            render_savings_adjustment_section(
                st.session_state.current_analysis['recommended_amount'],
                profile
            )

def generate_analysis_content(agent, analysis_type, profile, all_months):
    """Generate analysis content and return as dictionary"""
    try:
        context = build_financial_context(profile, all_months)
        prompt = create_analysis_prompt(context, analysis_type)
        
        if not agent:
            return {
                'type': analysis_type,
                'response': "AI agent not available. Please check your AWS configuration.",
                'has_recommendation': False,
                'recommended_amount': None
            }
        
        response = agent.run(prompt)
        recommended_amount = extract_savings_recommendation(response)
        
        return {
            'type': analysis_type,
            'response': response,
            'has_recommendation': recommended_amount is not None,
            'recommended_amount': recommended_amount
        }
        
    except Exception as e:
        return {
            'type': analysis_type,
            'response': f"Error generating analysis: {str(e)}",
            'has_recommendation': False,
            'recommended_amount': None
        }

def build_financial_context(profile, all_months):
    """Build context string from available data"""
    context = "USER'S FINANCIAL CONTEXT:\n\n"
    
    if profile:
        context += "👤 PROFILE:\n"
        context += f"- Age: {profile.get('current_age', 'Not set')}\n"
        context += f"- Retirement Goal: {profile.get('retirement_age', 'Not set')}\n"
        context += f"- Monthly Income: ${profile.get('current_income', 0):,.2f}\n"
        context += f"- Risk Tolerance: {profile.get('risk_tolerance', 'Not set')}\n"
        context += f"- Monthly Savings Target: ${profile.get('monthly_savings_target', 0):,.2f}\n\n"
    
    if all_months:
        completed_months = [month for month in all_months.values() if month.get('completed')]
        if completed_months:
            context += "📊 MONTHLY SUMMARY:\n"
            total_actual = sum(month.get('savings', {}).get('actual', 0) for month in completed_months)
            total_target = sum(month.get('savings', {}).get('target', 0) for month in completed_months)
            avg_income = sum(month.get('income', {}).get('total', 0) for month in completed_months) / len(completed_months)
            avg_expenses = sum(month.get('expenses', {}).get('total', 0) for month in completed_months) / len(completed_months)
            
            context += f"- Tracked Months: {len(completed_months)}\n"
            context += f"- Total Savings: ${total_actual:,.2f} of ${total_target:,.2f} target\n"
            context += f"- Avg Monthly Income: ${avg_income:,.2f}\n"
            context += f"- Avg Monthly Expenses: ${avg_expenses:,.2f}\n"
            context += f"- Avg Monthly Savings: ${(total_actual/len(completed_months)):,.2f}\n\n"
    
    return context

def create_analysis_prompt(context, analysis_type):
    """Create prompt for specific analysis type with explicit savings target request"""
    prompts = {
        "Comprehensive Review": """
        Provide a complete financial health assessment. Include:
        - Overall financial health score (1-10)
        - 3 strengths and 3 areas for improvement
        - Specific action items for the next 30 days
        - Long-term strategy recommendations
        - SPECIFIC SAVINGS TARGET RECOMMENDATION: Provide an exact dollar amount for a new monthly savings target
        """,
        
        "Savings Strategy": """
        Focus on savings optimization. Include:
        - Analysis of current savings rate vs recommended
        - 5 specific ways to increase savings
        - Ideal savings allocation based on risk profile
        - Emergency fund recommendations
        - SPECIFIC SAVINGS TARGET RECOMMENDATION: Provide an exact dollar amount for a new monthly savings target
        """,
        
        "Expense Optimization": """
        Focus on expense reduction. Include:
        - Top 3 expense categories to target
        - Practical cost-cutting strategies for each
        - Subscription audit recommendations
        - Lifestyle inflation warnings
        - SPECIFIC SAVINGS TARGET RECOMMENDATION: Provide an exact dollar amount that could be saved monthly
        """,
        
        "Retirement Planning": """
        Focus on retirement preparation. Include:
        - Projected retirement savings at current rate
        - Gap analysis vs retirement needs
        - Investment strategy adjustments
        - Retirement account optimization
        - SPECIFIC SAVINGS TARGET RECOMMENDATION: Provide an exact dollar amount needed for retirement goals
        """
    }
    
    return f"""
    {context}
    
    ANALYSIS REQUEST: {analysis_type}
    
    {prompts.get(analysis_type, 'Provide comprehensive financial advice')}
    
    CRITICAL: When suggesting savings target changes, ALWAYS provide:
    - Exact dollar amount (e.g., $1,250 instead of "increase by 25%")
    - Clear rationale for the change
    - Specific implementation steps
    - Follow a strict format for easy extraction: NEW SAVINGS TARGET: $<amount>
    
    Please provide:
    - Specific, actionable recommendations with examples
    - Quantitative estimates where possible ($ amounts, percentages)
    - Risk assessments and warnings
    - Clear formatting with bullet points and sections
    - Keep within 200 words
    """

def extract_savings_recommendation(response):
    """Extract savings target recommendation from AI response"""
    match = re.search(r'NEW SAVINGS TARGET:\s*\$([\d,]+(?:\.\d{2})?)', str(response))
    if match:
        amount_str = match.group(1).replace(',', '')
        try:
            return float(amount_str)
        except ValueError:
            return None
    return None

def display_analysis_results(analysis_data):
    """Display analysis results from session state"""
    st.subheader(f"📋 {analysis_data['type']} Analysis")
    st.markdown("---")
    
    # Highlight dollar amounts in the response
    highlighted_response = str(analysis_data['response'])
    dollar_matches = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', highlighted_response)
    for match in dollar_matches:
        highlighted_response = highlighted_response.replace(
            match, f"**{match}**"
        )
    
    with st.container():
        st.markdown(highlighted_response)
    
    st.success("✅ AI analysis completed!")

def render_savings_adjustment_section(recommended_amount, current_profile):
    """Render savings adjustment section"""
    st.markdown("---")
    st.subheader("🎯 Savings Target Adjustment")
    
    current_target = current_profile.get('monthly_savings_target', 0)
    
    # Show comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Target", f"${current_target:,.2f}")
    
    with col2:
        st.metric("AI Recommended", f"${recommended_amount:,.2f}")
    
    with col3:
        difference = recommended_amount - current_target
        st.metric("Difference", f"${difference:,.2f}", 
                 f"{difference/current_target*100:+.1f}%" if current_target > 0 else "+0%")
    
    # Adjustment form
    with st.form(key="savings_adjustment_form"):
        st.markdown("### Adjust Your Monthly Savings Target")
        
        # Set reasonable max value
        max_value = max(recommended_amount * 1.5, current_target * 2, 5000)
        
        new_target = st.slider(
            "Set new monthly target:",
            min_value=0.0,
            max_value=float(max_value),
            value=float(recommended_amount),
            step=50.0,
            format="$%.2f",
            key="savings_target_slider"
        )
        
        # Show change percentage
        if current_target > 0:
            change_percent = ((new_target - current_target) / current_target) * 100
            st.info(f"This is a {change_percent:+.1f}% change from your current target")
        
        # Submit button
        submitted = st.form_submit_button("💾 Apply New Savings Target", type="primary")
        
        if submitted:
            # Update the profile
            updated_profile = current_profile.copy()
            updated_profile['monthly_savings_target'] = new_target
            update_profile(updated_profile)
            
            st.success(f"✅ Savings target updated to ${new_target:,.2f} per month!")
            st.session_state.profile_updated = True
            st.session_state.show_adjustment = True