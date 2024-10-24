import streamlit as st

def add_logout_button():
    if st.button("Logout", key="logout_button"):
        st.session_state['logged_in'] = False
        st.rerun()