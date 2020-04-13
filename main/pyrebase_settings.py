import pyrebase
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = {
    'apiKey': "AIzaSyCTGc0x8acUhHq5iM3bNI2GYbQYal4czps",
    'authDomain': "notebook-aca9b.firebaseapp.com",
    'databaseURL': "https://notebook-aca9b.firebaseio.com",
    'projectId': "notebook-aca9b",
    'storageBucket': "notebook-aca9b.appspot.com",
    'messagingSenderId': "634156586246",
    'appId': "1:634156586246:web:0e5ce1b8f72928d6d0fa87",
    'measurementId': "G-RLR7491Z7P"}
    
 
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
p = os.path.join(BASE_DIR,'NoteBook/media/profile_image/NPTEL19CS40S11150162191129702_j7gs5aX.jpg')
print(p)
storage.child('images/a.jpg').put(p)