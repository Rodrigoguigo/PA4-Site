import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class DbBasic:

    def __init__(self):
        self.__cred = credentials.Certificate('/home/gutao/Desktop/com-pizza-firebase-adminsdk-9sili-dc12299921.json')
        self.__default_app = firebase_admin.initialize_app(self.__cred, {
        'databaseURL': 'https://com-pizza.firebaseio.com/'
        })
        self.ref= db.reference()
