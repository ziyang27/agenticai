import json
import os
import streamlit as st
import calendar

def initialize_test_user():
    """Initialize a test user with empty data for all months"""
    current_year = "2024"
    months_data = {}
    
    for month_name in calendar.month_name[1:]:  # Skip empty first element
        month_key = f"{month_name.lower()}_{current_year}"
        months_data[month_key] = {
            "income": {
                "salary": 0.0,
                "investment": 0.0,
                "other_income": 0.0,
                "total": 0.0
            },
            "expenses": {
                "rent": 0.0,
                "groceries": 0.0,
                "transportation": 0.0,
                "utilities": 0.0,
                "entertainment": 0.0,
                "other_expenses": 0.0,
                "total": 0.0
            },
            "savings": {
                "target": 0.0,
                "actual": 0.0,
                "difference": 0.0
            },
            "cash_flow": 0.0,
            "completed": False
        }
    
    return {
        "profile": {
            "name": "Test User",
            "current_age": 25,
            "retirement_age": 65,
            "current_income": 5000,
            "current_savings": 10000,
            "risk_tolerance": "Moderate",
            "inflation_rate": 2.5,
            "monthly_savings_target": 1000
        },
        "months": months_data
    }

def get_user_data():
    """Get or initialize user data"""
    user_id = "test_user"  # Fixed single user for demo
    
    if 'user_data' not in st.session_state:
        # Try to load from file
        filename = f"data/{user_id}.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    st.session_state.user_data = json.load(f)
            except:
                st.session_state.user_data = initialize_test_user()
        else:
            st.session_state.user_data = initialize_test_user()
    
    return st.session_state.user_data

def save_user_data():
    """Save user data to file"""
    user_id = "test_user"
    os.makedirs('data', exist_ok=True)
    filename = f"data/{user_id}.json"
    
    if 'user_data' in st.session_state:
        try:
            with open(filename, 'w') as f:
                json.dump(st.session_state.user_data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving data: {e}")
            return False
    return False

def get_month_data(month_key):
    """Get data for specific month"""
    user_data = get_user_data()
    return user_data["months"].get(month_key, {})

def update_month_data(month_key, data):
    """Update data for specific month"""
    if 'user_data' not in st.session_state:
        get_user_data()
    
    st.session_state.user_data["months"][month_key] = data
    save_user_data()

def update_profile(profile_data):
    """Update user profile"""
    if 'user_data' not in st.session_state:
        get_user_data()
    
    st.session_state.user_data["profile"] = profile_data
    save_user_data()

def get_all_months_data():
    """Get data for all months"""
    user_data = get_user_data()
    return user_data["months"]

def get_profile():
    """Get user profile"""
    user_data = get_user_data()
    return user_data["profile"]