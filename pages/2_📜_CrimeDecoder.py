# import os
# import time
# import requests
# import streamlit as st
# from dotenv import load_dotenv
# from streamlit_lottie import st_lottie
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import google.generativeai as genai
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from tqdm import tqdm
# import time
# import re
# from main import add_logout_button  # Import the logout function

# # Load environment variables
# load_dotenv()

# def show_page_name():
#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("Please log in to access this page.")
#         st.stop()

# # if __name__ == "__main__":
# #     show_page_name()


# # Set up LangChain tracing
# LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"

# # Global variables
# model = None
# groq_api_key = os.getenv('GROQ_API_KEY')
# google_api_key = None

# # Function to load Lottie animations
# def load_lottieurl(url):
#     r = requests.get(url)
#     return r.json() if r.status_code == 200 else None

# # Function to load the Groq model
# def load_model():
#     global model
#     genai.configure(api_key=google_api_key)
#     model = ChatGroq(groq_api_key=groq_api_key, model_name="Llama-3.1-70b-versatile")

# # Chat prompt template for the AI assistant
# prompt_template = ChatPromptTemplate.from_template(
#     """
#     This is your introduction - Your name is "Sahi Jawab (Your Nyaya Mitra)" and you are developed by "Keshav Agrawal".

#     You're a go-to platform for all legal queries. You are embedded with the entire data of the three newly enacted criminal laws, namely:
#     - The Bharatiya Nyaya Sanhita (BNS)
#     - The Bharatiya Nagrik Suraksha Sanhita (BNSS)
#     - The Bharatiya Sakshya Adhiniyam (BSA)

#     Your aim is to make legal knowledge accessible to everyone. Users will ask their questions, and you will guide them with clear and concise answers based on the relevant law.

#     Whether they are seeking legal advice or just curious about the law, you are here to help. Use suitable emojis wherever needed.

#     Greet users with "Radhe Radhe 🙏" and ask them for their queries.

#     You will never use any Arabic words in your conversation.

#     If users ask anything about yourself, respond with polite words and avoid very straightforward one-liner answers.

#     Provide detailed answers based on the context. Clearly state which law (BNS, BNSS, or BSA) the answer pertains to. If the answer is not available in the context, say, "Answer is not available in the context." Do not provide incorrect answers.

#     IMPORTANT: You must respond ONLY in the {language} language. Do not use any other language in your response.

#     If the language is Hindi, use Devanagari script exclusively. Avoid using English words or Roman script in your Hindi responses.

#     Context:\n{context}\n
#     Question: \n{input}\n

#     Answer (in {language}):
#     """
# )

# # Function to get or create vector store
# def get_vector_store():
#     global google_api_key

#     if "vectors" not in st.session_state:
#         # Initialize embeddings
#         st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
#         # Check if pre-computed embeddings exist
#         if os.path.exists("faiss_index"):
#             st.session_state.vectors = FAISS.load_local("faiss_index", st.session_state.embeddings,allow_dangerous_deserialization=True)
#             return

#         # Create a progress bar and status text
#         progress_bar = st.progress(0)
#         status_text = st.empty()
#         percentage_text = st.empty()

#         # Load documents
#         status_text.text("Loading documents...")
#         st.session_state.loader = PyPDFDirectoryLoader("./bns")
#         st.session_state.docs = st.session_state.loader.load()
#         progress_bar.progress(20)

#         # Split documents into chunks
#         status_text.text("Splitting documents...")
#         st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
#         progress_bar.progress(30)

#         # Create vector store
#         status_text.text("Creating vector store...")
#         total_docs = len(st.session_state.final_documents)
        
#         for i, doc in enumerate(st.session_state.final_documents):
#             st.session_state.vectors = FAISS.from_documents([doc], st.session_state.embeddings)
#             progress = int(40 + (i / total_docs) * 60)
#             progress_bar.progress(progress)
#             percentage = round((i / total_docs) * 100, 2)
#             percentage_text.text(f"Embedding Progress: {percentage}%")
#             status_text.text(f"Embedding documents... {i+1}/{total_docs}")
#             time.sleep(0.1)  # To make the progress visible

#         # Save the vector store
#         status_text.text("Saving vector store...")
#         st.session_state.vectors.save_local("faiss_index")
#         progress_bar.progress(100)
#         percentage_text.text("Embedding Progress: 100%")
#         status_text.text("Embedding process complete!")
#         time.sleep(1)
#         status_text.empty()
#         percentage_text.empty()
#         progress_bar.empty()

# # Main function
# def main():
#     global model, groq_api_key, google_api_key

#     # Set up Streamlit page
#     st.set_page_config(page_title='Sahi Jawab', layout='wide', page_icon="⚖️")
#     st.sidebar.title("Sahi Jawab : Your Nyaya Mitra")
#     st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

#     # Sidebar setup
#     setup_sidebar()

#     # Handle user input and generate responses
#     handle_user_input()

