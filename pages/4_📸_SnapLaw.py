# import streamlit as st
# import os
# from PIL import Image
# import io
# from streamlit_lottie import st_lottie
# import requests
# from dotenv import load_dotenv
# import google.generativeai as genai
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as PDFImage, Spacer
# from reportlab.lib.colors import HexColor
# from reportlab.lib.enums import TA_CENTER
# from annotated_text import annotated_text
# from reportlab.lib import colors
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib.units import inch
# from main import add_logout_button  # Import the logout function

# load_dotenv()

# def show_page_name():
#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("Please log in to access this page.")
#         st.stop()

# if __name__ == "__main__":
#     show_page_name()

# # Configure Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# st.set_page_config(page_title='SnapLaw - Sahi Jawab', layout='wide', page_icon="📸")
# st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

# # Function to load Lottie animations
# def load_lottieurl(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Load Lottie animations
# lottie_camera = load_lottieurl("https://lottie.host/ff051f81-13ab-42b3-b209-3cad44d690a4/UnrEKrEbeP.json")
# lottie_analysis = load_lottieurl("https://lottie.host/55a9ffe1-1379-4f67-803b-736e360b2a1e/GoUsiPljIX.json")

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background-color: #ffffff;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-weight: bold;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#     }
#     .document-summary {
#         background-color: #f0f0f0;
#         padding: 20px;
#         border-radius: 10px;
#         margin-top: 20px;
#     }
#     .heading {
#         font-size: 20px;
#         font-weight: bold;
#         margin-bottom: 15px;
#         color: #2e7d32;
#     }
#     .image-container {
#         border: 2px solid #4CAF50;
#         border-radius: 10px;
#         padding: 10px;
#         margin-top: 20px;
#     }
#     .summary-table {
#         width: 100%;
#         border-collapse: collapse;
#     }
#     .summary-table th, .summary-table td {
#         border: 1px solid #ddd;
#         padding: 8px;
#         text-align: left;
#     }
#     .summary-table th {
#         background-color: #4CAF50;
#         color: white;
#     }
#     .summary-table tr:nth-child(even) {
#         background-color: #f2f2f2;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
    
#     # About Us in an expander
#     with st.expander("ℹ️ About Us", expanded=False):
#         st.markdown("Welcome to SnapLaw: Instant Legal Document Analysis")
#         st.success("AI-powered legal document analyzer for Indian laws.")

#     # Features in an expander
#     with st.expander("🚀 Features", expanded=False):
#         st.markdown("- Real-time document capture\n- AI-driven analysis\n- Multi-language support")
    
#     def print_praise():
#         praise_quotes = """
#         Team Sahi Jawab

#     2nd Year Students,
#     B.Tech(Hons) CSE
#     GLA UNIVERSITY
#         """
#         title = "**Developed By -**\n\n"
#         return title + praise_quotes


#     st.write("---")
#     add_logout_button()
#     st.write("---")
#     st.success(print_praise())
#     st.write("---")

#     st.markdown(
#         "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
#         unsafe_allow_html=True
#     )

# # Main content
# st.title("Welcome to SnapLaw: Instant Legal Document Analysis")

# col1, col2 = st.columns([1,1])

# with col1:
#     st.markdown("""
#     ### Capture and Analyze Legal Documents in Real-Time
    
#     SnapLaw uses advanced AI to extract crucial information from your legal documents. 
#     Simply capture an image, and let our system do the rest!
    
#     **How it works:**
#     1. Use the camera below to take a clear photo of your legal document
#     2. Our AI will analyze the document and provide a summary
#     """)
# with col2:    
#     st_lottie(lottie_camera, height=300, key="camera")

# # Function to analyze image with Gemini
# def analyze_image(image):
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash')
        
#         # Convert PIL Image to bytes
#         img_byte_arr = io.BytesIO()
#         image.save(img_byte_arr, format='PNG')
#         img_byte_arr = img_byte_arr.getvalue()
        
#         st.write("Sending image to Gemini API...")
#         response = model.generate_content([
#             '''
#             Analyze the uploaded image with a focus on identifying and extracting relevant legal information. Your task is to determine if the image contains a legal document and provide a comprehensive summary of its content. Focus on the following aspects:

