import streamlit as st
import pandas as pd
import json
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer

action_kb = pd.read_csv("action_kb.csv").to_dict(orient="records")
info_kb = pd.read_csv("info_kb.csv").to_dict(orient="records")

def find_best_match(user_input, kb):
    user_input_lower = user_input.lower()
    for item in kb:
        if item["Question Trigger"].lower() in user_input_lower:
            return item
    return None

def fill_placeholders(template, customer_info):
    for key, value in customer_info.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template

def call_api(api_action, payload):
    payload_dict = json.loads(payload)
    return {
        "status": "success",
        "api_called": api_action,
        "payload": payload_dict
    }

def handle_user_query(user_input, customer_info):
    action_match = find_best_match(user_input, action_kb)
    if action_match:
        answer = fill_placeholders(action_match["Answer"], customer_info)
        payload = fill_placeholders(action_match["API_Payload"], customer_info)
        api_response = call_api(action_match["API_Action"], payload)
        return answer, api_response
    
    info_match = find_best_match(user_input, info_kb)
    if info_match:
        answer = fill_placeholders(info_match["Answer"], customer_info)
        return answer, None
    
    return "Sorry, I didn't understand your request. Can you rephrase?", None

st.set_page_config(page_title="Fintech Chatbot", layout="wide")
st.title("Fintech Chatbot")

st.sidebar.header("Customer Info")
customer_info = {
    "id": st.sidebar.text_input("Customer ID", "123456"),
    "last4": st.sidebar.text_input("Card Last 4 Digits", "4321"),
    "email": st.sidebar.text_input("Email", "demo@example.com"),
    "mobile": st.sidebar.text_input("Mobile", "9876543210"),
    "limit": st.sidebar.text_input("Requested Limit", "50000"),
    "date": st.sidebar.text_input("Date", "2025-12-10")
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("Voice Input")
webrtc_streamer(key="speech")

if st.button("Use Microphone and Send Voice"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio_data = r.listen(source, timeout=5)
        try:
            user_input = r.recognize_google(audio_data)
            st.success(f"Recognized: {user_input}")
            answer, api_resp = handle_user_query(user_input, customer_info)
            st.session_state.chat_history.append({"user": user_input, "bot": answer, "api": api_resp})
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError:
            st.error("Speech Recognition service error")

user_input_text = st.text_input("Or type your message here:")

if user_input_text:
    answer, api_resp = handle_user_query(user_input_text, customer_info)
    st.session_state.chat_history.append({"user": user_input_text, "bot": answer, "api": api_resp})

for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
    if chat['api']:
        st.markdown(f"*API Called:* `{chat['api']['api_called']}` with payload `{chat['api']['payload']}`")
    st.markdown("---")