#     # start documents embeddings
#     get_vector_store()

# # Function to set up the sidebar
# def setup_sidebar():
#     with st.sidebar:
#         st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
        
#         # Language selector
#         languages = ["English", "Hindi"]  # Add more languages as needed
#         st.session_state.language = st.sidebar.selectbox("Select Language 🌐 ", languages, index=languages.index(st.session_state.get('language', 'English')))

#         # About Us section
#         with st.sidebar.expander("ℹ️ About Us", expanded=False):
#             st.markdown("Welcome to Sahi Jawab, your AI-powered legal assistant for Indian laws.")
#             st.success("AI-powered legal assistant for Indian laws.")

#         # Features section
#         with st.sidebar.expander("🚀 Features", expanded=False):
#             st.markdown("- AI-driven query engine\n- Interactive chatbot\n- Multi-language support")

#         st.write("---")

#         # Lottie animation
#         lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
#         st_lottie(load_lottieurl(lottie_url), height=200, key="sidebar_animation")

#         st.markdown("---")

#         # API key input fields
#         setup_api_keys()

#         st.markdown("---")

#         # Start button for document embedding
#         start_document_embedding()

#         st.success(print_praise())   
#         st.write("---")

#         # New chat button
#         st.title("Looking to Restart your Conversation 🔄")
#         st.button('Start a New Chat', on_click=clear_chat_history)
        
#         st.write("---")
#         add_logout_button()
#         st.write("---")
        
#         # Developer information
#         st.markdown(
#             "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
#             unsafe_allow_html=True
#         )

#         # Visitor counter
#         st.markdown('''
#             <center>
#             <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
#             </center>
#         ''', unsafe_allow_html=True)

# # Function to set up API keys
# def setup_api_keys():
#     global groq_api_key, google_api_key

#     if 'GROQ_API_KEY' in st.secrets:
#         st.success('GROQ API key already provided!', icon='✅')
#         groq_api_key = st.secrets['GROQ_API_KEY']
#     else:
#         groq_api_key = st.text_input('Enter GROQ API Key:', type='password')
#         if not (groq_api_key.startswith('gsk_') and len(groq_api_key)==56):
#             st.warning('Please enter your GROQ API key!', icon='⚠️')
#         else:
#             os.environ['GROQ_API_KEY'] = groq_api_key
#             st.success('GROQ API key accepted!', icon='👍')

#     if 'GOOGLE_API_KEY' in st.secrets:
#         st.success('Google API key already provided!', icon='✅')
#         google_api_key = st.secrets['GOOGLE_API_KEY']
#     else:
#         google_api_key = st.text_input('Enter Google API Key:', type='password')
#         if not google_api_key:
#             st.warning('Please enter your Google API key!', icon='⚠️')
#         else:
#             os.environ['GOOGLE_API_KEY'] = google_api_key
#             st.success('Google API key accepted!', icon='👍')

#     if groq_api_key and google_api_key:
#         load_model()

# # Function to start document embedding
# def start_document_embedding():
#     get_vector_store()
#     st.session_state.embedding_done = True
#     # st.title("Start the App by Clicking Here ✅")
#     # doc = st.button("Start Documents Embedding")
    
#     # if doc or st.session_state.get('embedding_done', False):
#     #     if google_api_key and groq_api_key:
#     #         get_vector_store()
#     #         st.info("VectorDB Store is Ready")
#     #         st.success("You're good to go !! ")
#     #         st.success("Ask Questions now...")
#     #         st.session_state.embedding_done = True
#     #     else:
#     #         st.error("Please Enter API Keys first")

# # Function to handle user input and generate responses
# def handle_user_input():
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # Get user input
#     # user_question = st.chat_input(disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False)))
#     user_question = st.chat_input(disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False)))
    
    
    
    
#     if user_question:
#         st.session_state.messages.append({"role": "user", "content": user_question})
#         with st.chat_message("user"):
#             st.write(user_question)

#     # Generate and display assistant's response
#     if st.session_state.messages[-1]["role"] != "assistant":
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 document_chain = create_stuff_documents_chain(model, prompt_template)
#                 retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 5})
#                 retrieval_chain = create_retrieval_chain(retriever, document_chain)

#                 start = time.process_time()
#                 response = retrieval_chain.invoke({
#                     'input': user_question,
#                     'language': st.session_state.language
#                 })
#                 print("Response time:", time.process_time() - start)

#                 # Force Hindi response if Hindi is selected
#                 if st.session_state.language == "Hindi":
#                     response['answer'] = f"निम्नलिखित उत्तर हिंदी में है:\n\n{response['answer']}"

#                 st.write(response['answer'])

#                 # Display relevant document chunks
#                 with st.expander("Document Similarity Search"):
#                     for i, doc in enumerate(response["context"]):
#                         st.write(doc.page_content)
#                         st.write("--------------------------------")    