#             Document Type: Identify the type of legal document (e.g., contract, deed, affidavit, will, etc.).

#             Parties Involved: Extract the names and roles of all parties mentioned in the document.

#             Important Clauses: Summarize any key clauses, terms, or conditions that are crucial to the document's purpose.

#             Dates and Events: Identify and list any important dates, events, or deadlines mentioned in the document.

#             Property Information: If applicable, extract details about properties, assets, or any other relevant subject matter mentioned.

#             Signatures and Witnesses: Note the presence of any signatures, witnesses, or other markers of document authenticity.

#             Language Analysis: Ensure that the summary is accurate and concise, capturing the document's essence without losing critical legal details.

#             Error Handling: If the document is not recognized as legal or lacks clarity, provide a detailed explanation of why the document could not be analyzed effectively.

#             Prioritize accuracy, relevance, and clarity in the summary to assist users in quickly understanding the core aspects of the document. If additional context is needed to make the analysis precise, request it appropriately.
            
#             ''',
#             {"mime_type": "image/png", "data": img_byte_arr}
#         ])
#         st.write("Received response from Gemini API")
#         return response.text
#     except Exception as e:
#         st.error(f"Error in analyze_image function: {str(e)}")
#         raise

# # Function to create PDF
# def create_pdf(content, image=None):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=30, rightMargin=30)
#     styles = getSampleStyleSheet()
#     story = []

#     # Custom styles
#     styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, spaceAfter=20))
#     styles.add(ParagraphStyle(name='CustomSubtitle', parent=styles['Heading2'], fontSize=18, alignment=TA_CENTER, spaceAfter=15))
#     styles.add(ParagraphStyle(name='CustomBodyText', parent=styles['BodyText'], fontSize=12, spaceAfter=10))
#     styles.add(ParagraphStyle(name='Footer', parent=styles['BodyText'], fontSize=10, textColor=HexColor('#666666'), alignment=TA_CENTER))

#     # Title
#     story.append(Paragraph("Legal Document Analysis", styles['CustomTitle']))
#     story.append(Paragraph("Generated by Sahi Jawab", styles['CustomSubtitle']))
#     story.append(Spacer(1, 20))

#     # Add image to PDF if available
#     if image:
#         image_path = io.BytesIO()
#         image.save(image_path, format='PNG')
#         image_path.seek(0)
#         img = PDFImage(image_path, width=400, height=300)
#         story.append(img)
#         story.append(Spacer(1, 20))

#     # Content as table
#     data = [['Key', 'Value']]
#     for line in content.split('\n'):
#         if ':' in line:
#             key, value = line.split(':', 1)
#             data.append([key.strip(), value.strip()])

#     table = Table(data, colWidths=[doc.width / 2.0] * 2)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.green),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 10),
#         ('TOPPADDING', (0, 1), (-1, -1), 6),
#         ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
#     story.append(table)

#     # Footer
#     story.append(Spacer(1, 30))
#     story.append(Paragraph("Generated by Sahi Jawab | Developed by Keshav Agrawal", styles['Footer']))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # Function to reset state
# def reset_state():
#     st.session_state.img_file_buffer = None
#     st.session_state.analysis_result = None
#     st.session_state.pdf_buffer = None

# # Image capture and analysis
# if 'img_file_buffer' not in st.session_state:
#     st.session_state.img_file_buffer = None

# camera_placeholder = st.empty()
# if st.session_state.img_file_buffer is None:
#     st.session_state.img_file_buffer = camera_placeholder.camera_input("Take a picture")

# if st.session_state.img_file_buffer is not None:
#     bytes_data = st.session_state.img_file_buffer.getvalue()
#     img = Image.open(io.BytesIO(bytes_data))
    
#     # Clear the camera input
#     camera_placeholder.empty()

#     col1, col2 = st.columns([1, 1])
    
#     with col2:
#         st.markdown('<div class="image-container">', unsafe_allow_html=True)
#         st.markdown('<div class="heading">Clicked Legal Document</div>', unsafe_allow_html=True)
#         st.image(img, use_column_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col1:
#         with st.spinner("Processing image... Please wait."):
#             try:
#                 analysis_result = analyze_image(img)
                
