# main.py
import tkinter as tk
from tkinter import ttk
from login import LoginFrame
from registration import RegistrationFrame
from user_management import UserManagementFrame
from book_management import BookManagementFrame
from loan_management import LoanManagementFrame

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Biblioteca Escolar")
        self.geometry("1200x700")
        self.configure(bg="#f0f0f0")

        self.create_frames()
        self.create_menu()

        self.show_frame("login")

    def create_frames(self):
        self.frames = {}
        for F in (LoginFrame, RegistrationFrame, UserManagementFrame, BookManagementFrame, LoanManagementFrame):
            frame = F(self)
            self.frames[F.__name__.lower()] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def logout(self):
        self.show_frame("login")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()