import firebase_admin
from firebase_admin import db, credentials

class BaseDeDonnees:
    _firebase_initialized = False

    def __init__(self):
        if not BaseDeDonnees._firebase_initialized:
            cred = credentials.Certificate("credentials.json")
            firebase_admin.initialize_app(cred, {"databaseURL": "https://projet-securite-info-default-rtdb.firebaseio.com/"})
            BaseDeDonnees._firebase_initialized = True
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

    def add_message(self, from_user, to_user, message):
        # Lire et incrémenter le compteur
        counter_ref = self.ref.child("message_count")
        current_count = counter_ref.get() or 0
        new_count = current_count + 1

        # Mettre à jour le compteur
        counter_ref.set(new_count)

        # Ajouter le message
        message_ref = self.ref.child("conversations").child(str(new_count))
        message_ref.set({
            "from": from_user,
            "to": to_user,
            "message": message
        })
