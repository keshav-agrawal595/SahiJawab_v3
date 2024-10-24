import pyrebase

# Firebase configuration
config = {
    "apiKey": "AIzaSyDJeOXPebd7uVOAUEI4Hn329DzvlRNULos",
    "authDomain": "chatwithlawyer.firebaseapp.com",
    "databaseURL": "https://chatwithlawyer-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "chatwithlawyer",
    "storageBucket": "chatwithlawyer.appspot.com",
    "messagingSenderId": "250950721924",
    "appId": "1:250950721924:web:e0a1a2524fe8429acffdd1"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