#                 if "not a legal document" in analysis_result.lower():
#                     st.warning("The uploaded document seems to have no legal information.")
#                 else:
#                     st.success("Analysis complete!")
                    
#                     # Display the analysis as a table
#                     st.markdown('<div class="document-summary">', unsafe_allow_html=True)
#                     st.markdown('<div class="heading">Key Points after Legal Analysis are:</div>', unsafe_allow_html=True)
                    
#                     table_data = []
#                     for point in analysis_result.split('\n'):
#                         if ':' in point:
#                             key, value = point.split(':', 1)
#                             if value.strip():  # Only add if there's a value
#                                 table_data.append([key.strip(), value.strip()])
                    
#                     if table_data:
#                         st.table(table_data)
#                     else:
#                         st.write("No specific details found in the analysis.")
                    
#                     st.markdown('</div>', unsafe_allow_html=True)
                    
#                     # Create and offer PDF download
#                     pdf_buffer = create_pdf(analysis_result, img)
#                     st.download_button(
#                         label="Download Summary as PDF",
#                         data=pdf_buffer,
#                         file_name="legal_document_summary.pdf",
#                         mime="application/pdf"
#                     )
                    
#                     # Chatbox for further questions
#                     st.subheader("Ask a question about the document")
#                     user_question = st.text_input("Enter your question here:")
#                     if user_question:
#                         with st.spinner("Generating answer..."):
#                             model = genai.GenerativeModel('gemini-1.5-flash')
#                             response = model.generate_content([
#                                 f"Based on this legal document summary: {analysis_result}\n\nAnswer the following question: {user_question}"
#                             ])
#                             st.write(response.text)
                    
#                     # Add reset button
#                     if st.button("Reset and Take New Photo"):
#                         reset_state()
#                         st.rerun()
            
#             except Exception as e:
#                 st.error(f"An error occurred during analysis: {str(e)}")
#                 st.write("Error details:", e)

# # Lottie animation for analysis
# st_lottie(lottie_analysis, height=300, key="analysis")


# # Additional information
# st.markdown("""
# ---
# ### Why Use SnapLaw?

# - **Quick Analysis**: Get instant summaries of complex legal documents
# - **Key Information Extraction**: Automatically identify crucial details like parties involved, property information, and more
# - **Time-Saving**: Skip manual review and get straight to the important parts
# - **User-Friendly**: No need for complex software or legal knowledge

# Remember, while SnapLaw provides a helpful summary, it's always recommended to consult with a legal professional for comprehensive advice.
# """)

# # Footer
# st.markdown("""
# ---
# <p style="text-align: center;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
# """, unsafe_allow_html=True)

# import streamlit as st
# import os
# from PIL import Image
# import io
# import base64
# from streamlit_lottie import st_lottie
# import requests
# import json
# from dotenv import load_dotenv
# import google.generativeai as genai
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as PDFImage, Spacer
# from reportlab.lib.colors import HexColor
# from reportlab.lib.enums import TA_CENTER
# from annotated_text import annotated_text
# from reportlab.lib import colors
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib.units import inch
# from main import add_logout_button  # Import the logout function

# load_dotenv()

# def show_page_name():
#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("Please log in to access this page.")
#         st.stop()

# if __name__ == "__main__":
#     show_page_name()

# st.set_page_config(page_title='SnapLaw - Sahi Jawab', layout='wide', page_icon="📸")
# st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

# # Function to load Lottie animations
# def load_lottieurl(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Load Lottie animations
# lottie_camera = load_lottieurl("https://lottie.host/ff051f81-13ab-42b3-b209-3cad44d690a4/UnrEKrEbeP.json")
# lottie_analysis = load_lottieurl("https://lottie.host/55a9ffe1-1379-4f67-803b-736e360b2a1e/GoUsiPljIX.json")

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background-color: #ffffff;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-weight: bold;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#     }
#     .stButton>button:hover {
#         background-color: #FFFFFF;
#     }
#     .document-summary {
#         background-color: #f0f0f0;
#         padding: 20px;
#         border-radius: 10px;
#         margin-top: 20px;
#     }
#     .heading {
#         font-size: 20px;
#         font-weight: bold;
#         margin-bottom: 15px;
#         color: #2e7d32;
#     }
#     .image-container {
#         border: 2px solid #4CAF50;
#         border-radius: 10px;
#         padding: 10px;
#         margin-top: 20px;
#     }
#     .summary-table {
#         width: 100%;
#         border-collapse: collapse;
#     }
#     .summary-table th, .summary-table td {
#         border: 1px solid #ddd;
#         padding: 8px;
#         text-align: left;
#     }
#     .summary-table th {
#         background-color: #4CAF50;
#         color: white;
#     }
#     .summary-table tr:nth-child(even) {
#         background-color: #f2f2f2;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
    
