import streamlit as st
import os

from db import add_item
from model import predict_location
from auth import login, register
from voice import listen, speak_async
from nlp import detect_intent, extract_item, extract_location

st.title("🤖 AI Lost Item Finder")

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# AUTH
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if st.session_state.user is None:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("Logged in")
            else:
                st.error("Invalid credentials")

    else:
        if st.button("Register"):
            register(username, password)
            st.success("Registered successfully")

    st.stop()

# MAIN APP
st.sidebar.write(f"Welcome {st.session_state.user}")

option = st.selectbox("Choose", ["Find Item", "Update Item", "Voice Mode"])

# FIND
if option == "Find Item":
    item = st.text_input("Item name")

    if st.button("Find"):
        location, score = predict_location(st.session_state.user, item)

        if location:
            st.success(f"📍 {location}")
            st.info(f"Confidence: {score}")
        else:
            st.warning("No data found")

# UPDATE
elif option == "Update Item":
    item = st.text_input("Item")
    location = st.text_input("Location")

    image = st.file_uploader("Upload Image", type=["png", "jpg"])
    image_path = None

    if image:
        os.makedirs("uploads", exist_ok=True)
        image_path = f"uploads/{image.name}"
        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

    if st.button("Save"):
        add_item(st.session_state.user, item, location, image_path)
        st.success("Saved successfully")

# VOICE MODE
elif option == "Voice Mode":
    if st.button("🎤 Speak"):
        text = listen()

        if text:
            st.write(f"You said: {text}")

            intent = detect_intent(text)
            item = extract_item(text)
            location = extract_location(text)

            if intent == "FIND":
                loc, score = predict_location(st.session_state.user, item)

                if loc:
                    response = f"Your {item} is at {loc}"
                    st.success(response)
                    speak_async(response)
                else:
                    speak_async("No data found")

            elif intent == "UPDATE" and location:
                add_item(st.session_state.user, item, location)
                speak_async("Saved successfully")