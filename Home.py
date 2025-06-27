import streamlit as st
import json
import os
import random
from PIL import Image, ImageDraw
import base64
from io import BytesIO

st.set_page_config(page_title="AI Career Counsellor", page_icon="🎓", layout="wide")

# 💎 Career tips
career_tips = [
    "Success doesn't come to you. You go to it. 🚀",
    "Choose a job you love, and you'll never work a day in your life. 💼",
    "The future depends on what you do today. 🔮",
    "Find out what you're passionate about and get paid to do it. 💡",
    "Don't be afraid to start small. Great things begin with simple steps. 🌱",
    "Keep learning. Keep growing. 📚",
    "You are the CEO of your own life. Build your brand wisely. 👑",
    "Passion + Skill = Your Career Superpower 💪",
    "The only limit to your impact is your imagination and commitment. 🌠",
    "Small steps every day lead to big achievements. 🏆",
    "Stay curious, stay hungry. 🚀",
    "Your career is a journey, not a destination. 🌍",
    "The best way to predict your future is to create it. 🔧",
    "Dream big. Start now. 💫",
    "Never stop exploring new possibilities. 🌈"
]

career_suggestions = {
    "Engineering": ["Software Developer", "Data Scientist", "Cybersecurity Analyst", "Cloud Engineer", "AI Researcher", "Product Manager", "Entrepreneur", "Robotics Engineer", "Systems Architect"],
    "Arts": ["Graphic Designer", "Creative Writer", "Museum Curator", "Art Director", "Photographer", "Animator", "UI/UX Designer", "Film Director"],
    "Commerce": ["Business Consultant", "Financial Analyst", "Marketing Manager", "HR Specialist", "Investment Banker", "Entrepreneur", "E-commerce Manager", "Supply Chain Analyst"],
    "Medical": ["Doctor", "Nurse", "Medical Researcher", "Pharmacist", "Therapist", "Radiologist", "Healthcare Administrator"],
    "Technology": ["Full Stack Developer", "Mobile App Developer", "AI Engineer", "Cybersecurity Expert", "UI/UX Designer", "Cloud Solutions Architect", "Data Engineer", "DevOps Specialist"],
    "Education": ["Teacher", "Lecturer", "Corporate Trainer", "Education Consultant", "Academic Researcher"],
    "Law": ["Lawyer", "Corporate Legal Advisor", "Judge", "Legal Analyst", "Legal Consultant"],
    "Sports": ["Athlete", "Fitness Trainer", "Sports Analyst", "Coach", "Sports Psychologist"],
    "Government Services": ["IAS Officer", "IPS Officer", "Public Sector Manager", "Foreign Service Officer", "Army Officer", "Navy Officer", "Air Force Pilot", "Defence Analyst"],
    "Other": ["Entrepreneur", "Social Worker", "Career Coach", "Freelancer", "Content Creator", "NGO Coordinator"]
}

# 🖼️ Load logo and make it circular
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def load_logo():
    try:
        img = Image.open("assets/logo.png")
        mask = Image.new("L", img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)
        return img
    except FileNotFoundError:
        st.warning("Logo image not found!")
        return None

# 🌙 Custom Dark Theme CSS
st.markdown("""
    <style>
        body {background-color: #1E1E1E; color: white;}

        /* Input boxes */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            background-color: #2E2E2E !important;
            color: white !important;
            border: 1px solid #444 !important;
        }

        /* Multiselect and Dropdown */
        .stMultiSelect div, .stSelectbox div {
            background-color: #2E2E2E !important;
            color: white !important;
            border: 1px solid #444 !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: #333333 !important;
            color: white !important;
            border: 1px solid #555 !important;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: background-color 0.3s, color 0.3s;
        }

        /* Button hover effect */
        .stButton > button:hover {
            background-color: #555555 !important;
            color: white !important;
        }

        /* Info box */
        .stAlert {
            background-color: #2E2E2E !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Set Profile Completion in Session
if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False

# Save user data
def save_user_data(user_data):
    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)

# Load user profile
def load_user_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            return json.load(file)
    return {}

# UI Layout with Logo
logo = load_logo()
if logo:
    st.markdown("""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{}' width='180'/>
            <h1 style='color: #4CAF50;'>🎓 AI Virtual Career Counsellor</h1>
            <h3>Find your perfect career path based on what you love doing 💭✨</h3>
        </div>
    """.format(image_to_base64(logo)), unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align: center;'>🎓 AI Virtual Career Counsellor</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Find your perfect career path based on what you love doing 💭✨</h3>", unsafe_allow_html=True)

# 💡 Show Random Career Tip
st.info(f"💡 Career Tip of the Day: *{random.choice(career_tips)}*")

# Form Section
with st.expander("📝 Fill Your Profile Form", expanded=True):
    st.markdown("#### ✨ _This helps tailor your career path_")
    name = st.text_input("📛 Name")
    age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1)
    education = st.selectbox("🎓 Education Level", ["High School", "Diploma", "Undergraduate", "Postgraduate", "PhD", "Vocational Training", "Certification Program", "Distance Education", "Online Degree", "Other"])
    interests = st.multiselect("💡 Select Your Interests", ["Technology", "Gaming", "Design", "Art", "Finance", "Teaching", "Business", "Health", "Content Creation", "Writing", "Digital Marketing", "Public Speaking", "Public Relations", "Sports", "Defence", "Entrepreneurship", "Social Service"])
    skills = st.multiselect("🛠️ Select Your Skills", ["Problem Solving", "Communication", "Coding", "Design", "Leadership", "Marketing", "Data Analysis", "Machine Learning", "AI Prompt Engineering", "UI/UX Design", "Web Development", "Mobile App Development", "Cloud Computing", "Cybersecurity", "Video Editing", "Data Visualization", "Graphic Design", "Critical Thinking", "Adaptability", "Team Collaboration", "Startup Management"])
    field = st.selectbox("🏛️ Preferred Field", ["Engineering", "Arts", "Commerce", "Medical", "Technology", "Education", "Law", "Sports", "Government Services", "Other"])
    goal = st.text_input("🎯 What's your dream career?")

    if st.button("💾 Save Profile"):
        if name and interests and skills:
            user_data = {
                "name": name,
                "age": age,
                "education": education,
                "interests": interests,
                "skills": skills,
                "preferred_field": field,
                "career_goal": goal
            }
            save_user_data(user_data)
            st.session_state.profile_completed = True
            st.success("✅ Profile saved successfully!")
        else:
            st.warning("⚠️ Please fill all required fields!")

# Dynamic Career Suggestions
user_data = load_user_data()
if st.session_state.get("profile_completed", False):
    suggestions = random.sample(career_suggestions.get(user_data["preferred_field"], career_suggestions["Other"]), 2)
    st.markdown(f"## 🎯 Based on your interest in **{user_data['preferred_field']}**, you can explore:")
    st.markdown(f"- {suggestions[0]}\n- {suggestions[1]}")
    st.markdown(f"Your skills in **{', '.join(user_data.get('skills', ['****']))}** can be a great asset for these careers.")

    st.markdown("---")
    st.markdown("## ✨ Ready to explore more with our AI Chatbot?")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    with col3:
        if st.button("🎟️ Continue to Chatbot"):
            st.switch_page("pages/1_Chatbot.py")

# Fancy Footer
st.markdown("""
    <br><br><hr><div style='text-align: center; padding: 1rem;'>
        Made with ❤️ by <strong>Adithya M</strong> | Internship Project 2025 🚀
    </div>
""", unsafe_allow_html=True)
