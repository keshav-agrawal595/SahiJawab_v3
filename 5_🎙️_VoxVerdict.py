# import streamlit as st
# from openai import OpenAI
# import dotenv
# import os
# from PIL import Image
# from audio_recorder_streamlit import audio_recorder
# import base64
# from io import BytesIO
# import google.generativeai as genai
# import random
# import anthropic
# from streamlit_lottie import st_lottie
# import requests
# import streamlit_option_menu as option_menu
# from langchain_groq import ChatGroq
# import groq
# import pyttsx3  # Import pyttsx3 for text-to-speech
# from main import add_logout_button  # Import the logout function
# import speech_recognition as sr
# from pydub import AudioSegment

# dotenv.load_dotenv()

# def show_page_name():
#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("Please log in to access this page.")
#         st.stop()

# # if __name__ == "__main__":
# #     show_page_name()

# # Initialize the audio output
# engine=pyttsx3.init()


# anthropic_models = [
#     "claude-3-5-sonnet-20240620"
# ]

# google_models = [
#     "gemini-1.5-flash",
#     "gemini-1.5-pro",
# ]

# openai_models = [
#     "gpt-4o", 
#     "gpt-4-turbo", 
#     "gpt-3.5-turbo-16k", 
#     "gpt-4", 
#     "gpt-4-32k",
# ]


# # Function to convert the messages format from OpenAI and Streamlit to Gemini
# def messages_to_gemini(messages):
#     gemini_messages = []
#     prev_role = None
#     for message in messages:
#         if prev_role and (prev_role == message["role"]):
#             gemini_message = gemini_messages[-1]
#         else:
#             gemini_message = {
#                 "role": "model" if message["role"] == "assistant" else "user",
#                 "parts": [],
#             }

#         for content in message["content"]:
#             if content["type"] == "text":
#                 gemini_message["parts"].append(content["text"])
#             elif content["type"] == "image_url":
#                 gemini_message["parts"].append(base64_to_image(content["image_url"]["url"]))
#             elif content["type"] == "video_file":
#                 gemini_message["parts"].append(genai.upload_file(content["video_file"]))
#             elif content["type"] == "audio_file":
#                 gemini_message["parts"].append(genai.upload_file(content["audio_file"]))

#         if prev_role != message["role"]:
#             gemini_messages.append(gemini_message)

#         prev_role = message["role"]
        
#     return gemini_messages


# # Function to convert the messages format from OpenAI and Streamlit to Anthropic (the only difference is in the image messages)
# def messages_to_anthropic(messages):
#     anthropic_messages = []
#     prev_role = None
#     for message in messages:
#         if prev_role and (prev_role == message["role"]):
#             anthropic_message = anthropic_messages[-1]
#         else:
#             anthropic_message = {
#                 "role": message["role"] ,
#                 "content": [],
#             }
#         if message["content"][0]["type"] == "image_url":
#             anthropic_message["content"].append(
#                 {
#                     "type": "image",
#                     "source":{   
#                         "type": "base64",
#                         "media_type": message["content"][0]["image_url"]["url"].split(";")[0].split(":")[1],
#                         "data": message["content"][0]["image_url"]["url"].split(",")[1]
#                         # f"data:{img_type};base64,{img}"
#                     }
#                 }
#             )
#         else:
#             anthropic_message["content"].append(message["content"][0])

#         if prev_role != message["role"]:
#             anthropic_messages.append(anthropic_message)

#         prev_role = message["role"]
        
#     return anthropic_messages


# # Function to query and stream the response from the LLM
# def stream_llm_response(model_params, model_type="openai", api_key=None):
#     response_message = ""

#     if model_type == "openai":
#         client = OpenAI(api_key=api_key)
#         for chunk in client.chat.completions.create(
#             model=model_params["model"] if "model" in model_params else "gpt-4o",
#             messages=st.session_state.messages,
#             temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
#             max_tokens=4096,
#             stream=True,
#         ):
#             chunk_text = chunk.choices[0].delta.content or ""
#             response_message += chunk_text
#             yield chunk_text