#     with st.expander("ℹ️ About Us", expanded=False):
#         st.markdown("Welcome to SnapLaw: Instant Legal Document Analysis")
#         st.success("AI-powered legal document analyzer for Indian laws.")

#     with st.expander("🚀 Features", expanded=False):
#         st.markdown("- Real-time document capture\n- AI-driven analysis\n- Multi-language support")
    
#     def print_praise():
#         praise_quotes = """
#         Team Sahi Jawab

#     2nd Year Students,
#     B.Tech(Hons) CSE
#     GLA UNIVERSITY
#         """
#         title = "**Developed By -**\n\n"
#         return title + praise_quotes


#     st.write("---")
#     add_logout_button()
#     st.write("---")
#     st.success(print_praise())
#     st.write("---")

#     st.markdown(
#         "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
#         unsafe_allow_html=True
#     )

# # Main content
# st.title("Welcome to SnapLaw: Instant Legal Document Analysis")

# col1, col2 = st.columns([1,1])

# with col1:
#     st.markdown("""
#     ### Capture and Analyze Legal Documents in Real-Time
    
#     SnapLaw uses advanced AI to extract crucial information from your legal documents. 
#     Simply capture an image, and let our system do the rest!
    
#     **How it works:**
#     1. Use the camera below to take a clear photo of your legal document
#     2. Our AI will analyze the document and provide a summary
#     """)
# with col2:    
#     st.lottie(lottie_camera, height=300, key="camera")

# def process_with_groq(prompt, image=None):
#     try:
#         headers = {
#             "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
#             "Content-Type": "application/json"
#         }
        
#         messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        
#         if image:
#             buffered = io.BytesIO()
#             image.save(buffered, format="JPEG")
#             base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
#             messages[0]["content"].append({
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/jpeg;base64,{base64_image}"
#                 }
#             })
        
#         payload = {
#             "model": "llama-3.2-11b-vision-preview",
#             "messages": messages
#         }
        
#         response = requests.post(
#             "https://api.groq.com/openai/v1/chat/completions",
#             headers=headers,
#             data=json.dumps(payload)
#         )
        
#         if response.status_code == 200:
#             return response.json()['choices'][0]['message']['content']
#         else:
#             st.error(f"Error from Groq API: {response.status_code} - {response.text}")
#             return None
    
#     except Exception as e:
#         st.error(f"Error in process_with_groq function: {str(e)}")
#         raise

# def analyze_image(image):
#     prompt = """
#     Analyze the uploaded image with a focus on identifying and extracting relevant legal information. 
    
#     Your task is to determine if the image contains a legal document and provide a comprehensive summary of its content. Focus on the following aspects:

#     Document Type: Identify the type of legal document (e.g., contract, deed, affidavit, will, etc.).
    
#     Parties Involved: Extract the names and roles of all parties mentioned in the document.
    
#     Important Clauses: Summarize any key clauses, terms, or conditions that are crucial to the document's purpose.
    
#     Dates and Events: Identify and list any important dates, events, or deadlines mentioned in the document.
    
#     Property Information: If applicable, extract details about properties, assets, or any other relevant subject matter mentioned.
    
#     Signatures and Witnesses: Note the presence of any signatures, witnesses, or other markers of document authenticity.
    
#     Language Analysis: Ensure that the summary is accurate and concise, capturing the document's essence without losing critical legal details.
    
#     Error Handling: If the document is not recognized as legal or lacks clarity, provide a detailed explanation of why the document could not be analyzed effectively.

#     Prioritize accuracy, relevance, and clarity in the summary to assist users in quickly understanding the core aspects of the document. If additional context is needed to make the analysis precise, request it appropriately.
#     """
#     return process_with_groq(prompt, image)

