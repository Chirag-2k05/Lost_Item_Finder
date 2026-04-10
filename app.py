import streamlit as st
import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Lost Item Finder", layout="centered")

USER_FILE = "users.csv"
DATA_FILE = "data.csv"

# -----------------------------
# USER DATABASE
# -----------------------------
def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_users(df):
    df.to_csv(USER_FILE, index=False)

# -----------------------------
# ITEM DATABASE
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["user", "item", "location", "description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# -----------------------------
# LOGIN / SIGNUP UI
# -----------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login / Signup")

    option = st.selectbox("Choose Option", ["Login", "Signup"])
    users_df = load_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            if username and password:
                if username in users_df["username"].values:
                    st.error("⚠️ Username already exists")
                else:
                    new_user = pd.DataFrame([[username, password]],
                                            columns=["username", "password"])
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    save_users(users_df)
                    st.success("✅ Account created! Please login.")
            else:
                st.error("⚠️ Fill all fields")

    elif option == "Login":
        if st.button("Login"):
            user = users_df[
                (users_df["username"] == username) &
                (users_df["password"] == password)
            ]

            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# -----------------------------
# MAIN APP (AFTER LOGIN)
# -----------------------------
else:
    st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    st.title("🔍 AI Lost Item Finder")

    menu = st.sidebar.selectbox("Menu", ["Add Item", "Find Item", "View My Items"])

    df = load_data()

    # -------------------------
    # ADD ITEM
    # -------------------------
    if menu == "Add Item":
        st.subheader("➕ Add Lost Item")

        item = st.text_input("Item Name")
        location = st.text_input("Last Seen Location")
        description = st.text_area("Description")

        if st.button("Save Item"):
            if item and location:
                new_data = pd.DataFrame([[st.session_state.user, item, location, description]],
                                        columns=["user", "item", "location", "description"])
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)
                st.success("✅ Item saved!")
            else:
                st.error("⚠️ Fill required fields")

    # -------------------------
    # FIND ITEM
    # -------------------------
    elif menu == "Find Item":
        st.subheader("🔍 Find Item")

        query = st.text_input("Search item")

        if st.button("Search"):
            results = df[df["item"].str.contains(query, case=False, na=False)]

            if not results.empty:
                st.dataframe(results)
            else:
                st.warning("❌ No items found")

    # -------------------------
    # VIEW USER ITEMS
    # -------------------------
    elif menu == "View My Items":
        st.subheader("📋 My Items")

        user_items = df[df["user"] == st.session_state.user]

        if not user_items.empty:
            st.dataframe(user_items)
        else:
            st.info("No items found")

    # -------------------------
    # FOOTER
    # -------------------------
    st.markdown("---")
    st.caption("🚀 AI Lost Item Finder with Login System")