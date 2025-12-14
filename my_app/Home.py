import streamlit as st
import json
import os
import hashlib

# File where users are stored
USER_DATA_FILE = "user_data.json"

st.set_page_config(
    page_title="Login / Register",
    page_icon="🔑",
    layout="centered"
)

# Hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users from file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

# Session state initialisation
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")

# If user already logged in
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.username}")
    st.stop()

# Tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Log in"):
        users = st.session_state.users
        hashed_input = hash_password(login_password)

        if login_username in users and users[login_username] == hashed_input:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success("Login successful")
            st.switch_page("pages/1_Cyber_Security.py")
        else:
            st.error("Invalid username or password")

# ---------------- REGISTER ----------------
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        elif new_username in st.session_state.users:
            st.error("Username already exists")
        else:
            # Password is hashed before saving
            st.session_state.users[new_username] = hash_password(new_password)
            save_users(st.session_state.users)
            st.success("Account created you can now login")