# # Function to create PDF
# def create_pdf(content, image=None):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=30, rightMargin=30)
#     styles = getSampleStyleSheet()
#     story = []

#     # Custom styles
#     styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, spaceAfter=20))
#     styles.add(ParagraphStyle(name='CustomSubtitle', parent=styles['Heading2'], fontSize=18, alignment=TA_CENTER, spaceAfter=15))
#     styles.add(ParagraphStyle(name='CustomBodyText', parent=styles['BodyText'], fontSize=12, spaceAfter=10))
#     styles.add(ParagraphStyle(name='Footer', parent=styles['BodyText'], fontSize=10, textColor=HexColor('#666666'), alignment=TA_CENTER))

#     # Title
#     story.append(Paragraph("Legal Document Analysis", styles['CustomTitle']))
#     story.append(Paragraph("Generated by Sahi Jawab", styles['CustomSubtitle']))
#     story.append(Spacer(1, 20))

#     # Add image to PDF if available
#     if image:
#         image_path = io.BytesIO()
#         image.save(image_path, format='PNG')
#         image_path.seek(0)
#         img = PDFImage(image_path, width=400, height=300)
#         story.append(img)
#         story.append(Spacer(1, 20))

#     # Content as table
#     data = [['Key', 'Value']]
#     for line in content.split('\n'):
#         if ':' in line:
#             key, value = line.split(':', 1)
#             data.append([key.strip(), value.strip()])

#     table = Table(data, colWidths=[doc.width / 2.0] * 2)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.green),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 10),
#         ('TOPPADDING', (0, 1), (-1, -1), 6),
#         ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
#     story.append(table)

#     # Footer
#     story.append(Spacer(1, 30))
#     story.append(Paragraph("Generated by Sahi Jawab | Developed by Team Sahi Jawab", styles['Footer']))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # Function to reset state
# def reset_state():
#     st.session_state.img_file_buffer = None
#     st.session_state.analysis_result = None
#     st.session_state.pdf_buffer = None

# # Image capture and analysis
# if 'img_file_buffer' not in st.session_state:
#     st.session_state.img_file_buffer = None

# col1, col2 = st.columns(2)

# with col1:
#     camera_placeholder = st.empty()
#     if st.session_state.img_file_buffer is None:
#         st.session_state.img_file_buffer = camera_placeholder.camera_input("Take a picture")

# with col2:
#     uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "jpeg", "png"])
#     if uploaded_file is not None:
#         st.session_state.img_file_buffer = uploaded_file

# if st.session_state.img_file_buffer is not None:
#     bytes_data = st.session_state.img_file_buffer.getvalue()
#     img = Image.open(io.BytesIO(bytes_data))
    
#     # Clear the camera input and file uploader
#     camera_placeholder.empty()
#     st.empty()  # This will clear the file uploader

#     col1, col2 = st.columns([1, 1])
    
#     with col2:
#         st.markdown('<div class="image-container">', unsafe_allow_html=True)
#         st.markdown('<div class="heading">Uploaded Legal Document</div>', unsafe_allow_html=True)
#         st.image(img, use_column_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col1:
#         with st.spinner("Processing image... Please wait."):
#             try:
#                 analysis_result = analyze_image(img)
                
#                 if analysis_result:
#                     if "not a legal document" in analysis_result.lower():
#                         st.warning("The uploaded document seems to have no legal information.")
#                     else:
#                         st.success("Analysis complete!")
                        
#                         # Display the analysis as a table
#                         st.markdown('<div class="document-summary">', unsafe_allow_html=True)
#                         st.markdown('<div class="heading">Key Points after Legal Analysis are:</div>', unsafe_allow_html=True)
                        
#                         table_data = []
#                         for point in analysis_result.split('\n'):
#                             if ':' in point:
#                                 key, value = point.split(':', 1)
#                                 if value.strip():  # Only add if there's a value
#                                     table_data.append([key.strip(), value.strip()])
                        
#                         if table_data:
#                             st.table(table_data)
#                         else:
#                             st.write("No specific details found in the analysis.")
                        
#                         st.markdown('</div>', unsafe_allow_html=True)
                        
