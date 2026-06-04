import streamlit as st
from pandas import options
from supabase import create_client, Client
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Summer Chat", page_icon="💬", layout="centered")
st.title("Summer Chat")

st_autorefresh(interval=2000, key="chat_live_refresh")

SUPABASE_URL = "https://sfarxlayfddzmztwbhyr.supabase.co"
SUPABASE_KEY = "sb_publishable_yBq_Ee82lIgo-j5QeAIRQA_7qFKYk3F"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    user_input = st.text_input("Enter your username")
    if st.button("Join Summer Chat"):
        if user_input.strip():
            st.session_state.username = user_input.strip()
            st.rerun()
        else:
            st.error("Name cannot be empty")
    st.stop()

def fetch_messages():
    response = supabase.table("chat_messages").select("*").order("created_at", desc=False).execute()
    return response.data

messages = fetch_messages()

chat_contaner = st.container(height=400)
with chat_contaner:
    for msg in messages:
        if msg["sender"] == st.session_state.username:
            with st.chat_message("user"):
                st.write(f"**you**: {msg['message']}")
        else:
            with st.chat_message("assistant"):
                st.write(f"**{msg['sender']}**: {msg['message']}")


if prompt :=st.chat_input("Enter your message here..."):
    supabase.table("chat_messages").insert({"sender": st.session_state.username, "message": prompt}).execute()
    st.rerun()