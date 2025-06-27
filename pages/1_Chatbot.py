import streamlit as st
import json
import os
import google.generativeai as genai
from streamlit_chat import message

# 🚩 Profile Check
if 'profile_completed' not in st.session_state or not st.session_state.profile_completed:
    st.warning("⚠️ Please complete your profile first!")
    if st.button("Go to Profile Page"):
        st.switch_page("Home.py")  # ✅ Fixed navigation
    st.stop()

# 🔐 Configure Gemini API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load user profile
def load_user_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            return json.load(file)
    return {}

# Load chat history
def load_chat_history():
    if os.path.exists("chat_history.json"):
        try:
            with open("chat_history.json", "r") as file:
                history = json.load(file)
                if isinstance(history, list):
                    return history
        except:
            return []
    return []

# Save chat
def save_chat(user_message, bot_reply, reactions=None):
    if not user_message or not bot_reply:
        return

    chat = {"user": str(user_message), "bot": str(bot_reply), "reactions": reactions or {"👍": 0, "👎": 0, "❤️": 0}}

    history = load_chat_history()
    history.append(chat)

    with open("chat_history.json", "w") as file:
        json.dump(history, file, indent=4)

# Generate Gemini response
def generate_response(user_input, user_data):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])
        response = chat.send_message(user_input)
        return response.text.strip()
    except:
        return "⚙️ Sorry, I faced an issue generating the response. Please try again!"

# 🔥 Unified Questions List
all_questions = [
    "How do I choose my career path?",
    "What are the top skills for IT jobs?",
    "How can I prepare for interviews?",
    "What courses should I take for Data Science?",
    "Is work-life balance possible in tech?",
    "What are trending careers in 2025?",
    "How to improve my resume?",
    "How can I find internships?",
    "What are some high-paying jobs?",
    "How to switch careers smoothly?",
    "What skills are needed for project management?",
    "Is freelancing a good career option?",
    "How can I build a strong LinkedIn profile?",
    "How to find remote job opportunities?",
    "What is the best way to start in cybersecurity?",
]

# UI starts here
def main():
    st.set_page_config(page_title="AI Career Counsellor - Chatbot", page_icon="💬", layout="wide")

    # Custom CSS for theme matching
    st.markdown("""
    <style>
        body {color: white; background-color: #1E1E1E;}
        .stTextInput input {
            background-color: #2E2E2E !important;
            color: white !important;
            text-align: left;
            width: 350px !important;
            margin: 0 auto;
        }
        .stButton>button {
            background-color: #2E2E2E !important;
            color: white !important;
            border: none !important;
            text-align: left !important;
            padding: 10px !important;
            border-radius: 5px !important;
        }
        .stButton>button:hover {
            background-color: #4CAF50 !important;
            color: white !important;
        }
        .stSidebar .css-6qob1r {  
            background-color: #1E1E1E !important;
        }
        .chat-input-container {display: flex; justify-content: center;}
        .chat-title {text-align: center; font-size: 36px; color: white;}
        .chat-subtitle {text-align: center; font-size: 18px; color: grey;}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Section (Unified Questions)
    st.sidebar.markdown("## 💡 Suggested Questions")
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = ""

    for question in all_questions:
        if st.sidebar.button(question, use_container_width=True):
            st.session_state.selected_question = question

    # Main Chat Section
    st.markdown('<h1 class="chat-title">🤖 Live Chat with CareerBot</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="chat-subtitle">💬 What are you working on?</h3>', unsafe_allow_html=True)

    user_data = load_user_data()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history()
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", value=st.session_state.selected_question, placeholder="💬 Ask anything...", key=f"user_input_{st.session_state.input_key}")
        submitted = st.form_submit_button("🚀 Send")

    if submitted and user_input:
        with st.spinner("💬 CareerBot is typing..."):
            bot_reply = generate_response(user_input, user_data)
            
        st.session_state.chat_history.append({"user": user_input, "bot": bot_reply, "reactions": {"👍": 0, "👎": 0, "❤️": 0}})
        save_chat(user_input, bot_reply)
        st.session_state.input_key += 1
        st.session_state.selected_question = ""  # Clear selected question after sending
        st.rerun()

    st.markdown("## 🔥 Recent Conversations")

    # Show recent 3 messages (most recent on top)
    for i, chat in enumerate(reversed(st.session_state.chat_history[-3:])):
        message(f"🧑 You: {chat['user']}", is_user=True, key=f"user_{i}")
        message(f"🤖 CareerBot: {chat['bot']}", key=f"bot_{i}")

        cols = st.columns(5)
        with cols[0]:
            if st.button("👍", key=f"like_{i}"):
                chat["reactions"]["👍"] += 1
                st.rerun()
        with cols[1]:
            if st.button("👎", key=f"dislike_{i}"):
                chat["reactions"]["👎"] += 1
                st.rerun()
        with cols[2]:
            if st.button("❤️", key=f"love_{i}"):
                chat["reactions"]["❤️"] += 1
                st.rerun()
        with cols[3]:
            st.write(f"👍 {chat['reactions']['👍']}  👎 {chat['reactions']['👎']}  ❤️ {chat['reactions']['❤️']}")

        st.markdown("<hr>", unsafe_allow_html=True)

    # View Past Conversations
    with st.expander("📜 View Past Conversations"):
        full_history = load_chat_history()
        if full_history:
            for chat in full_history[:-3]:
                st.markdown(f"🧑 **You:** {chat['user']}")
                st.markdown(f"🤖 **CareerBot:** {chat['bot']}")
                st.markdown(f"👍 {chat['reactions']['👍']}  👎 {chat['reactions']['👎']}  ❤️ {chat['reactions']['❤️']}")
                st.markdown("---")
        else:
            st.info("ℹ️ No past conversations found.")

    # Download options
    with st.expander("⬇️ Download Chat History"):
        if st.session_state.chat_history:
            json_data = json.dumps(st.session_state.chat_history, indent=4)
            chat_txt = ""
            for chat in st.session_state.chat_history:
                chat_txt += f"🧑 You: {chat['user']}\n🤖 CareerBot: {chat['bot']}\nReactions: {chat['reactions']}\n" + "-" * 40 + "\n"

            st.download_button("📁 Download JSON", data=json_data, file_name="chat_history.json", mime="application/json")
            st.download_button("📝 Download TXT", data=chat_txt, file_name="chat_history.txt", mime="text/plain")
        else:
            st.info("ℹ️ No chat history to download.")

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        if os.path.exists("chat_history.json"):
            os.remove("chat_history.json")
        st.success("🧹 Chat cleared!")
        st.rerun()

if __name__ == "__main__":
    main()
