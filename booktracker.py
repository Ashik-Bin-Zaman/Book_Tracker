import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Book class for borrowed books
class Book:
    def __init__(self, title, borrowed_from, borrowed_date, return_due_date):
        self.title = title
        self.borrowed_from = borrowed_from
        self.borrowed_date = borrowed_date
        self.return_due_date = return_due_date

# Borrowed Book Tracker UI
class BorrowedBookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("📕 Borrowed Books Tracker")
        self.root.geometry("500x400")
        self.root.configure(bg="white")

        self.borrowed_books = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Title:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(self.root, text="Borrowed From:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(self.root, text="Borrowed Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Label(self.root, text="Return Due Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.entry_title = tk.Entry(self.root, width=30)
        self.entry_from = tk.Entry(self.root, width=30)
        self.entry_borrowed = tk.Entry(self.root, width=30)
        self.entry_due = tk.Entry(self.root, width=30)

        self.entry_title.grid(row=0, column=1, pady=5)
        self.entry_from.grid(row=1, column=1, pady=5)
        self.entry_borrowed.grid(row=2, column=1, pady=5)
        self.entry_due.grid(row=3, column=1, pady=5)

        tk.Button(self.root, text="➕ Add Borrowed Book", command=self.add_borrowed_book).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="📚 Borrowed Books List:", font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, pady=5)

        self.listbox = tk.Listbox(self.root, width=60, height=10)
        self.listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def add_borrowed_book(self):
        title = self.entry_title.get()
        borrowed_from = self.entry_from.get()
        borrowed_date = self.entry_borrowed.get()
        return_due = self.entry_due.get()

        try:
            bd = datetime.strptime(borrowed_date, "%Y-%m-%d")
            rd = datetime.strptime(return_due, "%Y-%m-%d")
            book = Book(title, borrowed_from, bd, rd)
            self.borrowed_books.append(book)

            self.listbox.insert(tk.END, f"{title} from {borrowed_from} (Return by {rd.date()})")
            self.clear_entries()
        except:
            messagebox.showerror("Error", "Please enter valid dates in YYYY-MM-DD format.")

    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_from.delete(0, tk.END)
        self.entry_borrowed.delete(0, tk.END)
        self.entry_due.delete(0, tk.END)

# Run this section only
if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowedBookTracker(root)
    root.mainloop()
