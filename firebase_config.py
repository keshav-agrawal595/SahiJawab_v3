import firebase_admin
from firebase_admin import credentials, firestore

# Check if Firebase has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('ai-legal-advisor-ad193-firebase-adminsdk-ai0xk-68de16c867.json')

    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_chat_history(session_name, messages):
    try:
        db.collection('chat_histories').document(session_name).set({
            'messages': messages
        })
        print(f"Chat history for session '{session_name}' has been saved.")
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")

def get_chat_history(session_name):
    try:
        doc = db.collection('chat_histories').document(session_name).get()
        if doc.exists:
            return doc.to_dict().get('messages', [])
        else:
            return []
    except Exception as e:
        print(f"Error retrieving chat history: {str(e)}")
        return []

