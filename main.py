import tkinter as tk
from tkinter import ttk

class MessagingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Messagerie")
        self.geometry("1000x800")
        self.configure(bg="#e0e0e0")

        self.users = ["Alice", "Bob", "Charlie"]
        self.conversations = {
            "Alice": ["Alice: Salut, comment ça va?", "Vous: Ça va bien, merci! Et toi?", "Alice: Je vais bien aussi, merci!"],
            "Bob": ["Bob: Hey, tu es là?", "Vous: Oui, je suis là!"],
            "Charlie": ["Charlie: Bonjour!", "Vous: Salut Charlie!"]
        }

        self.is_typing = False
        self.current_user = self.users[0]
        self.current_conversation = self.current_user
        print(f"Utilisateur actuel: {self.current_user}")

        self.create_widgets()

    def create_widgets(self):
        # Menu déroulant pour sélectionner l'utilisateur
        self.user_selection = ttk.Combobox(self, values=self.users, state="readonly")
        self.user_selection.current(0)
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
        self.current_conversation = self.current_user
        print(f"Utilisateur sélectionné: {self.current_user}")
        self.update_conversations_list()

    def update_conversations_list(self):
        self.conversations_listbox.delete(0, tk.END)
        for user in self.users:
            if user != self.current_user:
                self.conversations_listbox.insert(tk.END, user)
                self.conversations_listbox.select_set(0)
                self.display_conversation(self.conversations_listbox.get(0))


    def on_conversation_select(self, event):
        if self.is_typing:
            return
        selected_conversation = self.conversations_listbox.get(self.conversations_listbox.curselection())
        self.current_conversation = selected_conversation
        self.display_conversation(selected_conversation)

    def display_conversation(self, conversation):
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.delete(1.0, tk.END)
        for message in self.conversations[conversation]:
            self.messages_text.insert(tk.END, f"{message}\n")
        self.messages_text.config(state=tk.DISABLED)

    def on_typing(self, event):
        self.is_typing = True

    def send_message(self):
        message = self.message_entry.get()
        if message:
            if self.current_conversation:
                self.conversations[self.current_conversation].append(f"Vous: {message}")
                print(f"Message envoyé à {self.current_conversation}")
                self.messages_text.config(state=tk.NORMAL)
                self.messages_text.insert(tk.END, f"Vous: {message}\n")
                self.messages_text.config(state=tk.DISABLED)
                self.message_entry.delete(0, tk.END)
                self.is_typing = False


if __name__ == "__main__":
    app = MessagingApp()
    app.mainloop()