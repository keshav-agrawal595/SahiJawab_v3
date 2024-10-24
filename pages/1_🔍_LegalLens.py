import streamlit as st
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import google.generativeai as genai
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
import streamlit_option_menu as option_menu
from streamlit_lottie import st_lottie
import requests
from main import add_logout_button  # Import the logout function

load_dotenv()

LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Define translations
translations = {
    "English": {
        "welcome": "Welcome to Sahi Jawab: Your AI Legal Advisor",
        "chat_placeholder": "Ask your legal question here...",
        "thinking": "Thinking...",
        "new_chat": "Start a New Chat",
        "label_chat": "Label your chat:",
        "save_label": "Save Chat Label",
    },
    "Hindi": {
        "welcome": "सही जवाब में आपका स्वागत है: आपका AI कानूनी सलाहकार",
        "chat_placeholder": "अपना कानूनी प्रश्न यहाँ पूछें...",
        "thinking": "सोच रहा हूँ...",
        "new_chat": "नई चैट शुरू करें",
        "label_chat": "अपनी चैट को लेबल करें:",
        "save_label": "चैट लेबल सहेजें",
    },
    # Add more languages as needed
}

# Load Lottie animations
lottie_law = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qmfs6c3i.json")
lottie_robot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_xh83pj1c.json")
lottie_get_started=load_lottieurl("https://lottie.host/5ae92e40-52c0-447c-a24b-ca2ced970f38/q67fopDQir.json")

# Page config
st.set_page_config(
    page_title='Sahi Jawab',
    layout='wide',
    page_icon="⚖️"
)
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


# Sidebar
with st.sidebar.container():
    st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
with st.sidebar:
    # Language selector
    languages = list(translations.keys())
    st.session_state.language="English"
    selected_language = st.sidebar.selectbox("Select Language 🌐 ", languages, index=languages.index(st.session_state.get('language', 'English')))
    if selected_language != st.session_state.get('language', 'English'):
        st.session_state.language = selected_language
        st.rerun(scope="app")
    
    # About Us in an expander
    with st.sidebar.expander("ℹ️ About Us", expanded=False):
        st.markdown(translations[selected_language]["welcome"])
        st.success("AI-powered legal assistant for Indian laws.")

    # Features in an expander
    with st.sidebar.expander("🚀 Features", expanded=False):
        st.markdown("- AI-driven query engine\n- Interactive chatbot\n- Multi-language support")

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

# Main content
st.title("Welcome to Sahi Jawab: Your AI Legal Advisor")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["About", "Features", "Get Started"])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        # About Sahi Jawab

        **Sahi Jawab** is your comprehensive AI-powered legal platform designed to provide accurate and reliable answers to your legal queries. We harness the power of AI to extract all necessary information from the newly introduced criminal laws of India, making legal knowledge accessible to everyone. 🌟

        Our mission is to demystify legal jargon and provide clear, concise, and accurate information to help you navigate the complex world of Indian law.
        """)
    with col2:
        st_lottie(lottie_law, height=300, key="law")

with tab2:
    st.header("Key Features of Sahi Jawab")
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        - **📜 CrimeDecoder**: Engage with our smart chatbot for instant legal information.
        - **🗂️ DocWhisperer**: Upload and query your own legal documents.
        - **📸 SnapLaw**: Submit queries based on image content for legal insights.
        - **🎙️ VoxVerdict**: Use voice commands for hands-free legal assistance.
        - **🔒 Secure Login**: Ensures that only authorized users access the platform.
        - **🌐 Multi-language Support**: Get assistance in multiple Indian languages.
        """)
    with col2:
        st_lottie(lottie_robot, height=400, key="robot")

with tab3:
    st.header("Get Started with Sahi Jawab")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. **Select your preferred language** from the sidebar.
        2. **Choose a feature** you want to explore:
            - Use the chatbot for general legal queries
            - Upload documents for specific document-based questions
            - Try the image query feature for visual legal assistance
            - Experience rapid responses with our beta quick-answer feature
            - Use voice commands for a hands-free experience
        3. **Login or Sign Up** to access all features and save your query history.
        4. Start asking your legal questions and get accurate, AI-powered responses!
        """)
        
        if st.button("Launch 🔍LegalLens"):
            st.success("Redirecting to 🔍LegalLens...")
            # Add actual redirection logic here
    with col2:
        st_lottie(lottie_get_started, height=400, key="get-started")


# Important Notice Section
st.markdown("""
<div style="background-color:#ffcccb; padding:20px; border-radius:10px; border: 2px solid red; margin-top: 30px;">
    <h4 style="color:red; font-weight:bold;">⚠️ Important Notice</h4>
    <p style="color:black;">Please note that <strong>Sahi Jawab</strong> provides general legal information and advice based on the latest criminal laws of India. While we strive for accuracy, the information provided by this platform may not be exhaustive or up-to-date. <strong>Sahi Jawab</strong> does not replace professional legal counsel. We strongly recommend consulting with a qualified lawyer before taking any legal action or making any decisions based on the information provided by this platform.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
---
<p style="text-align: center;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
""", unsafe_allow_html=True)