import firebase_admin
from firebase_admin import db, credentials, storage

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
        users = self.get_users()
        users_name = []
        for _, user_info in users.items():
            if isinstance(user_info, dict) and "name" in user_info:
                users_name.append(user_info["name"])
        return users_name
    
    def get_pub_key(self, user_name):
        users = self.get_users()
        for _, user_info in users.items():
            if user_info["name"] == user_name:
                return user_info["pub_key"]
        return None
    
    def get_conversations(self):
        return self.ref.child("conversations").get()

    # Setters
    def set_conversations(self, conversations):
        self.ref.child("conversations").set(conversations)

    def set_users(self, users):
        self.ref.child("users").set(users)

    def add_message(self, from_user, to_user, message, encryptedBy):
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
            "message": message,
            "encryptedBy": encryptedBy
        })
    
    def update_user_pub_key(self, user_name, new_pub_key):
        users = self.get_users()
        for user_id, user_info in users.items():
            if user_info["name"] == user_name:
                self.ref.child(f"users/{user_id}").update({"pub_key": new_pub_key})
                break