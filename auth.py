import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

# Initialize Firebase Admin SDK
cred = credentials.Certificate('chatwithlawyer-b38e6-firebase-adminsdk-cbiq0-a32eeb5fab.json')  # Update with your path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatwithlawyer-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Initialize Pyrebase
firebase_config = {
    "apiKey": "AIzaSyDJeOXPebd7uVOAUEI4Hn329DzvlRNULos",
    "authDomain": "chatwithlawyer.firebaseapp.com",
    "databaseURL": "https://chatwithlawyer-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "chatwithlawyer",
    "storageBucket": "chatwithlawyer.appspot.com",
    "messagingSenderId": "250950721924",
    "appId": "1:250950721924:web:e0a1a2524fe8429acffdd1"
}
firebase = pyrebase.initialize_app(firebase_config)
pb_auth = firebase.auth()

# Function for Email/Password login
def login():
    username = st.text_input("Username (Email)", "")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = pb_auth.sign_in_with_email_and_password(username, password)
            st.session_state['user'] = user
            st.success(f'Welcome back, {username}!')
            return True
        except Exception as e:
            st.error(str(e))

    return False

# Function for User Registration
def register():
    username = st.text_input("Username (Email)", "", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Register"):
        try:
            user = pb_auth.create_user_with_email_and_password(username, password)
            st.session_state['user'] = user
            st.success(f'Account created for {username}!')
            return True
        except Exception as e:
            st.error(str(e))

    return False

# Function to Logout
def logout():
    if st.button("Logout"):
        st.session_state.pop('user', None)
        st.success("Logged out successfully!")

# Function to test database access
def test_database_access():
    if st.button("Test Database Access"):
        try:
            # Attempt to read from the database
            ref = db.reference('messages')
            messages = ref.get()
            st.success("Successfully accessed the database!")
            st.write(messages)
        except Exception as e:
            st.error(f"Error accessing database: {str(e)}")
            st.error("Please check your Firebase Security Rules.")

# Main app logic
def main():
    if 'user' not in st.session_state:
        st.title("Login / Register")
        choice = st.radio("Choose an option", ["Login", "Register"])

        if choice == "Login":
            login()
        else:
            register()
    else:
        user = st.session_state['user']
        if isinstance(user, dict) and 'email' in user:
            st.write(f"Welcome, {user['email']}")
        elif hasattr(user, 'email'):
            st.write(f"Welcome, {user.email}")
        else:
            st.write("Welcome, User")
        
        test_database_access()
        logout()

if __name__ == "__main__":
    main()