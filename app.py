import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Lost Item Finder", layout="centered")

USER_FILE = "users.csv"
DATA_FILE = "data.csv"
RL_FILE = "feedback_rl.csv"

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# -----------------------------
# SAFE LOAD FUNCTIONS
# -----------------------------
def load_users():
    if os.path.exists(USER_FILE):
        try:
            df = pd.read_csv(USER_FILE)
            if df.empty:
                return pd.DataFrame(columns=["username", "password"])
            return df
        except:
            return pd.DataFrame(columns=["username", "password"])
    return pd.DataFrame(columns=["username", "password"])


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            if df.empty:
                return pd.DataFrame(columns=["user","item","location","description","type"])
            return df
        except:
            return pd.DataFrame(columns=["user","item","location","description","type"])
    return pd.DataFrame(columns=["user","item","location","description","type"])


def load_rl_data():
    if os.path.exists(RL_FILE):
        try:
            return pd.read_csv(RL_FILE)
        except:
            return pd.DataFrame(columns=["user","query","item","reward"])
    return pd.DataFrame(columns=["user","query","item","reward"])


def save_users(df):
    df.to_csv(USER_FILE, index=False)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def save_rl_data(df):
    df.to_csv(RL_FILE, index=False)

# -----------------------------
# RL SCORE
# -----------------------------
def get_rl_score(item, query, rl_df):
    data = rl_df[(rl_df["item"] == item) & (rl_df["query"] == query)]
    if data.empty:
        return 0
    return data["reward"].sum()

# -----------------------------
# MATCHING FUNCTION
# -----------------------------
def find_matches(df, item_row):
    others = df[df["type"] != item_row["type"]]

    if others.empty:
        return pd.DataFrame()

    item_text = item_row["description"] + " " + item_row["item"]
    other_texts = others["description"].fillna("") + " " + others["item"]

    emb1 = model.encode([item_text])
    emb2 = model.encode(other_texts.tolist())

    scores = cosine_similarity(emb1, emb2)[0]
    others = others.copy()
    others["match_score"] = scores

    return others.sort_values(by="match_score", ascending=False).head(3)

# -----------------------------
# RECOMMENDATION
# -----------------------------
def recommend_items(df, selected_index):
    texts = df["description"].fillna("") + " " + df["item"]

    embeddings = model.encode(texts.tolist())
    scores = cosine_similarity([embeddings[selected_index]], embeddings)[0]

    df = df.copy()
    df["rec_score"] = scores

    return df.sort_values(by="rec_score", ascending=False)[1:4]

# -----------------------------
# SESSION
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# -----------------------------
# LOGIN / SIGNUP
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
                    st.error("Username already exists")
                else:
                    new_user = pd.DataFrame([[username, password]],
                                            columns=["username","password"])
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    save_users(users_df)
                    st.success("Account created! Please login.")
            else:
                st.error("Fill all fields")

    elif option == "Login":
        if st.button("Login"):
            user = users_df[
                (users_df["username"] == username) &
                (users_df["password"] == password)
            ]

            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

# -----------------------------
# MAIN APP
# -----------------------------
else:
    st.sidebar.write(f"👤 {st.session_state.user}")

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
        st.subheader("➕ Add Item")

        item = st.text_input("Item Name")
        location = st.text_input("Location")
        description = st.text_area("Description")
        item_type = st.selectbox("Type", ["lost","found"])

        if st.button("Save Item"):
            if item and location:
                new_data = pd.DataFrame([[st.session_state.user, item, location, description, item_type]],
                                        columns=["user","item","location","description","type"])
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)
                st.success("Item saved!")

                matches = find_matches(df, new_data.iloc[0])
                if not matches.empty:
                    st.info("🤖 Possible Matches Found!")
                    st.dataframe(matches)

            else:
                st.error("Fill required fields")

    # -------------------------
    # SEARCH (NLP + RL)
    # -------------------------
    elif menu == "Find Item":
        st.subheader("🔍 AI Smart Search (RL Enabled)")

        query = st.text_input("Describe your item")

        if st.button("Search"):
            if query and not df.empty:

                texts = df["description"].fillna("") + " " + df["item"]

                item_embeddings = model.encode(texts.tolist())
                query_embedding = model.encode([query])

                base_scores = cosine_similarity(query_embedding, item_embeddings)[0]

                rl_df = load_rl_data()

                final_scores = []

                for i, row in df.iterrows():
                    rl_score = get_rl_score(row["item"], query, rl_df)
                    final_score = base_scores[i] + (0.2 * rl_score)
                    final_scores.append(final_score)

                df = df.copy()
                df["final_score"] = final_scores

                results = df.sort_values(by="final_score", ascending=False).head(5)

                st.success("Top Matches:")

                for idx, row in results.iterrows():
                    st.write(f"📌 {row['item']} (Score: {row['final_score']:.2f})")
                    st.write(f"📍 {row['location']}")
                    st.write(row["description"])

                    col1, col2 = st.columns(2)

                    rl_df = load_rl_data()

                    if col1.button(f"👍 Correct {idx}"):
                        new = pd.DataFrame([[st.session_state.user, query, row["item"], 1]],
                                           columns=["user","query","item","reward"])
                        rl_df = pd.concat([rl_df, new], ignore_index=True)
                        save_rl_data(rl_df)
                        st.success("Learning... Improved!")

                    if col2.button(f"👎 Wrong {idx}"):
                        new = pd.DataFrame([[st.session_state.user, query, row["item"], -1]],
                                           columns=["user","query","item","reward"])
                        rl_df = pd.concat([rl_df, new], ignore_index=True)
                        save_rl_data(rl_df)
                        st.warning("Got it! Will improve.")

                    st.markdown("---")

                # RECOMMENDATION
                st.subheader("🤖 Recommended Items")
                recs = recommend_items(df, results.index[0])
                st.dataframe(recs)

            else:
                st.warning("No data available")

    # -------------------------
    # VIEW ITEMS
    # -------------------------
    elif menu == "View My Items":
        st.subheader("📋 My Items")

        user_items = df[df["user"] == st.session_state.user]

        if not user_items.empty:
            st.dataframe(user_items)
        else:
            st.info("No items found")

    st.markdown("---")
    st.caption("🚀 AI + RL Powered Lost Item Finder")