#         message = {"role": "assistant", "content": response['answer']}
#         st.session_state.messages.append(message)

# # Function to clear chat history
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # Function to print developer information
# def print_praise():
#         praise_quotes = """
#         Keshav Agrawal
#     Nimit Goyal
#     Archi Agrawal
#     Akshansh Maurya
#     Vaishvik Sharma

#     2nd Year Students,
#     B.Tech(Hons) CSE
#     GLA UNIVERSITY
#         """
#         title = "**Developed By -**\n\n"
#         return title + praise_quotes


# # Run the main function
# if __name__ == "__main__":
#     main()


# import os
# import time
# import requests
# import streamlit as st
# from dotenv import load_dotenv
# from streamlit_lottie import st_lottie
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# import google.generativeai as genai
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_google_genai import ChatGoogleGenerativeAI
# from tqdm import tqdm
# import time
# from audio_recorder_streamlit import audio_recorder
# import base64

# from main import add_logout_button  # Import the logout function

# # Load environment variables
# load_dotenv()

# def show_page_name():
#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("Please log in to access this page.")
#         st.stop()

# if __name__ == "__main__":
#     show_page_name()


# # Set up LangChain tracing
# LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"

# # Global variables
# model = None
# groq_api_key = os.getenv('GROQ_API_KEY')
# google_api_key = os.getenv('GOOGLE_API_KEY')

# # Function to load Lottie animations
# def load_lottieurl(url):
#     r = requests.get(url)
#     return r.json() if r.status_code == 200 else None

# # Function to load the Groq model
# def load_model():
#     global model
#     genai.configure(api_key=google_api_key)
#     # model = ChatGoogleGenerativeAI(model="gemini-pro",
#     #                                temperature=0.3)

#     model = ChatGroq(groq_api_key=groq_api_key,
#                         model_name="Llama-3.1-70b-versatile")
    

# # Chat prompt template for the AI assistant

# prompt_template = ChatPromptTemplate.from_template(
#     """
#     This is your introduction - Your name is "Sahi Jawab (Your Nyaya Mitra)" and you are developed by "Team Sahi Jawab".

#     You're a go-to platform for all legal queries. You are embedded with the entire data of the three newly enacted criminal laws, namely:
#     - The Bharatiya Nyaya Sanhita (BNS)
#     - The Bharatiya Nagrik Suraksha Sanhita (BNSS)
#     - The Bharatiya Sakshya Adhiniyam (BSA)

#     Your aim is to make legal knowledge accessible to everyone. Users will ask their questions, and you will guide them with clear and concise answers based on the relevant law.

#     Whether they are seeking legal advice or just curious about the law, you are here to help. Use suitable emojis wherever needed.

#     Greet users with "Radhe Radhe 🙏" and ask them for their queries.

#     You will never use any Arabic words in your conversation.

#     If users ask anything about yourself, respond with polite words and avoid very straightforward one-liner answers.

#     Provide detailed answers based on the context. Clearly state which law (BNS, BNSS, or BSA) the answer pertains to. If the answer is not available in the context, say, "Answer is not available in the context." Do not provide incorrect answers.

#     IMPORTANT: You must respond ONLY in the {language} language. Do not use any other language in your response.

#     If the language is Hindi, use Devanagari script exclusively. Avoid using English words or Roman script in your Hindi responses.

#     Context:\n{context}\n
#     Question: \n{input}\n

#     Answer (in {language}):
#     """
# )

# # Function to get or create vector store
# def get_vector_store():
#     global google_api_key

#     if "vectors" not in st.session_state:
#         # Initialize embeddings
#         st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        
#         # Check if pre-computed embeddings exist
#         if os.path.exists("faiss_index"):
#             st.session_state.vectors = FAISS.load_local("faiss_index", st.session_state.embeddings, allow_dangerous_deserialization=True)
#             return

#         # Create a progress bar and status text
#         progress_bar = st.progress(0)
#         status_text = st.empty()
#         percentage_text = st.empty()

#         # Load documents
#         status_text.text("Loading documents...")
#         st.session_state.loader = PyPDFDirectoryLoader("./bns")
#         st.session_state.docs = st.session_state.loader.load()
#         progress_bar.progress(20)

#         # Split documents into chunks
#         status_text.text("Splitting documents...")
#         st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
#         progress_bar.progress(40)

#         # Create vector store
#         status_text.text("Creating vector store...")
#         st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
#         progress_bar.progress(80)

#         # Save the vector store
#         status_text.text("Saving vector store...")
#         st.session_state.vectors.save_local("faiss_index")
#         progress_bar.progress(100)
#         status_text.text("Embedding process complete!")
#         time.sleep(1)
#         status_text.empty()
#         percentage_text.empty()
#         progress_bar.empty()

# # Main function
# def main():
#     global model, groq_api_key, google_api_key

