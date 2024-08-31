import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import DatabaseConnection

class LoanManagementFrame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.frame, text="Loan Management", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Loan Book Section
        loan_frame = tk.LabelFrame(self.frame, text="Loan a Book")
        loan_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(loan_frame, text="Book ID:").pack()
        self.book_id_entry = tk.Entry(loan_frame)
        self.book_id_entry.pack(pady=5)

        tk.Label(loan_frame, text="Loan Date:").pack()
        self.loan_date_entry = DateEntry(loan_frame, date_pattern='yyyy-mm-dd')
        self.loan_date_entry.pack(pady=5)

        tk.Button(loan_frame, text="Loan Book", command=self.loan_book).pack(pady=10)

        # Show Loans Section
        tk.Button(self.frame, text="Show All Loans", command=self.show_loans).pack(pady=10)

        # Treeview for displaying loans
        self.tree = ttk.Treeview(self.frame, columns=("Loan ID", "Book Name", "User ID", "Loan Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Return Book Section
        return_frame = tk.LabelFrame(self.frame, text="Return a Book")
        return_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(return_frame, text="Loan ID:").pack()
        self.return_loan_id_entry = tk.Entry(return_frame)
        self.return_loan_id_entry.pack(pady=5)

        tk.Button(return_frame, text="Return Book", command=self.return_book).pack(pady=10)

    def loan_book(self):
        book_id = self.book_id_entry.get()
        loan_date = self.loan_date_entry.get()
        user_id = "current_user_id"  # This should be obtained from the current logged-in user

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            try:
                cursor.callproc('AgregarLibroPrestado', [user_id, book_id, loan_date])
                connection.commit()
                messagebox.showinfo("Success", "Book loaned successfully!")
                self.book_id_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to loan book: {str(e)}")

    def show_loans(self):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT p.ID_prestamo, l.Titulo, p.Numero_documento, p.Fecha_prestamo FROM prestamos p JOIN libros l ON p.ID_libro = l.ID_libro")
                loans = cursor.fetchall()
                self.tree.delete(*self.tree.get_children())
                for loan in loans:
                    self.tree.insert("", "end", values=loan)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch loans: {str(e)}")

    def return_book(self):
        loan_id = self.return_loan_id_entry.get()

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM prestamos WHERE ID_prestamo = %s", (loan_id,))
                connection.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
                self.return_loan_id_entry.delete(0, tk.END)
                self.show_loans()  # Refresh the loans list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def pack(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()