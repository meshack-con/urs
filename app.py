import streamlit as st
from supabase import create_client
import pandas as pd

# ---------------------------------------------
# SUPABASE CONFIG
# ---------------------------------------------
SUPABASE_URL = "https://pnpjfaalcvetdjbcuadj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBucGpmYWFsY3ZldGRqYmN1YWRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMyMjM5NTYsImV4cCI6MjA3ODc5OTk1Nn0.5AmOhm_ATsZTX1Vkg5_XHKEytVVpBsGCfATM4dqWlOo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------
st.set_page_config(page_title="UVCCM Registration", layout="wide")

# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------
def login(username, password):
    return (
        supabase.table("admins")
        .select("*")
        .eq("username", username)
        .eq("password", password)
        .maybe_single()
        .execute()
        .data
    )

def save_student(data):
    return supabase.table("students").insert(data).execute()

def get_students():
    return (
        supabase.table("students")
        .select("*")
        .order("created_at", desc=True)
        .execute()
        .data
    )

# ---------------------------------------------
# SESSION
# ---------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------
# LOGIN PAGE
# ---------------------------------------------
if not st.session_state.logged_in:

    st.markdown("<h1 style='text-align:center;color:#ffea00;'>UVCCM Registration System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:white;font-size:20px;'>Login to continue</p>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.logged_in = True
            st.success("Login success!")
            st.rerun()
        else:
            st.error("Wrong username or password")

    st.stop()

# ---------------------------------------------
# DASHBOARD UI
# ---------------------------------------------
st.markdown("<h2 style='color:#ffea00;'>Dashboard</h2>", unsafe_allow_html=True)
st.success("You are logged in!")

colA, colB = st.columns([1.1, 2])

# LEFT SIDE
with colA:
    st.markdown("<h3 style='color:#ffea00;'>Register Student</h3>", unsafe_allow_html=True)

    full_name = st.text_input("Full name")
    course = st.selectbox("Course", ["", "CNISE", "CSDFE", "CS", "IS", "HIS", "DCBE", "CE", "TE", "SE"])
    years = st.number_input("Years", 1, 6, 3)
    block = st.text_input("Block")
    gender = st.selectbox("Gender", ["", "Male", "Female"])
    room = st.text_input("Room number")
    phone = st.text_input("Phone number")

    if st.button("Save Student"):
        if not full_name or not course or not gender:
            st.error("Please fill required fields")
        else:
            data = {
                "full_name": full_name,
                "course": course,
                "years_of_study": years,
                "block": block,
                "gender": gender,
                "room": room,
                "phone_number": phone,
            }
            save_student(data)
            st.success("Student saved successfully!")
            st.rerun()

# RIGHT SIDE
with colB:
    st.markdown("<h3 style='color:#ffea00;'>Overview</h3>", unsafe_allow_html=True)

    students = get_students()
    df = pd.DataFrame(students) if students else pd.DataFrame()

    total = len(df)
    male = len(df[df["gender"] == "Male"]) if not df.empty else 0
    female = len(df[df["gender"] == "Female"]) if not df.empty else 0

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Students", total)
    c2.metric("Male", male)
    c3.metric("Female", female)

    st.subheader("All Registered Students")

    if df.empty:
        st.info("No students registered yet.")
    else:
        st.dataframe(df, use_container_width=True)

# LOGOUT
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------------------------------------
# FINAL COLOR THEME
# ---------------------------------------------
st.markdown("""
    <style>

        /* Background */
        .stApp {
            background-color: black !important;
        }

        /* Titles */
        h1, h2, h3, h4 {
            color: #ffea00 !important;
        }

        /* Labels White */
        label {
            color: white !important;
            font-weight: 600;
        }

        /* Inputs now BLACK inside + white text */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {
            background-color: black !important;
            color: white !important;
            border: 2px solid #ffea00 !important;
            border-radius: 6px;
        }

        /* Buttons Yellow */
        div.stButton > button {
            background-color: #ffea00 !important;
            color: black !important;
            font-weight: bold;
            border-radius: 10px;
        }

        /* METRICS — Black bg + yellow text */
        [data-testid="stMetric"] {
            background-color: black !important;
            border: 2px solid #ffea00 !important;
            color: #ffea00 !important;
            padding: 15px;
            border-radius: 10px;
        }

        /* TABLE — White */
        .stDataFrame, .dataframe {
            background-color: white !important;
            color: black !important;
        }

    </style>
""", unsafe_allow_html=True)