#     # Set up Streamlit page
#     st.set_page_config(page_title='Sahi Jawab', layout='wide', page_icon="⚖️")
#     st.sidebar.title("Sahi Jawab : Your Nyaya Mitra")
#     st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

#     # Sidebar setup
#     setup_sidebar()

#     # Handle user input and generate responses
#     handle_user_input()

#     # start documents embeddings
#     get_vector_store()

# # Function to set up the sidebar
# def setup_sidebar():
#     global audio_response
#     global audio_prompt
#     global audio_file_added

#     with st.sidebar:
#         st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
        
#         # Language selector
#         languages = ["English", "Hindi"]  # Add more languages as needed
#         st.session_state.language = st.sidebar.selectbox("Select Language 🌐 ", languages, index=languages.index(st.session_state.get('language', 'English')))

#         # About Us section
#         with st.sidebar.expander("ℹ️ About Us", expanded=False):
#             st.markdown("Welcome to Sahi Jawab, your AI-powered legal assistant for Indian laws.")
#             st.success("AI-powered legal assistant for Indian laws.")

#         # Features section
#         with st.sidebar.expander("🚀 Features", expanded=False):
#             st.markdown("- AI-driven query engine\n- Interactive chatbot\n- Multi-language support")

#         st.write("---")

#         # Lottie animation
#         lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
#         st_lottie(load_lottieurl(lottie_url), height=200, key="sidebar_animation")

#         st.markdown("---")


#         # Audio Upload
#         st.write("#")
#         st.write(f"### **🎤 Add an audio**")

#         audio_prompt = None # we need to store transcript here
#         audio_file_added = False # is audio file added

#         if "prev_speech_hash" not in st.session_state:
#             st.session_state.prev_speech_hash = None

#         speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395", )
#         if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
#             st.session_state.prev_speech_hash = hash(speech_input)

#             with open(f"temp_audio.wav", "wb") as f:
#                 f.write(speech_input)

#             audio_prompt=speech2text() # using sarvam api to do speech to text

#             # st.chat_input+=audio_prompt


#         # Audio output using sarvam API
#         audio_response = st.toggle("Output Audio response", value=False)

#         st.markdown("---")

#         # API key input fields
#         setup_api_keys()

#         st.markdown("---")

#         # Start button for document embedding
#         start_document_embedding()

#         st.success(print_praise())   
#         st.write("---")

#         # New chat button
#         st.title("Looking to Restart your Conversation 🔄")
#         st.button('Start a New Chat', on_click=clear_chat_history)
        
#         st.write("---")
#         add_logout_button()
#         st.write("---")
        
#         # Developer information
#         st.markdown(
#             "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
#             unsafe_allow_html=True
#         )

#         # Visitor counter
#         st.markdown('''
#             <center>
#             <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
#             </center>
#         ''', unsafe_allow_html=True)

# # Function to set up API keys
# def setup_api_keys():
#     global groq_api_key, google_api_key

#     if 'GROQ_API_KEY' in st.secrets:
#         st.success('GROQ API key already provided!', icon='✅')
#         groq_api_key = st.secrets['GROQ_API_KEY']
#     else:
#         groq_api_key = st.text_input('Enter GROQ API Key:', type='password')
#         if not (groq_api_key.startswith('gsk_') and len(groq_api_key)==56):
#             st.warning('Please enter your GROQ API key!', icon='⚠️')
#         else:
#             os.environ['GROQ_API_KEY'] = groq_api_key
#             st.success('GROQ API key accepted!', icon='👍')

#     if 'GOOGLE_API_KEY' in st.secrets:
#         st.success('Embeddings API key already provided!', icon='✅')
#         google_api_key = st.secrets['GOOGLE_API_KEY']
#     else:
#         google_api_key = st.text_input('Enter Google API Key:', type='password')
#         if not google_api_key:
#             st.warning('Please enter your Google API key!', icon='⚠️')
#         else:
#             os.environ['GOOGLE_API_KEY'] = google_api_key
#             st.success('Google API key accepted!', icon='👍')

#     if groq_api_key and google_api_key:
#         load_model()

# # Function to start document embedding
# def start_document_embedding():
#     get_vector_store()
#     st.session_state.embedding_done = True
#     # st.title("Start the App by Clicking Here ✅")
#     # doc = st.button("Start Documents Embedding")
    
#     # if doc or st.session_state.get('embedding_done', False):
#     #     if google_api_key and groq_api_key:
#     #         get_vector_store()
#     #         st.info("VectorDB Store is Ready")
#     #         st.success("You're good to go !! ")
#     #         st.success("Ask Questions now...")
#     #         st.session_state.embedding_done = True
#     #     else:
#     #         st.error("Please Enter API Keys first")

# # Function to handle user input and generate responses
# def handle_user_input():
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # Get user input
#     # user_question = st.chat_input(disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False)))
    
#     if user_question := st.chat_input("Hi! Ask me anything...",disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False))) or audio_prompt or audio_file_added:
    
