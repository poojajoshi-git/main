import streamlit as st
import os
from auth import login_screen
import dashboard_customer
import dashboard_retailer
import dashboard_admin

# Ensure folders exist
for folder in ["data", "data/invoices", "data/reports"]:
    os.makedirs(folder, exist_ok=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Routing logic
if not st.session_state.logged_in:
    login_screen()
else:

    role = st.session_state.get("role")
    if role == "Customer":
        dashboard_customer.show()
    elif role == "Retailer":
        dashboard_retailer.show()
    elif role == "Admin":
        dashboard_admin.show()
    else:
        st.error("Unknown role. Please contact support.")