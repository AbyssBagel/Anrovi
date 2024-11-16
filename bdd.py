import firebase_admin
from firebase_admin import db, credentials

class BaseDeDonnees:
    # Constructeur
    def __init__(self):
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://projet-securite-info-default-rtdb.firebaseio.com/"})
        self.ref = db.reference("/")

    # Getters
    def get_users(self):
        return self.ref.child("users").get()
    
    def get_users_name(self):
        users_name = []
        for user in self.get_users():
            users_name.append(user["name"])
        return users_name
    
    def get_conversations(self):
        return self.ref.child("conversations").get()

    # Setters
    def set_conversations(self, conversations):
        self.ref.child("conversations").set(conversations)

    def set_users(self, users):
        self.ref.child("users").set(users)