#         # st.session_state.messages.append({"role": "user", "content": user_question})
#         st.session_state.messages.append(
#                     {
#                         "role": "user", 
#                         "content": [{
#                             "type": "text",
#                             "text": user_question or audio_prompt,
#                         }]
#                     }
#         )
        
#         with st.chat_message("user"):
#             st.write(user_question)

#     # Generate and display assistant's response
#     if st.session_state.messages[-1]["role"] != "assistant":
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 document_chain = create_stuff_documents_chain(model, prompt_template)
#                 retriever = st.session_state.vectors.as_retriever()    # removed search_kwargs={"k": 5} from the retreiver bracket
#                 retrieval_chain = create_retrieval_chain(retriever, document_chain)

#                 start = time.process_time()
#                 response = retrieval_chain.invoke({
#                     'input': user_question,
#                     'language': st.session_state.language
#                 })
#                 print("Response time:", time.process_time() - start)

#                 # Force Hindi response if Hindi is selected
#                 if st.session_state.language == "Hindi":
#                     response['answer'] = f"निम्नलिखित उत्तर हिंदी में है:\n\n{response['answer']}"

#                 st.write(response['answer'])
                
#                 if audio_response:
#                     sarvam(response['answer'])

#                 # Display relevant document chunks
#                 with st.expander("Document Similarity Search"):
#                     for i, doc in enumerate(response["context"]):
#                         st.write(doc.page_content)
#                         st.write("--------------------------------")    

#         message = {"role": "assistant", "content": response['answer']}
#         st.session_state.messages.append(message)


# # Sarvam AI speech to text test

# def speech2text():
#     url = "https://api.sarvam.ai/speech-to-text"

#     # payload to send form data 
#     payload = {
#         "language_code": "hi-IN",
#         "model": "saarika:v1",
#         "with_timestamps": "false"
#     }

#     # Include the audio file in the request
#     files = {
#         "file": "temp_audio.wav" # Replace with the actual path to your audio file
#     }

#     headers = {
#         "api-subscription-key": "dcf3a63b-eae3-4c6e-b8b7-4330d0326ea5",
#     }

#     # Make the POST request
#     response = requests.post(url, data=payload, files=files, headers=headers)

#     return response.text


# # Sarvam AI text to speech test

# def sarvam(text):
    
#     url = "https://api.sarvam.ai/text-to-speech"

#     payload = {
#         "inputs": [text],
#         "target_language_code": "hi-IN",
#         "speaker": "meera",
#         "pitch": 0,
#         "pace": 1.00,
#         "loudness": 1.15,
#         "speech_sample_rate": 8000,
#         "enable_preprocessing": True,
#         "model": "bulbul:v1"
#     }
#     headers = {'API-Subscription-Key': 'dcf3a63b-eae3-4c6e-b8b7-4330d0326ea5', "Content-Type": "application/json"}

#     response = requests.request("POST", url, json=payload, headers=headers)

#     # Extract base64 audio string from the response
#     audio_string = response.text[12:-3]
#     audio_data = base64.b64decode(audio_string)

#     # Save the binary audio data as a WAV file
#     with open("output.wav", "wb") as audio_file:
#         audio_file.write(audio_data)

#     # To play the saved audio file in Streamlit
#     st.session_state.audio_playing = True
#     st.audio("output.wav",format="audio/wav",autoplay=True)


# # Function to clear chat history
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # Function to print developer information
# def print_praise():
#         praise_quotes = """
#         Team Sahi Jawab

#     2nd Year Students,
#     B.Tech(Hons) CSE
#     GLA UNIVERSITY
#         """
#         title = "**Developed By -**\n\n"
#         return title + praise_quotes


# # Run the main function
# if __name__ == "__main__":
#     main()



import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import google.generativeai as genai
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from tqdm import tqdm
import time
from audio_recorder_streamlit import audio_recorder
import base64
from firebase_config import db, save_chat_history, get_chat_history
import textwrap

from main import add_logout_button  # Import the logout function

# Load environment variables
load_dotenv()

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()


