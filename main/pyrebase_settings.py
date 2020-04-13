import pyrebase
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = {
    'apiKey': "",
    'authDomain': "",
    'databaseURL': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': ""}
    
 
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
#p = os.path.join(BASE_DIR,'NoteBook/media/profile_image/NPTEL19CS40S11150162191129702_j7gs5aX.jpg')
#print(p)
#storage.child('images/a.jpg').put(p)