#     elif model_type == "google":
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel(
#             model_name = model_params["model"],
#             generation_config={
#                 "temperature": model_params["temperature"] if "temperature" in model_params else 0.3,
#             }
#         )
#         gemini_messages = messages_to_gemini(st.session_state.messages)

#         for chunk in model.generate_content(
#             contents=gemini_messages,
#             stream=True,
#         ):
#             chunk_text = chunk.text or ""
#             response_message += chunk_text
#             yield chunk_text

#     elif model_type == "anthropic":
#         client = anthropic.Anthropic(api_key=api_key)
#         with client.messages.stream(
#             model=model_params["model"] if "model" in model_params else "claude-3-5-sonnet-20240620",
#             messages=messages_to_anthropic(st.session_state.messages),
#             temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
#             max_tokens=4096,
#         ) as stream:
#             for text in stream.text_stream:
#                 response_message += text
#                 yield text

#     st.session_state.messages.append({
#         "role": "assistant", 
#         "content": [
#             {
#                 "type": "text",
#                 "text": response_message,
#             }
#         ]})


# # Function to convert file to base64
# def get_image_base64(image_raw):
#     buffered = BytesIO()
#     image_raw.save(buffered, format=image_raw.format)
#     img_byte = buffered.getvalue()

#     return base64.b64encode(img_byte).decode('utf-8')

# def file_to_base64(file):
#     with open(file, "rb") as f:

#         return base64.b64encode(f.read())

# def base64_to_image(base64_string):
#     base64_string = base64_string.split(",")[1]
    
#     return Image.open(BytesIO(base64.b64decode(base64_string)))


# # Function to handle audio input and transcribe it
# def handle_audio_input(audio_data):
#     recognizer = sr.Recognizer()

#     # Convert the audio data to a recognizable format for speech recognition
#     with sr.AudioFile(audio_data) as source:
#         audio = recognizer.record(source)
    
#     try:
#         # Transcribe the audio using Google Web Speech API
#         transcript = recognizer.recognize_google(audio)
#         return transcript
#     except sr.UnknownValueError:
#         return "Sorry, I could not understand the audio."
#     except sr.RequestError:
#         return "Sorry, there was an issue with the speech recognition service."


# def main():

#     # --- Page Config ---
#     st.set_page_config(
#         page_title="VoxVerdict",
#         page_icon="🎙️",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

#     # --- Header ---
#     st.title(" 🎙️ VoxVerdict: Talk in your own Style")

#     engine = pyttsx3.init()

#     # --- Side Bar ---
#     with st.sidebar:
#         cols_keys = st.columns(2)
#         with cols_keys[0]:
#             default_openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
#             with st.popover("🔐 OpenAI"):
#                 openai_api_key = st.text_input("Introduce your OpenAI API Key (https://platform.openai.com/)", value=default_openai_api_key, type="password")
        
#         with cols_keys[1]:
#             default_google_api_key = os.getenv("GOOGLE_API_KEY") if os.getenv("GOOGLE_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
#             with st.popover("🔐 Google"):
#                 google_api_key = st.text_input("Introduce your Google API Key (https://aistudio.google.com/app/apikey)", value=default_google_api_key, type="password")

#         default_anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") if os.getenv("ANTHROPIC_API_KEY") is not None else ""
#         with st.popover("🔐 Anthropic"):
#             anthropic_api_key = st.text_input("Introduce your Anthropic API Key (https://console.anthropic.com/)", value=default_anthropic_api_key, type="password")
    
#     # --- Main Content ---
#     # Checking if the user has introduced the OpenAI API Key, if not, a warning is displayed
#     if (openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key) and (google_api_key == "" or google_api_key is None) and (anthropic_api_key == "" or anthropic_api_key is None):
#         st.write("#")
#         st.warning("⬅️ Please introduce an API Key to continue...")

#         with st.sidebar:
#             st.write("#")

#     else:
#         client = OpenAI(api_key=openai_api_key)

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Displaying the previous messages if there are any
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 for content in message["content"]:
#                     if content["type"] == "text":
#                         st.write(content["text"])
#                     elif content["type"] == "image_url":      
#                         st.image(content["image_url"]["url"])
#                     elif content["type"] == "video_file":
#                         st.video(content["video_file"])
#                     elif content["type"] == "audio_file":
#                         st.audio(content["audio_file"])

#         # Side bar model options and inputs
#         with st.sidebar:

#             st.divider()
            
#             available_models = [] + (anthropic_models if anthropic_api_key else []) + (google_models if google_api_key else []) + (openai_models if openai_api_key else [])
#             model = st.selectbox("Select a model:", available_models, index=0)
#             model_type = None
#             if model.startswith("gpt"): model_type = "openai"
#             elif model.startswith("gemini"): model_type = "google"
#             elif model.startswith("claude"): model_type = "anthropic"
            
#             with st.popover("⚙️ Model parameters"):
#                 model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)

#             audio_response = st.toggle("Audio response", value=False)

#             model_params = {
#                 "model": model,
#                 "temperature": model_temp,
#             }

#             def reset_conversation():
#                 if "messages" in st.session_state and len(st.session_state.messages) > 0:
#                     st.session_state.pop("messages", None)

#             st.button(
#                 "🗑️ Reset conversation", 
#                 on_click=reset_conversation,
#             )

#             st.divider()

#             # Image Upload
#             if model in ["gpt-4o", "gpt-4-turbo", "gemini-1.5-flash", "gemini-1.5-pro", "claude-3-5-sonnet-20240620"]:
                    
#                 st.write(f"### **🖼️ Add an image{' or a video file' if model_type=='google' else ''}:**")

#                 def add_image_to_messages():
#                     if st.session_state.uploaded_img or ("camera_img" in st.session_state and st.session_state.camera_img):
#                         img_type = st.session_state.uploaded_img.type if st.session_state.uploaded_img else "image/jpeg"
#                         if img_type == "video/mp4":
#                             # save the video file
#                             video_id = random.randint(100000, 999999)
#                             with open(f"video_{video_id}.mp4", "wb") as f:
#                                 f.write(st.session_state.uploaded_img.read())
#                             st.session_state.messages.append(
#                                 {
#                                     "role": "user", 
#                                     "content": [{
#                                         "type": "video_file",
#                                         "video_file": f"video_{video_id}.mp4",
#                                     }]
#                                 }
#                             )
#                         else:
#                             raw_img = Image.open(st.session_state.uploaded_img or st.session_state.camera_img)
#                             img = get_image_base64(raw_img)
#                             st.session_state.messages.append(
#                                 {
#                                     "role": "user", 
#                                     "content": [{
#                                         "type": "image_url",
#                                         "image_url": {"url": f"data:{img_type};base64,{img}"}
#                                     }]
#                                 }
#                             )

#                 cols_img = st.columns(2)

#                 with cols_img[0]:
#                     with st.popover("📁 Upload"):
#                         st.file_uploader(
#                             f"Upload an image{' or a video' if model_type == 'google' else ''}:", 
#                             type=["png", "jpg", "jpeg"] + (["mp4"] if model_type == "google" else []), 
#                             accept_multiple_files=False,
#                             key="uploaded_img",
#                             on_change=add_image_to_messages,
#                         )

#                 with cols_img[1]:                    
#                     with st.popover("📸 Camera"):
#                         activate_camera = st.checkbox("Activate camera")
#                         if activate_camera:
#                             st.camera_input(
#                                 "Take a picture", 
#                                 key="camera_img",
#                                 on_change=add_image_to_messages,
#                             )

#             # Audio Upload
#             st.write("#")
#             st.write(f"### **🎤 Add an audio{' (Speech To Text)' if model_type == 'google' else ''}:**")

#             audio_prompt = None
#             audio_file_added = False
#             if "prev_speech_hash" not in st.session_state:
#                 st.session_state.prev_speech_hash = None

#             speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395", )
#             if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
#                 st.session_state.prev_speech_hash = hash(speech_input)
#                 if model_type != "google":
#                     transcript = client.audio.transcriptions.create(
#                         model="whisper-1", 
#                         file=("audio.wav", speech_input),
#                     )

#                     audio_prompt = transcript.text

#                 elif model_type == "google":
#                     # save the audio file
#                     with open(f"temp_audio.wav", "wb") as f:
#                         f.write(speech_input)
#                     audio_prompt = handle_audio_input("temp_audio.wav")

#             st.divider()


#         # Chat input
#         if prompt := st.chat_input("Hi! Ask me anything...") or audio_prompt or audio_file_added:
#             if not audio_file_added:
#                 st.session_state.messages.append(
#                     {
#                         "role": "user", 
#                         "content": [{
#                             "type": "text",
#                             "text": prompt or audio_prompt,
#                         }]
#                     }
#                 )
                
#                 # Display the new messages
#                 with st.chat_message("user"):
#                     st.markdown(prompt)

#             else:
#                 # Display the audio file
#                 with st.chat_message("user"):
#                     st.audio(f"temp_audio.wav")

#             with st.chat_message("assistant"):
#                 model2key = {
#                     "openai": openai_api_key,
#                     "google": google_api_key,
#                     "anthropic": anthropic_api_key,
#                 }

#                 response = "".join(
#                     stream_llm_response(
#                         model_params=model_params, 
#                         model_type=model_type, 
#                         api_key=model2key[model_type]
#                     )
#                 )
#                 st.write(response)

#                 # Use pyttsx3 for audio response
#                 if audio_response:
#                     engine.say(response)
#                     engine.runAndWait()

#     def print_praise():
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

#     with st.sidebar:
#         with st.popover("❌ Stop Audio Response"):
#             st.info("Click only, if you want to stop the current voice response")
#             st.button("⚠️ Stop",on_click=engine.stop())
#         st.write("---")
#         st.success(print_praise())
#         st.write("---")
#         st.write("---")
#         add_logout_button()
#         st.write("---")
#         st.markdown(
#                 "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
#                 unsafe_allow_html=True
#             )
#         st.divider()
#         st.markdown('''
#                 <center>
#                 <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
#                 </center>
#             ''', unsafe_allow_html=True)



# if __name__=="__main__":
#     main()

# VoxVerdict for streamlit cloud

import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
from audio_recorder_streamlit import audio_recorder
import base64
from io import BytesIO
import google.generativeai as genai
import random
import anthropic
from streamlit_lottie import st_lottie
from main import add_logout_button  # Import the logout function
import speech_recognition as sr
from gtts import gTTS
import io

dotenv.load_dotenv()

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()

# Initialize session state for audio control
if 'audio_playing' not in st.session_state:
    st.session_state.audio_playing = False


def text_to_speech(text):
    # Create gTTS object and save to a file-like object
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    # Save the audio file to disk or a file-like object for later use
    with open("output.mp3", "wb") as f:
        f.write(fp.read())
    
    # To play the saved audio file in Streamlit
    st.session_state.audio_playing = True
    st.audio("output.mp3",format="audio/mpeg",autoplay=True)


anthropic_models = [
    "claude-3-5-sonnet-20240620"
]

google_models = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

openai_models = [
    "gpt-4o", 
    "gpt-4-turbo", 
    "gpt-3.5-turbo-16k", 
    "gpt-4", 
    "gpt-4-32k",
]


# Function to convert the messages format from OpenAI and Streamlit to Gemini
def messages_to_gemini(messages):
    gemini_messages = []
    prev_role = None
    for message in messages:
        if prev_role and (prev_role == message["role"]):
            gemini_message = gemini_messages[-1]
        else:
            gemini_message = {
                "role": "model" if message["role"] == "assistant" else "user",
                "parts": [],
            }

        for content in message["content"]:
            if content["type"] == "text":
                gemini_message["parts"].append(content["text"])
            elif content["type"] == "image_url":
                gemini_message["parts"].append(base64_to_image(content["image_url"]["url"]))
            elif content["type"] == "video_file":
                gemini_message["parts"].append(genai.upload_file(content["video_file"]))
            elif content["type"] == "audio_file":
                gemini_message["parts"].append(genai.upload_file(content["audio_file"]))

        if prev_role != message["role"]:
            gemini_messages.append(gemini_message)

        prev_role = message["role"]
        
    return gemini_messages


# Function to convert the messages format from OpenAI and Streamlit to Anthropic (the only difference is in the image messages)
def messages_to_anthropic(messages):
    anthropic_messages = []
    prev_role = None
    for message in messages:
        if prev_role and (prev_role == message["role"]):
            anthropic_message = anthropic_messages[-1]
        else:
            anthropic_message = {
                "role": message["role"] ,
                "content": [],
            }
        if message["content"][0]["type"] == "image_url":
            anthropic_message["content"].append(
                {
                    "type": "image",
                    "source":{   
                        "type": "base64",
                        "media_type": message["content"][0]["image_url"]["url"].split(";")[0].split(":")[1],
                        "data": message["content"][0]["image_url"]["url"].split(",")[1]
                        # f"data:{img_type};base64,{img}"
                    }
                }
            )
        else:
            anthropic_message["content"].append(message["content"][0])

        if prev_role != message["role"]:
            anthropic_messages.append(anthropic_message)

        prev_role = message["role"]
        
    return anthropic_messages


# Function to query and stream the response from the LLM
def stream_llm_response(model_params, model_type="openai", api_key=None):
    response_message = ""

    if model_type == "openai":
        client = OpenAI(api_key=api_key)
        for chunk in client.chat.completions.create(
            model=model_params["model"] if "model" in model_params else "gpt-4o",
            messages=st.session_state.messages,
            temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
            max_tokens=4096,
            stream=True,
        ):
            chunk_text = chunk.choices[0].delta.content or ""
            response_message += chunk_text
            yield chunk_text

    elif model_type == "google":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name = model_params["model"],
            generation_config={
                "temperature": model_params["temperature"] if "temperature" in model_params else 0.3,
            }
        )
        gemini_messages = messages_to_gemini(st.session_state.messages)

        for chunk in model.generate_content(
            contents=gemini_messages,
            stream=True,
        ):
            chunk_text = chunk.text or ""
            response_message += chunk_text
            yield chunk_text

    elif model_type == "anthropic":
        client = anthropic.Anthropic(api_key=api_key)
        with client.messages.stream(
            model=model_params["model"] if "model" in model_params else "claude-3-5-sonnet-20240620",
            messages=messages_to_anthropic(st.session_state.messages),
            temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
            max_tokens=4096,
        ) as stream:
            for text in stream.text_stream:
                response_message += text
                yield text

    st.session_state.messages.append({
        "role": "assistant", 
        "content": [
            {
                "type": "text",
                "text": response_message,
            }
        ]})