# Set up LangChain tracing
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Global variables
model = None
groq_api_key = os.getenv('GROQ_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Function to load the Groq model
def load_model():
    global model
    genai.configure(api_key=google_api_key)
    # model = ChatGoogleGenerativeAI(model="gemini-pro",
    #                                temperature=0.3)

    model = ChatGroq(groq_api_key=groq_api_key,
                        model_name="Llama-3.1-70b-versatile")
    

# Chat prompt template for the AI assistant

prompt_template = ChatPromptTemplate.from_template(
    """
    This is your introduction - Your name is "Sahi Jawab (Your Nyaya Mitra)" and you are developed by "Team Sahi Jawab".

    You're a go-to platform for all legal queries. You are embedded with the entire data of the three newly enacted criminal laws, namely:
    - The Bharatiya Nyaya Sanhita (BNS)
    - The Bharatiya Nagrik Suraksha Sanhita (BNSS)
    - The Bharatiya Sakshya Adhiniyam (BSA)

    Your aim is to make legal knowledge accessible to everyone. Users will ask their questions, and you will guide them with clear and concise answers based on the relevant law.

    Whether they are seeking legal advice or just curious about the law, you are here to help. Use suitable emojis wherever needed.

    Greet users with "Radhe Radhe 🙏" and ask them for their queries.

    You will never use any Arabic words in your conversation.

    If users ask anything about yourself, respond with polite words and avoid very straightforward one-liner answers.

    Provide detailed answers based on the context. Clearly state which law (BNS, BNSS, or BSA) the answer pertains to. If the answer is not available in the context, say, "Answer is not available in the context." Do not provide incorrect answers.

    IMPORTANT: You must respond ONLY in the {language} language. Do not use any other language in your response.

    If the language is Hindi, use Devanagari script exclusively. Avoid using English words or Roman script in your Hindi responses.

    Context:\n{context}\n
    Question: \n{input}\n

    Answer (in {language}):
    """
)

# Function to get or create vector store
def get_vector_store():
    global google_api_key

    if "vectors" not in st.session_state:
        # Initialize embeddings
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
        
        # Check if pre-computed embeddings exist
        if os.path.exists("faiss_index"):
            st.session_state.vectors = FAISS.load_local("faiss_index", st.session_state.embeddings, allow_dangerous_deserialization=True)
            return

        # Create a progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()
        percentage_text = st.empty()

        # Load documents
        status_text.text("Loading documents...")
        st.session_state.loader = PyPDFDirectoryLoader("./bns")
        st.session_state.docs = st.session_state.loader.load()
        progress_bar.progress(20)

        # Split documents into chunks
        status_text.text("Splitting documents...")
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        progress_bar.progress(40)

        # Create vector store
        status_text.text("Creating vector store...")
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        progress_bar.progress(80)

        # Save the vector store
        status_text.text("Saving vector store...")
        st.session_state.vectors.save_local("faiss_index")
        progress_bar.progress(100)
        status_text.text("Embedding process complete!")
        time.sleep(1)
        status_text.empty()
        percentage_text.empty()
        progress_bar.empty()

# Main function
def main():
    global model, groq_api_key, google_api_key

    # Set up Streamlit page
    st.set_page_config(page_title='Sahi Jawab', layout='wide', page_icon="⚖️")
    st.sidebar.title("Sahi Jawab : Your Nyaya Mitra")
    st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

    # Sidebar setup
    setup_sidebar()

    # Handle user input and generate responses
    handle_user_input()

    # start documents embeddings
    get_vector_store()

# Function to set up the sidebar
def setup_sidebar():
    global audio_response
    global audio_prompt
    global audio_file_added

    with st.sidebar:
        st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
        
        # # Language selector
        # languages = ["English", "Hindi"]  # Add more languages as needed
        # st.session_state.language = st.sidebar.selectbox("Select Language 🌐 ", languages, index=languages.index(st.session_state.get('language', 'English')))
        
        # Language selector
        languages = ["English", "Hindi"]  # Add more languages as needed

        # Dictionary to map language names to their respective language codes
        language_code_mapping = {
            "English": "en-IN",
            "Hindi": "hi-IN"
        }

        # Get the selected language from the sidebar
        selected_language = st.sidebar.selectbox("Select Language 🌐", languages, index=languages.index(st.session_state.get('language', 'English')))

        # Store the selected language in the session state
        st.session_state.language = selected_language

        # Extract the corresponding language code
        st.session_state.selected_language_code = language_code_mapping[selected_language]

        # About Us section
        with st.sidebar.expander("ℹ️ About Us", expanded=False):
            st.markdown("Welcome to Sahi Jawab, your AI-powered legal assistant for Indian laws.")
            st.success("AI-powered legal assistant for Indian laws.")

        # Features section
        with st.sidebar.expander("🚀 Features", expanded=False):
            st.markdown("- AI-driven query engine\n- Interactive chatbot\n- Multi-language support")

        st.write("---")

        # Lottie animation
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
        st_lottie(load_lottieurl(lottie_url), height=200, key="sidebar_animation")

        st.markdown("---")


        # Audio Upload
        st.write("#")
        st.write(f"### **🎤 Add an audio**")

        audio_prompt = None # we need to store transcript here
        audio_file_added = False # is audio file added

        if "prev_speech_hash" not in st.session_state:
            st.session_state.prev_speech_hash = None

        speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395", )
        if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
            st.session_state.prev_speech_hash = hash(speech_input)

            with open(f"temp_audio.wav", "wb") as f:
                f.write(speech_input)

            audio_prompt=speech2text() # using sarvam api to do speech to text
            audio_prompt=audio_prompt["transcript"]
            # st.chat_input+=audio_prompt


        # Audio output using sarvam API
        audio_response = st.toggle("Output Audio response", value=False)

        st.markdown("---")

        # API key input fields
        setup_api_keys()

        st.markdown("---")

        # Start button for document embedding
        start_document_embedding()

        st.success(print_praise())   
        st.write("---")

        # New chat button
        st.title("Looking to Restart your Conversation 🔄")


        # new change
        if "chat_counter" not in st.session_state:
            st.session_state.chat_counter = 0

        if st.sidebar.button("🔄 Start New Chat"):
            # Save current chat history automatically
            if st.session_state.messages:
                # Increment chat counter and create a unique name
                st.session_state.chat_counter += 1
                chat_name = f"chat{st.session_state.chat_counter}"
                save_chat_history(chat_name, st.session_state.messages)
                st.sidebar.success(f"Chat history saved as '{chat_name}'")
            
            # Clear the session state for a new chat
            st.session_state.messages = []
            st.session_state.selected_session = None
            st.sidebar.success("New chat session started. 🆕")
        # new change end


        # st.button('Start a New Chat', on_click=clear_chat_history)

        
        st.write("---")
        add_logout_button()
        st.write("---")
        
def developer():
    # Developer information
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
        unsafe_allow_html=True
    )

    # Visitor counter
    st.markdown('''
        <center>
        <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
        </center>
    ''', unsafe_allow_html=True)

