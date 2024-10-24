import streamlit as st
import os
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from streamlit_lottie import st_lottie
import json
from main import add_logout_button  # Import the logout function

# Load environment variables
load_dotenv()

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()

# Configure API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Function to load Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

# Load Lottie animations
lottie_document = load_lottieurl("https://lottie.host/166bd88a-d9d0-498b-8f86-774195b99454/MBWDTWyffi.json")
lottie_chat = load_lottieurl("https://lottie.host/df41fd21-d0a2-4904-8e86-6d266299bca2/m6FgBZPrax.json")
lottie_law = load_lottieurl("https://lottie.host/102f2c6c-e9ce-41f1-87f3-2cc1a29b4d3b/P4WxZYm1UM.json")

# Page config
st.set_page_config(page_title='DocWhisperer', layout='wide', page_icon="🗂️")

# Custom CSS
st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    .css-1cpxqw2 {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
    st.markdown("---")
    if lottie_law:
        st_lottie(lottie_law, height=200, key="law")
    st.markdown("---")
    st.markdown("### About DocWhisperer")
    st.info("DocWhisperer allows you to upload your legal documents and chat with their content. Get insights and answers specific to your documents!")
    st.write("---")
    add_logout_button()
    st.write("---")

# Main content
st.title("🗂️ DocWhisperer: Chat with Your Legal Documents")
st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

# Display document animation before file upload
if lottie_document:
    st_lottie(lottie_document, height=300, key="document")

# File uploader
uploaded_file = st.file_uploader("Upload your legal document (PDF)", type="pdf")

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file is not None:
    with st.spinner("Processing your document..."):
        # Read PDF
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Create embeddings using Google's Generative AI
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Create conversation chain
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="Llama-3.2-90b-text-preview"
        )
        
        st.session_state.conversation = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=knowledge_base.as_retriever(),
            return_source_documents=True
        )

    st.success("Document processed successfully! You can now ask questions about its content.")

# Chat interface
if st.session_state.conversation is not None:
    if lottie_chat:
        st_lottie(lottie_chat, height=200, key="chat")

    user_question = st.text_input("Ask a question about your document:")
    if user_question:
        with st.spinner("Generating response..."):
            response = st.session_state.conversation({"question": user_question, "chat_history": st.session_state.chat_history})
            st.session_state.chat_history.append((user_question, response["answer"]))

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**You:**")
            with col2:
                st.markdown(f"{question}")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**DocWhisperer:**")
            with col2:
                st.markdown(f"{answer}")
            st.markdown("---")

# Display warning
st.warning("Please note that DocWhisperer provides information based on the uploaded document. Always consult with a qualified legal professional for accurate legal advice.")

# Footer
st.markdown("""
---
<p style="text-align: center; color: #666666;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
""", unsafe_allow_html=True)