# Function to convert file to base64
def get_image_base64(image_raw):
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()

    return base64.b64encode(img_byte).decode('utf-8')

def file_to_base64(file):
    with open(file, "rb") as f:

        return base64.b64encode(f.read())

def base64_to_image(base64_string):
    base64_string = base64_string.split(",")[1]
    
    return Image.open(BytesIO(base64.b64decode(base64_string)))


# Function to handle audio input and transcribe it
def handle_audio_input(audio_data):
    recognizer = sr.Recognizer()

    # Convert the audio data to a recognizable format for speech recognition
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
    
    try:
        # Transcribe the audio using Google Web Speech API
        transcript = recognizer.recognize_google(audio)
        return transcript
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, there was an issue with the speech recognition service."


def main():

    # --- Page Config ---
    st.set_page_config(
        page_title="VoxVerdict",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

    # --- Header ---
    st.title(" 🎙️ VoxVerdict: Talk in your own Style")
    st.markdown('####')

    # --- Side Bar ---
    with st.sidebar:
        cols_keys = st.columns(2)
        with cols_keys[0]:
            default_openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
            with st.popover("🔐 OpenAI"):
                openai_api_key = st.text_input("Introduce your OpenAI API Key (https://platform.openai.com/)", value=default_openai_api_key, type="password")
        
        with cols_keys[1]:
            # default_google_api_key = os.getenv("GOOGLE_API_KEY") if os.getenv("GOOGLE_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
            with st.popover("🔐 Google"):
                if 'GOOGLE_API_KEY' in st.secrets:
                    st.success('GOOGLE API key already provided!', icon='✅')
                    google_api_key = st.secrets['GOOGLE_API_KEY']
                else:
                    google_api_key = st.text_input("Introduce your Google API Key (https://aistudio.google.com/app/apikey)", type="password")

        default_anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") if os.getenv("ANTHROPIC_API_KEY") is not None else ""
        with st.popover("🔐 Anthropic"):
            anthropic_api_key = st.text_input("Introduce your Anthropic API Key (https://console.anthropic.com/)", value=default_anthropic_api_key, type="password")
    
    # --- Main Content ---
    # Checking if the user has introduced the OpenAI API Key, if not, a warning is displayed
    if (openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key) and (google_api_key == "" or google_api_key is None) and (anthropic_api_key == "" or anthropic_api_key is None):
        st.write("#")
        st.warning("⬅️ Please introduce an API Key to continue...")

        with st.sidebar:
            st.write("#")

    else:
        client = OpenAI(api_key=openai_api_key)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Displaying the previous messages if there are any
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.write(content["text"])
                    elif content["type"] == "image_url":      
                        st.image(content["image_url"]["url"])
                    elif content["type"] == "video_file":
                        st.video(content["video_file"])
                    elif content["type"] == "audio_file":
                        st.audio(content["audio_file"])

        # Side bar model options and inputs
        with st.sidebar:

            st.divider()
            
            available_models = [] + (anthropic_models if anthropic_api_key else []) + (google_models if google_api_key else []) + (openai_models if openai_api_key else [])
            model = st.selectbox("Select a model:", available_models, index=0)
            model_type = None
            if model.startswith("gpt"): model_type = "openai"
            elif model.startswith("gemini"): model_type = "google"
            elif model.startswith("claude"): model_type = "anthropic"
            
            with st.popover("⚙️ Model parameters"):
                model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.1)

            audio_response = st.toggle("Audio response", value=False)

            model_params = {
                "model": model,
                "temperature": model_temp,
            }

            def reset_conversation():
                if "messages" in st.session_state and len(st.session_state.messages) > 0:
                    st.session_state.pop("messages", None)

            st.button(
                "🗑️ Reset conversation", 
                on_click=reset_conversation,
            )

            st.divider()

            # Image Upload
            if model in ["gpt-4o", "gpt-4-turbo", "gemini-1.5-flash", "gemini-1.5-pro", "claude-3-5-sonnet-20240620"]:
                    
                st.write(f"### **🖼️ Add an image{' or a video file' if model_type=='google' else ''}:**")

                def add_image_to_messages():
                    if st.session_state.uploaded_img or ("camera_img" in st.session_state and st.session_state.camera_img):
                        img_type = st.session_state.uploaded_img.type if st.session_state.uploaded_img else "image/jpeg"
                        if img_type == "video/mp4":
                            # save the video file
                            video_id = random.randint(100000, 999999)
                            with open(f"video_{video_id}.mp4", "wb") as f:
                                f.write(st.session_state.uploaded_img.read())
                            st.session_state.messages.append(
                                {
                                    "role": "user", 
                                    "content": [{
                                        "type": "video_file",
                                        "video_file": f"video_{video_id}.mp4",
                                    }]
                                }
                            )
                        else:
                            raw_img = Image.open(st.session_state.uploaded_img or st.session_state.camera_img)
                            img = get_image_base64(raw_img)
                            st.session_state.messages.append(
                                {
                                    "role": "user", 
                                    "content": [{
                                        "type": "image_url",
                                        "image_url": {"url": f"data:{img_type};base64,{img}"}
                                    }]
                                }
                            )

                cols_img = st.columns(2)

                with cols_img[0]:
                    with st.popover("📁 Upload"):
                        st.file_uploader(
                            f"Upload an image{' or a video' if model_type == 'google' else ''}:", 
                            type=["png", "jpg", "jpeg"] + (["mp4"] if model_type == "google" else []), 
                            accept_multiple_files=False,
                            key="uploaded_img",
                            on_change=add_image_to_messages,
                        )

                with cols_img[1]:                    
                    with st.popover("📸 Camera"):
                        activate_camera = st.checkbox("Activate camera")
                        if activate_camera:
                            st.camera_input(
                                "Take a picture", 
                                key="camera_img",
                                on_change=add_image_to_messages,
                            )

            # Audio Upload
            st.write("#")
            st.write(f"### **🎤 Add an audio{' (Speech To Text)' if model_type == 'google' else ''}:**")

            audio_prompt = None
            audio_file_added = False
            if "prev_speech_hash" not in st.session_state:
                st.session_state.prev_speech_hash = None

            speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395", )
            if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
                st.session_state.prev_speech_hash = hash(speech_input)
                if model_type != "google":
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=("audio.wav", speech_input),
                    )

                    audio_prompt = transcript.text

                elif model_type == "google":
                    # save the audio file
                    with open(f"temp_audio.wav", "wb") as f:
                        f.write(speech_input)
                    audio_prompt = handle_audio_input("temp_audio.wav")

            st.divider()


        # Chat input
        if prompt := st.chat_input("Hi! Ask me anything...") or audio_prompt or audio_file_added:
            if not audio_file_added:
                st.session_state.messages.append(
                    {
                        "role": "user", 
                        "content": [{
                            "type": "text",
                            "text": prompt or audio_prompt,
                        }]
                    }
                )
                
                # Display the new messages
                with st.chat_message("user"):
                    st.markdown(prompt)

            else:
                # Display the audio file
                with st.chat_message("user"):
                    st.audio(f"temp_audio.wav")

            with st.chat_message("assistant"):
                model2key = {
                    "openai": openai_api_key,
                    "google": google_api_key,
                    "anthropic": anthropic_api_key,
                }

                response = "".join(
                    stream_llm_response(
                        model_params=model_params, 
                        model_type=model_type, 
                        api_key=model2key[model_type]
                    )
                )
                st.write(response)

                # Use pyttsx3 for audio response
                if audio_response:
                    text_to_speech(response)

    def print_praise():
        praise_quotes = """
        Keshav Agrawal
    Nimit Goyal
    Archi Agrawal
    Akshansh Maurya
    Vaishvik Sharma

    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

    with st.sidebar:
        with st.popover("❌ Stop Audio Response"):
            st.info("Click to stop the current voice response")
            if st.button("⚠️ Stop"):
                st.session_state.audio_playing = False
                st.stop()  # This stops the execution of the script, effectively stopping the audio
        
        st.write("---")
        st.success(print_praise())
        st.write("---")
        add_logout_button()
        st.write("---")
        st.markdown(
                "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
                unsafe_allow_html=True
            )
        st.divider()
        st.markdown('''
                <center>
                <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
                </center>
            ''', unsafe_allow_html=True)



if __name__=="__main__":
    main()