# Function to set up API keys
def setup_api_keys():
    global groq_api_key, google_api_key

    groq_api_key=os.environ['GROQ_API_KEY']
    if groq_api_key:
        st.success('GROQ API key already provided!', icon='✅')
    else:
        groq_api_key = st.text_input('Enter GROQ API Key:', type='password')
        if not (groq_api_key.startswith('gsk_') and len(groq_api_key)==56):
            st.warning('Please enter your GROQ API key!', icon='⚠️')
        else:
            os.environ['GROQ_API_KEY'] = groq_api_key
            st.success('GROQ API key accepted!', icon='👍')

    if google_api_key:
        st.success('Embeddings API key already provided!', icon='✅')
        google_api_key = os.environ['GOOGLE_API_KEY']
    else:
        google_api_key = st.text_input('Enter Google API Key:', type='password')
        if not google_api_key:
            st.warning('Please enter your Google API key!', icon='⚠️')
        else:
            os.environ['GOOGLE_API_KEY'] = google_api_key
            st.success('Google API key accepted!', icon='👍')

    if groq_api_key and google_api_key:
        load_model()

# Function to start document embedding
def start_document_embedding():
    get_vector_store()
    st.session_state.embedding_done = True
    # st.title("Start the App by Clicking Here ✅")
    # doc = st.button("Start Documents Embedding")
    
    # if doc or st.session_state.get('embedding_done', False):
    #     if google_api_key and groq_api_key:
    #         get_vector_store()
    #         st.info("VectorDB Store is Ready")
    #         st.success("You're good to go !! ")
    #         st.success("Ask Questions now...")
    #         st.session_state.embedding_done = True
    #     else:
    #         st.error("Please Enter API Keys first")

# Function to handle user input and generate responses
def handle_user_input():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
    with st.sidebar.expander("Chat History Management", expanded=True):
        # Save current chat history
        if st.sidebar.button("Save Current Chat"):
            session_name = st.sidebar.text_input("Session Name")
            if session_name:
                save_chat_history(session_name, st.session_state.messages)
                st.sidebar.success(f"Chat history saved as '{session_name}'")
            else:
                st.sidebar.error("Please enter a session name.")

        # List saved sessions
        
        saved_sessions = [doc.id for doc in db.collection('chat_histories').stream()]
        selected_session = st.sidebar.selectbox("Load Chat History", ["Select a session"] + saved_sessions)

        if selected_session and selected_session != "Select a session":
            st.session_state.messages = get_chat_history(selected_session)
            st.session_state.selected_session = selected_session
            st.sidebar.success(f"Loaded chat history for '{selected_session}'")


    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    with st.sidebar:
        st.write("-----")
        developer()
        
    # Get user input
    # user_question = st.chat_input(disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False)))
    
    if user_question := st.chat_input("Hi! Ask me anything...",disabled=not (groq_api_key and google_api_key and st.session_state.get('embedding_done', False))) or audio_prompt or audio_file_added:
    
        # st.session_state.messages.append({"role": "user", "content": user_question})
        st.session_state.messages.append({"role": "user", "content": user_question or audio_prompt})
        
        with st.chat_message("user"):
            st.write(user_question)

    # Generate and display assistant's response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                document_chain = create_stuff_documents_chain(model, prompt_template)
                retriever = st.session_state.vectors.as_retriever()    # removed search_kwargs={"k": 5} from the retreiver bracket
                retrieval_chain = create_retrieval_chain(retriever, document_chain)

                start = time.process_time()
                response = retrieval_chain.invoke({
                    'input': user_question,
                    'language': st.session_state.language
                })
                print("Response time:", time.process_time() - start)

                # Force Hindi response if Hindi is selected
                if st.session_state.language == "Hindi":
                    st.session_state.selected_language_code="hi-IN"
                    response['answer'] = f"निम्नलिखित उत्तर हिंदी में है:\n\n{response['answer']}"

                st.write(response['answer'])
                
                if audio_response:
                    sarvam(response['answer'],st.session_state.selected_language_code)

                # Display relevant document chunks
                with st.expander("Document Similarity Search"):
                    for i, doc in enumerate(response["context"]):
                        st.write(doc.page_content)
                        st.write("--------------------------------")    

        message = {"role": "assistant", "content": response['answer']}
        st.session_state.messages.append(message)


