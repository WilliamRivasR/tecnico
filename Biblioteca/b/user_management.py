# user_management.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database import DatabaseConnection

class UserManagementFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.db = DatabaseConnection()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.update_frame = ttk.Frame(self.notebook)
        self.delete_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.update_frame, text="Update User")
        self.notebook.add(self.delete_frame, text="Delete User")

        self.create_update_widgets()
        self.create_delete_widgets()

    def create_update_widgets(self):
        fields = [
            ("Document Number", ttk.Entry(self.update_frame)),
            ("Name", ttk.Entry(self.update_frame)),
            ("Surname", ttk.Entry(self.update_frame)),
            ("Birth Date", DateEntry(self.update_frame, date_pattern='yyyy-mm-dd')),
            ("Email", ttk.Entry(self.update_frame)),
            ("Phone", ttk.Entry(self.update_frame)),
            ("Password", ttk.Entry(self.update_frame, show="*"))
        ]

        for i, (text, entry) in enumerate(fields):
            ttk.Label(self.update_frame, text=text).grid(column=0, row=i, sticky=tk.W, pady=5)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
            setattr(self, f"update_{text.lower().replace(' ', '_')}", entry)

        ttk.Button(self.update_frame, text="Update User", command=self.update_user).grid(column=0, row=len(fields), columnspan=2, pady=20)

        self.update_message = ttk.Label(self.update_frame, text="")
        self.update_message.grid(column=0, row=len(fields)+1, columnspan=2, pady=10)

    def create_delete_widgets(self):
        ttk.Label(self.delete_frame, text="Document Number:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.delete_document_number = ttk.Entry(self.delete_frame)
        self.delete_document_number.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.delete_frame, text="Delete User", command=self.delete_user).grid(column=0, row=1, columnspan=2, pady=20)

        self.delete_message = ttk.Label(self.delete_frame, text="")
        self.delete_message.grid(column=0, row=2, columnspan=2, pady=10)

    def update_user(self):
        values = [getattr(self, f"update_{field.lower().replace(' ', '_')}").get() for field, _ in self.fields]
        cursor = self.db.call_procedure('ActualizarUsuario', values)
        self.update_message.config(text="User updated successfully!")

    def delete_user(self):
        document_number = self.delete_document_number.get()
        cursor = self.db.call_procedure('BorrarUsuario', [document_number])
        self.delete_message.config(text="User deleted successfully!")