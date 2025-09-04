import streamlit as st
from .utils.storage import get_month_data, update_month_data, get_profile
import calendar

def render_income_expense_tracker():
    st.header("📊 Monthly Income & Expense Tracking")
    
    # Get current year and months
    current_year = "2024"
    months = list(calendar.month_name[1:])
    
    # Create tabs for each month
    month_tabs = st.tabs(months)
    
    for i, month_tab in enumerate(month_tabs):
        month_name = months[i]
        month_key = f"{month_name.lower()}_{current_year}"
        
        with month_tab:
            st.subheader(f"{month_name} {current_year}")
            
            # Load existing data for this month
            month_data = get_month_data(month_key)
            income_data = month_data.get("income", {})
            expenses_data = month_data.get("expenses", {})
            savings_data = month_data.get("savings", {})
            
            with st.form(key=f"form_{month_key}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**💰 Income Sources**")
                    salary = st.number_input("Salary/Wages", min_value=0.0, 
                                          value=income_data.get("salary", 0.0), 
                                          key=f"salary_{month_key}", step=100.0)
                    investment = st.number_input("Investment Income", min_value=0.0, 
                                              value=income_data.get("investment", 0.0),
                                              key=f"investment_{month_key}", step=50.0)
                    other_income = st.number_input("Other Income", min_value=0.0, 
                                                 value=income_data.get("other_income", 0.0),
                                                 key=f"other_income_{month_key}", step=50.0)
                    total_income = salary + investment + other_income
                    st.metric("Total Income", f"${total_income:,.2f}")
                
                with col2:
                    st.markdown("**💸 Expenses**")
                    rent = st.number_input("Rent/Mortgage", min_value=0.0,
                                         value=expenses_data.get("rent", 0.0),
                                         key=f"rent_{month_key}", step=100.0)
                    groceries = st.number_input("Groceries", min_value=0.0,
                                              value=expenses_data.get("groceries", 0.0),
                                              key=f"groceries_{month_key}", step=50.0)
                    transportation = st.number_input("Transportation", min_value=0.0,
                                                   value=expenses_data.get("transportation", 0.0),
                                                   key=f"transportation_{month_key}", step=50.0)
                    utilities = st.number_input("Utilities", min_value=0.0,
                                              value=expenses_data.get("utilities", 0.0),
                                              key=f"utilities_{month_key}", step=50.0)
                    entertainment = st.number_input("Entertainment", min_value=0.0,
                                                  value=expenses_data.get("entertainment", 0.0),
                                                  key=f"entertainment_{month_key}", step=50.0)
                    other_expenses = st.number_input("Other Expenses", min_value=0.0,
                                                   value=expenses_data.get("other_expenses", 0.0),
                                                   key=f"other_expenses_{month_key}", step=50.0)
                    total_expenses = rent + groceries + transportation + utilities + entertainment + other_expenses
                    st.metric("Total Expenses", f"${total_expenses:,.2f}")
                
                # Savings section
                st.markdown("**💵 Savings**")
                profile = get_profile()
                monthly_target = profile.get("monthly_savings_target", 0)
                
                # Calculations
                cash_flow = total_income - total_expenses
                savings_difference = cash_flow - monthly_target
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Monthly Cash Flow", f"${cash_flow:,.2f}")
                with col2:
                    st.metric("Savings Target", f"${monthly_target:,.2f}")
                with col3:
                    st.metric("Savings Difference", f"${savings_difference:,.2f}",
                             delta_color="inverse" if savings_difference < 0 else "normal")
                
                if st.form_submit_button(f"Save {month_name} Data"):
                    updated_data = {
                        "income": {
                            "salary": salary,
                            "investment": investment,
                            "other_income": other_income,
                            "total": total_income
                        },
                        "expenses": {
                            "rent": rent,
                            "groceries": groceries,
                            "transportation": transportation,
                            "utilities": utilities,
                            "entertainment": entertainment,
                            "other_expenses": other_expenses,
                            "total": total_expenses
                        },
                        "savings": {
                            "target": monthly_target,
                            "actual": cash_flow,
                            "difference": savings_difference
                        },
                        "cash_flow": cash_flow,
                        "completed": True
                    }
                    
                    update_month_data(month_key, updated_data)
                    st.success(f"{month_name} data saved successfully!")