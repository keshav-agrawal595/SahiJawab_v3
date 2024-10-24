import streamlit as st
import pyrebase
from utils import add_logout_button  # Import the logout function from utils.py

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyDuI1hHPO53snuT-S9boJ1PiHrHYhqaRj4",
    "authDomain": "ai-legal-advisor-ad193.firebaseapp.com",
    "projectId": "ai-legal-advisor-ad193",
    "storageBucket": "ai-legal-advisor-ad193.appspot.com",
    "messagingSenderId": "1013334880666",
    "appId": "1:1013334880666:web:db34606e71638457e90a23",
    "measurementId": "G-3FY4KKGXG0",
    "databaseURL": "https://ai-legal-advisor-ad193-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

st.set_page_config(page_title='Sahi Jawab', layout='wide', page_icon="⚖️")
st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

def print_praise():
        praise_quotes = """
        Team Sahi Jawab
    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

with st.sidebar.container():
    st.warning("Seperate Login is Required for ChatWithAdvocate App.\nFirst log out of main app then visit ChatWithAdvocate and login and signup there.")
    st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')

# About Us in an expander
with st.sidebar.expander("ℹ️ About Us", expanded=False):
    st.write("Sahi Jawab : AI Legal Advisor")
    st.success("AI-powered legal assistant for Indian laws.")

# Features in an expander
with st.sidebar.expander("🚀 Features", expanded=False):
    st.markdown("- AI-driven query engine\n- Interactive chatbot\n- Multi-language support")

with st.sidebar:
    st.write("---")
    st.success(print_praise())
    st.write("---")
    add_logout_button()
    st.write("---")
    
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
        unsafe_allow_html=True
    )

    st.markdown('''
        <center>
        <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
        </center>
    ''', unsafe_allow_html=True)

def login_signup():
    st.image('logo/Sahi Jawab.png', width=200)
    st.title("Welcome to Sahi Jawab")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to Existing Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in successfully!")
                st.session_state['user'] = user
                st.session_state['logged_in'] = True
                # Manually rerun the script by setting a session state
                st.session_state["rerun"] = not st.session_state.get("rerun", False)
            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.subheader("Create New Account")
        new_email = st.text_input("Email Address", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            try:
                user = auth.create_user_with_email_and_password(new_email, new_password)
                st.success("Account created successfully! Please login.")
            except Exception as e:
                st.error(f"Error: {e}")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.success("You are logged in. Redirecting to the main application...")

if __name__ == "__main__":
    login_signup()
