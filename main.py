import streamlit as st
import importlib
import os
from Login import login_signup
from utils import add_logout_button  # Import the logout function from utils.py

def load_module(module_name):
    return importlib.import_module(f"pages.{module_name}")

def main():
    st.set_page_config(page_title="Sahi Jawab", layout="wide")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_signup()
        return

    st.sidebar.title("Sahi Jawab")
    st.sidebar.image('logo/Sahi Jawab.png', width=200)
    
    # Dynamically load pages
    pages = [f[:-3] for f in os.listdir('pages') if f.endswith('.py')]
    choice = st.sidebar.selectbox("Choose a feature", pages)

    # Load and display the selected page
    try:
        page_module = load_module(choice)
        page_function = getattr(page_module, f"show_{choice.lower()}")
        page_function()
    except Exception as e:
        st.error(f"Error loading page: {e}")

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    # Footer
    st.markdown("""
    ---
    <p style="text-align: center;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()