#                         # Create and offer PDF download
#                         pdf_buffer = create_pdf(analysis_result, img)
#                         st.download_button(
#                             label="Download Summary as PDF",
#                             data=pdf_buffer,
#                             file_name="legal_document_summary.pdf",
#                             mime="application/pdf"
#                         )
                        
#                         # Chatbox for further questions
#                         st.subheader("Ask a question about the document")
#                         user_question = st.text_input("Enter your question here:")
#                         if user_question:
#                             with st.spinner("Generating answer..."):
#                                 question_prompt = f"Based on the following legal document summary:\n\n{analysis_result}\n\nAnswer the following question: {user_question}"
#                                 answer = process_with_groq(question_prompt)
#                                 if answer:
#                                     st.write(answer)
#                                 else:
#                                     st.error("Failed to generate an answer. Please try again.")
#                 else:
#                     st.error("Failed to analyze the image. Please try again.")
                
#                 # Add reset button
#                 if st.button("Reset and Upload New Photo"):
#                     reset_state()
#                     st.rerun()
            
#             except Exception as e:
#                 st.error(f"An error occurred during analysis: {str(e)}")
#                 st.write("Error details:", e)

# # Lottie animation for analysis
# st.lottie(lottie_analysis, height=300, key="analysis")

# # Additional information
# st.markdown("""
# ---
# ### Why Use SnapLaw?

# - **Quick Analysis**: Get instant summaries of complex legal documents
# - **Key Information Extraction**: Automatically identify crucial details like parties involved, property information, and more
# - **Time-Saving**: Skip manual review and get straight to the important parts
# - **User-Friendly**: No need for complex software or legal knowledge

# Remember, while SnapLaw provides a helpful summary, it's always recommended to consult with a legal professional for comprehensive advice.
# """)

# # Footer
# st.markdown("""
# ---
# <p style="text-align: center;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
# """, unsafe_allow_html=True)

# # Main execution
# if __name__ == "__main__":
#     # This is where your main Streamlit app execution would go
#     # However, since Streamlit runs the entire script from top to bottom,
#     # most of your app's logic is already defined above
#     pass

import streamlit as st
import os
from PIL import Image
import io
from streamlit_lottie import st_lottie
import requests
import base64
import time
from dotenv import load_dotenv
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as PDFImage, Spacer
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from annotated_text import annotated_text
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from main import add_logout_button  # Import the logout function

load_dotenv()

def show_page_name():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        st.stop()

if __name__ == "__main__":
    show_page_name()

