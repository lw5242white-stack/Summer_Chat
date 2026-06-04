# ==========================================
# LINE 1: THE INITIALIZATION IMPORTS
# ==========================================
import streamlit as st
from panda import options
from supabase import create_client, Client
from streamlit_autorefresh import st_autorefresh

# ==========================================
# LINE 7: SCREEN & PAGE LAYOUT SETUP
# ==========================================
st.set_page_config(page_title="Summer Chat", page_icon="💬", layout="centered")
st.title("💬 Our Private Chat")

# ==========================================
# LINE 12: THE SECURE PASSWORD GATEWAY
# ==========================================
PRIVATE_CHAT_PASSWORD = st.secrets["secret_password"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔒 Private Access Required")
    entered_password = st.text_input("Enter the secret chat password:", type="password")
    
    if st.button("Unlock Chat"):
        if entered_password == PRIVATE_CHAT_PASSWORD:
            st.session_state.authenticated = True
            st.success("Access Granted!")
            st.rerun()
        else:
            st.error("Incorrect password! Access denied.")
    st.stop()  # Script pauses here until password matches

# ==========================================
# LINE 35: BACKGROUND TOOLS & LIVE SYNCING
# ==========================================
st_autorefresh(interval=2000, key="chat_live_refresh")

SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_yBq_Ee82lIgo-j5QeAIRQA_7qFKY3F"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# ==========================================
# LINE 48: SCREEN 2 - USER IDENTITY SIGN IN
# ==========================================
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    user_input = st.text_input("Enter your username to join the chat:", key="name_input")
    if st.button("Join Summer Chat"):
        if user_input.strip():
            st.session_state.username = user_input.strip()
            st.rerun()
        else:
            st.error("Name cannot be empty!")
    st.stop()

# ==========================================
# LINE 65: SCREEN 3 - THE ACTIVE CHAT ROOM
# ==========================================
def fetch_messages():
    response = supabase.table("chat_messages").select("*").order("created_at", desc=False).execute()
    return response.data

messages = fetch_messages()

chat_container = st.container(height=400)
with chat_container:
    for msg in messages:
        if msg["sender"] == st.session_state.username:
            with st.chat_message("user"):
                st.write(f"**You**: {msg['message']}")
        else:
            with st.chat_message("assistant"):
                st.write(f"**{msg['sender']}**: {msg['message']}")

if prompt := st.chat_input("Type your message here..."):
    supabase.table("chat_messages").insert({"sender": st.session_state.username, "message": prompt}).execute()
    st.rerun()
