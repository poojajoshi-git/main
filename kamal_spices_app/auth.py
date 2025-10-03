import streamlit as st
import pandas as pd
import hashlib
import os

# 🔧 File setup
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")
os.makedirs(DATA_DIR, exist_ok=True)

# 🔐 Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 📥 Load users
def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_excel(USERS_FILE)
    else:
        return pd.DataFrame(columns=["Username", "Password", "Role"])

# 💾 Save new user
def save_user(username, password, role):
    users = load_users()
    new_entry = pd.DataFrame([[username, password, role]], columns=["Username", "Password", "Role"])
    users = pd.concat([users, new_entry], ignore_index=True)
    users.to_excel(USERS_FILE, index=False)

# 🔐 Login screen
def login_screen():
    st.title("🔐 Kamal Masale")

    tab1, tab2 = st.tabs(["📝 Signup", "🔑 Login"])

    with tab1:
        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        new_role = st.selectbox("Role", ["Customer", "Retailer"], key="signup_role")  # ✅ Admin removed

        if st.button("Create Account"):
            users = load_users()
            if new_user in users["Username"].values:
                st.error("Username already exists.")
            else:
                hashed_pass = hash_password(new_pass)
                save_user(new_user, hashed_pass, new_role)
                st.success("Account created successfully!")

                # Auto-login after signup
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.session_state.role = new_role
                st.rerun()

    with tab2:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            users = load_users()
            hashed_pass = hash_password(password)
            user_row = users[(users["Username"] == username) & (users["Password"] == hashed_pass)]

            if not user_row.empty:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user_row.iloc[0]["Role"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")