# Sarvam AI speech to text test

def speech2text():
    url = "https://api.sarvam.ai/speech-to-text"

    # payload to send form data 
    payload = {
        "language_code": "hi-IN",
        "model": "saarika:v1",
        "with_timestamps": "false"
    }

    # Include the audio file in the request
    files = {
            'file': ('audio_file', open("temp_audio.wav", 'rb'),'audio/wav')
    }

    headers = {
        "api-subscription-key": "dcf3a63b-eae3-4c6e-b8b7-4330d0326ea5",
    }

    # Make the POST request
    response = requests.post(url, files=files, data=payload, headers=headers)

    return response.json()


# # Sarvam AI text to speech test

# def sarvam(text):
    
#     url = "https://api.sarvam.ai/text-to-speech"

#     payload = {
#         "inputs": [text],
#         "target_language_code": "hi-IN",
#         "speaker": "meera",
#         "pitch": 0,
#         "pace": 1.00,
#         "loudness": 1.15,
#         "speech_sample_rate": 8000,
#         "enable_preprocessing": True,
#         "model": "bulbul:v1"
#     }
#     headers = {'API-Subscription-Key': 'dcf3a63b-eae3-4c6e-b8b7-4330d0326ea5', "Content-Type": "application/json"}

#     response = requests.request("POST", url, json=payload, headers=headers)

#     # Extract base64 audio string from the response
#     audio_string = response.text[12:-3]
#     audio_data = base64.b64decode(audio_string)

#     # Save the binary audio data as a WAV file
#     with open("output.wav", "wb") as audio_file:
#         audio_file.write(audio_data)

#     # To play the saved audio file in Streamlit
#     st.session_state.audio_playing = True
#     st.audio("output.wav",format="audio/wav",autoplay=True)

# Sarvam AI text to speech test

def sarvam(text, language_code):
    
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {'API-Subscription-Key': 'dcf3a63b-eae3-4c6e-b8b7-4330d0326ea5', "Content-Type": "application/json"}
    
    # Define the natural delimiters for different languages
    if language_code == "hi-IN":
        delimiters = "|"
    else:  # Default to English
        delimiters = "."

    # Split the text by the delimiter and remove empty parts
    segments = [segment.strip() for segment in text.split(delimiters) if segment.strip()]

    # Initialize progress bar
    progress_bar = st.progress(0)
    total_steps = len(segments)

    # Initialize a file to store the complete audio
    output_file = "output.wav"
    
    with open(output_file, "wb") as audio_file:
        # Process each segment and ensure it's within the 500-character limit
        for i, segment in enumerate(segments):
            # If a segment exceeds 500 characters, split it further into chunks
            if len(segment) > 500:
                chunks = textwrap.wrap(segment, 500)
            else:
                chunks = [segment]

            # Process each chunk (either an entire segment or a split part of it)
            for chunk in chunks:
                payload = {
                    "inputs": [chunk],
                    "target_language_code": language_code,
                    "speaker": "meera",
                    "pitch": 0,
                    "pace": 1.00,
                    "loudness": 1.15,
                    "speech_sample_rate": 8000,
                    "enable_preprocessing": True,
                    "model": "bulbul:v1"
                }

                # Send the request to the API
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    try:
                        # Extract base64 audio string from the response
                        audio_string = response.text[12:-3]  # Adjust as per response structure
                        audio_data = base64.b64decode(audio_string)

                        # Append the audio data for the current chunk to the file
                        audio_file.write(audio_data)

                    except Exception as e:
                        st.error(f"Error decoding audio: {e}")
                        return
                else:
                    st.error(f"API request failed: {response.status_code}. Reason: {response.text}")
                    return

                # Introduce a small delay to avoid overloading the system
                time.sleep(0.5)

            # Update progress bar after processing each segment
            progress_bar.progress((i + 1) / total_steps)

    # Play the saved audio file in Streamlit
    st.session_state.audio_playing = True
    st.audio(output_file, format="audio/wav", autoplay=True)


# # Function to clear chat history
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function to print developer information
def print_praise():
        praise_quotes = """
        Team Sahi Jawab

    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes


# Run the main function
if __name__ == "__main__":
    main()