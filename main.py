import tkinter as tk
from tkinter import ttk
import bdd
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class MessagingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Messagerie")
        self.geometry("1000x800")
        self.configure(bg="#e0e0e0")

        bdd_projet = bdd.BaseDeDonnees()

        self.users = bdd_projet.get_users_name()
        
        self.conversations = bdd_projet.get_conversations()
        
        # Génération de la paire de clés RSA
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

        self.is_typing = False
        self.current_user = None
        self.current_conversation = None
        print(f"Utilisateur actuel: {self.current_user}")

        self.create_widgets()

    def create_widgets(self):
        # Menu déroulant pour sélectionner l'utilisateur
        self.user_selection = ttk.Combobox(self, values=self.users, state="readonly")
        self.user_selection.bind("<<ComboboxSelected>>", self.on_user_select)
        self.user_selection.place(relx=0.35, rely=0.02, relwidth=0.3)

        # Frame pour la liste des conversations
        self.conversations_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.conversations_frame.place(relx=0, rely=0.05, relwidth=0.3, relheight=0.95)

        # Liste des conversations
        self.conversations_listbox = tk.Listbox(self.conversations_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.conversations_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.conversations_listbox.bind("<<ListboxSelect>>", self.on_conversation_select)

        # Frame pour les messages
        self.messages_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.messages_frame.place(relx=0.3, rely=0.05, relwidth=0.7, relheight=0.75)

        # Zone d'affichage des messages
        self.messages_text = tk.Text(self.messages_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12), state=tk.DISABLED)
        self.messages_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pour la saisie de message
        self.entry_frame = tk.Frame(self, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.entry_frame.place(relx=0.3, rely=0.8, relwidth=0.7, relheight=0.15)

        # Champ de saisie de message
        self.message_entry = tk.Entry(self.entry_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.message_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.message_entry.bind("<Key>", self.on_typing)

        # Bouton d'envoi
        self.send_button = tk.Button(self.entry_frame, text="Envoyer", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12), command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Afficher les conversations de l'utilisateur actuel
        self.update_conversations_list()

    def on_user_select(self, event):
        self.current_user = self.user_selection.get()
        self.current_conversation = None
        print(f"Utilisateur sélectionné: {self.current_user}")
        self.update_conversations_list()

    def update_conversations_list(self):
        self.conversations_listbox.delete(0, tk.END)
        if self.current_user == None:
            return
        for user in self.users:
            if user != self.current_user:
                self.conversations_listbox.insert(tk.END, user)
        if self.conversations_listbox.size() > 0:
            self.conversations_listbox.select_set(0)
            self.current_conversation = self.conversations_listbox.get(0)
            print(f"Conversation ajoutée: {user}")
            self.display_conversation(self.conversations_listbox.get(0))
        print(f"Conversation actuelle affichée: {self.conversations_listbox.get(0)}")

    def on_conversation_select(self, event):
        if self.is_typing:
            return
        selected_conversation = self.conversations_listbox.get(self.conversations_listbox.curselection())
        print(f"Conversation sélectionnée: {selected_conversation}")
        self.current_conversation = selected_conversation
        self.display_conversation(selected_conversation)

    def display_conversation(self, conversation):
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.delete(1.0, tk.END)
        for message in self.conversations:
            if message["from"] == self.current_user and message["to"] == conversation:
                self.messages_text.insert(tk.END, f"Vous: {message['message']}\n")
            elif message["from"] == conversation and message["to"] == self.current_user:
                self.messages_text.insert(tk.END, f"{conversation}: {message['message']}\n")

    def on_typing(self, event):
        self.is_typing = True

    def send_message(self):
        message = self.message_entry.get()
        if message:
            if self.current_conversation:
                # Mettre à jour l'affichage
                # Chiffrer message
                encrypted_message = self.encrypt_message(message)

                # Ajouter le message dans la bdd
                bdd_projet = bdd.BaseDeDonnees()                
                bdd_projet.add_message(self.current_user, self.current_conversation, encrypted_message)

                # Déchiffrer message
                decrypted_message = self.decrypt_message(encrypted_message)
                
                # Afficher message dans zone de texte
                self.messages_text.config(state=tk.NORMAL)
                self.messages_text.insert(tk.END, f"Vous: {encrypted_message}\n")
                self.messages_text.insert(tk.END, f"Vous: {decrypted_message}\n")
                self.messages_text.config(state=tk.DISABLED)
                
                # Effacer champ de saisie
                self.message_entry.delete(0, tk.END)
                self.is_typing = False



    # Chiffrement de message
    def encrypt_message(self, message):
        encrypted_message = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_message).decode('utf-8')
    
    # Déchiffrement de message
    def decrypt_message(self, message):
        encrypted_message = base64.b64decode(message)
        decrypted_message = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode('utf-8')



if __name__ == "__main__":
    app = MessagingApp()
    app.mainloop()