#  Configuration with Tune.ai setup
TUNE_API_KEY = os.getenv("TUNE_API_KEY")
TUNE_API_URL = "https://proxy.tune.app/chat/completions"

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.set_page_config(page_title='SnapLaw - Sahi Jawab', layout='wide', page_icon="📸")
st.logo("logo/sidebar_logo.png", icon_image="logo/only_logo.png")

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_camera = load_lottieurl("https://lottie.host/ff051f81-13ab-42b3-b209-3cad44d690a4/UnrEKrEbeP.json")
lottie_analysis = load_lottieurl("https://lottie.host/55a9ffe1-1379-4f67-803b-736e360b2a1e/GoUsiPljIX.json")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .document-summary {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .heading {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2e7d32;
    }
    .image-container {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px;
    }
    .summary-table {
        width: 100%;
        border-collapse: collapse;
    }
    .summary-table th, .summary-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .summary-table th {
        background-color: #4CAF50;
        color: white;
    }
    .summary-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image('logo/Sahi Jawab.png', use_column_width=True, caption='Sahi Jawab : Your Nyaya Mitra 👩🏻‍⚖️📚𓍝')
    
    # About Us in an expander
    with st.expander("ℹ️ About Us", expanded=False):
        st.markdown("Welcome to SnapLaw: Instant Legal Document Analysis")
        st.success("AI-powered legal document analyzer for Indian laws.")

    # Features in an expander
    with st.expander("🚀 Features", expanded=False):
        st.markdown("- Real-time document capture\n- AI-driven analysis\n- Multi-language support")
    
    def print_praise():
        praise_quotes = """
        Team Sahi Jawab

    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes


    st.write("---")
    add_logout_button()
    st.write("---")
    st.success(print_praise())
    st.write("---")

    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/keshavagrawal595/'>Team Sahi Jawab</a></h3>",
        unsafe_allow_html=True
    )

# Main content
st.title("Welcome to SnapLaw: Instant Legal Document Analysis")

col1, col2 = st.columns([1,1])

with col1:
    st.markdown("""
    ### Capture and Analyze Legal Documents in Real-Time
    
    SnapLaw uses advanced AI to extract crucial information from your legal documents. 
    Simply capture an image, and let our system do the rest!
    
    **How it works:**
    1. Use the camera below to take a clear photo of your legal document
    2. Our AI will analyze the document and provide a summary
    """)
with col2:    
    st_lottie(lottie_camera, height=300, key="camera")

# Function to analyze image with Tune.ai
import base64

def analyze_image(image):
    try:
        # Convert PIL Image to base64
        buffered = io.BytesIO()
        image.save(buffered, format='PNG')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        headers = {
            "Authorization": f"{TUNE_API_KEY}",
            "Content-Type": "application/json",
        }
        
        prompt = '''
        Analyze the uploaded image with a focus on identifying and extracting relevant legal information. Your task is to determine if the image contains a legal document and provide a comprehensive summary of its content. Focus on the following aspects:

        - **Document Type**: Identify the type of legal document (e.g., contract, deed, affidavit, will, etc.). Avoid any placeholders like "[Insert type]".
        
        - **Parties Involved**: Extract the names and roles of all parties mentioned in the document. Do not include placeholders like "[Name X]" or "[Role X]". Only use real names and roles, or if they are not clear, state "Name not identifiable".

        - **Important Clauses**: Summarize any key clauses, terms, or conditions that are crucial to the document's purpose. Do not include text such as "[Clause X]" or similar placeholders. If a clause is unclear or unreadable, explicitly state that it could not be identified.

        - **Dates and Events**: Identify and list any important dates, events, or deadlines mentioned in the document. Do not use "[Date X]" or "[Event X]" placeholders. If no dates or events are found, say "No dates/events mentioned".

        - **Property Information**: If applicable, extract details about properties, assets, or any other relevant subject matter mentioned. Avoid placeholders such as "[Property X]". If no relevant information is found, state "No property information identified."

        - **Signatures and Witnesses**: Note the presence of any signatures, witnesses, or other markers of document authenticity. Do not use placeholders like "[Signature X]" or "[Witness X]". If signatures are not found, state "No signatures/witnesses identified."

        **Important**: Do not generate placeholders like "[Insert type]", "[Name X]", "[Clause X]", etc. If you cannot extract specific information, clearly explain why the information could not be extracted (e.g., the document is unreadable, missing, or contains no such data).

        Prioritize accuracy, relevance, and clarity in the summary to assist users in quickly understanding the core aspects of the document.
        
        Important : If the image is blurry or not completely visible then do not generate any inconsistent or dummy or wrong results. Simply say image is blurry or not clear.
        '''

        # Data to be sent in the request
        data = {
            "temperature": 0.7,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in analyzing legal documents. Provide a detailed analysis in a structured format with clear headings for each aspect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "meta/llama-3.2-90b-vision",
            "image": img_base64  # Send base64 image string
        }

        st.write("Sending image to Tune.ai API...")
        response = requests.post(TUNE_API_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            analysis_result = response.json()  # Parse the JSON response
            st.write("Received response from Tune.ai API")
            return analysis_result
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        st.error(f"Error in analyze_image function: {str(e)}")
        raise


# Function to create PDF
def create_pdf(content, image=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=30, rightMargin=30)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Title'], fontSize=24, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name='CustomSubtitle', parent=styles['Heading2'], fontSize=18, alignment=TA_CENTER, spaceAfter=15))
    styles.add(ParagraphStyle(name='CustomBodyText', parent=styles['BodyText'], fontSize=12, spaceAfter=10))
    styles.add(ParagraphStyle(name='Footer', parent=styles['BodyText'], fontSize=10, textColor=HexColor('#666666'), alignment=TA_CENTER))

    # Title
    story.append(Paragraph("Legal Document Analysis", styles['CustomTitle']))
    story.append(Paragraph("Generated by Sahi Jawab", styles['CustomSubtitle']))
    story.append(Spacer(1, 20))

    # Add image to PDF if available
    if image:
        image_path = io.BytesIO()
        image.save(image_path, format='PNG')
        image_path.seek(0)
        img = PDFImage(image_path, width=400, height=300)
        story.append(img)
        story.append(Spacer(1, 20))

    # Content as table
    data = [['Key', 'Value']]
    for line in content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            data.append([key.strip(), value.strip()])

    table = Table(data, colWidths=[doc.width / 2.0] * 2)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)

    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by Sahi Jawab | Developed by Keshav Agrawal", styles['Footer']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Function to reset state
def reset_state():
    st.session_state.img_file_buffer = None
    st.session_state.analysis_result = None
    st.session_state.pdf_buffer = None

# Image capture and analysis
if 'img_file_buffer' not in st.session_state:
    st.session_state.img_file_buffer = None

camera_placeholder = st.empty()
if st.session_state.img_file_buffer is None:
    st.session_state.img_file_buffer = camera_placeholder.camera_input("Take a picture")

# Image capture and analysis
if st.session_state.img_file_buffer is not None:
    bytes_data = st.session_state.img_file_buffer.getvalue()
    img = Image.open(io.BytesIO(bytes_data))

    # Clear the camera input and file uploader
    camera_placeholder.empty()
    st.empty()  # This will clear the file uploader
    
    col1, col2 = st.columns([1, 1])
    
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown('<div class="heading">Uploaded Legal Document</div>', unsafe_allow_html=True)
        st.image(img, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col1:
        with st.spinner("Analyzing image... Please wait."):
            try:
                analysis_result = analyze_image(img)
                
                # Extract the actual text content from the response
                if analysis_result and "choices" in analysis_result:
                    # Extract the content from the first choice
                    message_content = analysis_result["choices"][0]["message"]["content"]
                    
                    # Check if it contains "not a legal document"
                    if "not a legal document" in message_content.lower():
                        st.warning("The uploaded document seems to have no legal information.")
                    else:
                        st.success("Analysis complete!")
                    
                    # Display the analysis as a table
                    st.markdown('<div class="document-summary">', unsafe_allow_html=True)
                    st.markdown('<div class="heading">Key Points after Legal Analysis are:</div>', unsafe_allow_html=True)
                    
                    table_data = []
                    for point in message_content.split('\n'):
                        if ':' in point:
                            key, value = point.split(':', 1)
                            if value.strip():  # Only add if there's a value
                                table_data.append([key.strip(), value.strip()])
                    
                    if table_data:
                        st.table(table_data)
                    else:
                        st.write("No specific details found in the analysis.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Create and offer PDF download
                    pdf_buffer = create_pdf(message_content, img)
                    st.download_button(
                        label="Download Summary as PDF",
                        data=pdf_buffer,
                        file_name="legal_document_summary.pdf",
                        mime="application/pdf"
                    )
                        
                    # Chatbox for further questions
                    st.subheader("Ask a question about the document")
                    user_question = st.text_input("Enter your question here:")
                    if user_question:
                        with st.spinner("Generating answer..."):
                            model_google = genai.GenerativeModel('gemini-1.5-flash')
                            response = model_google.generate_content([
                                f"Based on this legal document summary: {analysis_result}\n\nAnswer the following question: {user_question}"
                            ])
                            st.write(response.text)
                    
                    # Add reset button
                    if st.button("Reset and Take New Photo"):
                        reset_state()
                        st.rerun()
            
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.write("Error details:", e)

# Lottie animation for analysis
st_lottie(lottie_analysis, height=300, key="analysis")


# Additional information
st.markdown("""
---
### Why Use SnapLaw?

- **Quick Analysis**: Get instant summaries of complex legal documents
- **Key Information Extraction**: Automatically identify crucial details like parties involved, property information, and more
- **Time-Saving**: Skip manual review and get straight to the important parts
- **User-Friendly**: No need for complex software or legal knowledge

Remember, while SnapLaw provides a helpful summary, it's always recommended to consult with a legal professional for comprehensive advice.
""")

# Footer
st.markdown("""
---
<p style="text-align: center;">© 2024 Sahi Jawab - AI Legal Advisor. All rights reserved.</p>
""", unsafe_allow_html=True)