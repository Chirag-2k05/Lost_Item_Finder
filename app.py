import streamlit as st
import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Lost Item Finder", layout="centered")

# -----------------------------
# DATABASE (Simple CSV-based)
# -----------------------------
DATA_FILE = "data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["item", "location", "description"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -----------------------------
# UI
# -----------------------------
st.title("🔍 AI Lost Item Finder")
st.write("Find your lost items easily!")

menu = st.sidebar.selectbox("Menu", ["Add Item", "Find Item", "View All"])

df = load_data()

# -----------------------------
# ADD ITEM
# -----------------------------
if menu == "Add Item":
    st.subheader("➕ Add Lost Item")

    item = st.text_input("Item Name")
    location = st.text_input("Last Seen Location")
    description = st.text_area("Description")

    if st.button("Save Item"):
        if item and location:
            new_data = pd.DataFrame([[item, location, description]],
                                    columns=["item", "location", "description"])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("✅ Item saved successfully!")
        else:
            st.error("⚠️ Please fill required fields")

# -----------------------------
# FIND ITEM
# -----------------------------
elif menu == "Find Item":
    st.subheader("🔍 Find Your Item")

    query = st.text_input("Enter item name")

    if st.button("Search"):
        if query:
            results = df[df["item"].str.contains(query, case=False, na=False)]

            if not results.empty:
                st.success(f"Found {len(results)} result(s)")
                st.dataframe(results)
            else:
                st.warning("❌ No items found")
        else:
            st.error("⚠️ Enter something to search")

# -----------------------------
# VIEW ALL
# -----------------------------
elif menu == "View All":
    st.subheader("📋 All Items")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No data available")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("🚀 Built with Streamlit | AI Project")