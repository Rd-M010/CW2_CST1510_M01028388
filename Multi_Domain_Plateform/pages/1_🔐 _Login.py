import streamlit as st

from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager


st.set_page_config(page_title="Authentication", layout="wide")

st.title("🔐 Authentication")

db = DatabaseManager("database/platform.db")
auth = AuthManager(db)


# ---------- SUCCESS MESSAGE AFTER RERUN ----------
if "login_success" in st.session_state and st.session_state.login_success:
    st.success(f"Welcome {st.session_state.current_user}!")
    st.session_state.login_success = False


# ---------- TABS ----------
tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])


# ---------- LOGIN ----------
with tab_login:
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = auth.login_user(username, password)

        if user is None:
            st.error("Invalid username or password")
        else:
            st.session_state.logged_in = True
            st.session_state.current_user = user.get_username()
            st.session_state.current_role = user.get_role()
            st.session_state.login_success = True
            st.rerun()


# REGISTER 
with tab_register:
    st.subheader("Create an account")

    new_username = st.text_input("New username", key="reg_username")
    new_password = st.text_input("New password", type="password", key="reg_password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Register"):
        if not new_username or not new_password:
            st.error("Username and password are required")
        else:
            try:
                auth.register_user(new_username, new_password, role)
                st.success("Account created successfully. You can now log in.")
            except Exception as e:
                st.error("Username already exists or database error")
