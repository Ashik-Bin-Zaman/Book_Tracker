import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import defaultdict

# ------------------ Book Class ------------------
class Book:
    def __init__(self, title, author=None, borrowed_from=None, borrowed_date=None, return_due_date=None, is_read=False):
        self.title = title
        self.author = author
        self.borrowed_from = borrowed_from
        self.borrowed_date = borrowed_date
        self.return_due_date = return_due_date
        self.is_read = is_read

# ------------------ Tree for Completed Books ------------------
class BookNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class CompletedBooksBST:
    def __init__(self):
        self.root = None

    def insert(self, book):
        def _insert(node, book):
            if node is None:
                return BookNode(book)
            if book.title.lower() < node.book.title.lower():
                node.left = _insert(node.left, book)
            else:
                node.right = _insert(node.right, book)
            return node
        self.root = _insert(self.root, book)

    def search(self, title):
        def _search(node, title):
            if node is None:
                return None
            if node.book.title.lower() == title.lower():
                return node.book
            elif title.lower() < node.book.title.lower():
                return _search(node.left, title)
            else:
                return _search(node.right, title)
        return _search(self.root, title)

# ------------------ Main App Class ------------------
class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Book Tracker")
        self.root.geometry("800x600")

        self.borrowed_books = []
        self.monthly_to_read = defaultdict(list)
        self.completed_tree = CompletedBooksBST()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.create_borrow_tab()
        self.create_to_read_tab()
        self.create_completed_tab()

    # -------- Borrowed Books Tab --------
    def create_borrow_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Borrowed Books')

        labels = ["Title", "Borrowed From", "Borrowed Date (YYYY-MM-DD)", "Return Due Date (YYYY-MM-DD)"]
        self.borrow_entries = []
        for i, text in enumerate(labels):
            ttk.Label(tab, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(tab, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.borrow_entries.append(entry)

        ttk.Button(tab, text="Add Book", command=self.add_borrowed_book).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Label(tab, text="Borrowed Books List", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, columnspan=2, pady=5)
        self.borrow_listbox = tk.Listbox(tab, width=80, height=10)
        self.borrow_listbox.grid(row=6, column=0, columnspan=2, padx=10)

    def add_borrowed_book(self):
        try:
            title = self.borrow_entries[0].get()
            borrowed_from = self.borrow_entries[1].get()
            bd = datetime.strptime(self.borrow_entries[2].get(), "%Y-%m-%d")
            rd = datetime.strptime(self.borrow_entries[3].get(), "%Y-%m-%d")
            book = Book(title=title, borrowed_from=borrowed_from, borrowed_date=bd, return_due_date=rd)
            self.borrowed_books.append(book)

            self.borrow_listbox.insert(tk.END, f"{title} from {borrowed_from} (Due: {rd.date()})")
            for entry in self.borrow_entries:
                entry.delete(0, tk.END)
        except:
            messagebox.showerror("Date Error", "Please enter valid dates in YYYY-MM-DD format.")

    # -------- Monthly To-Read Tab --------
    def create_to_read_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Monthly To-Read')

        ttk.Label(tab, text="Month (e.g., July 2025)").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(tab, text="Book Title").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(tab, text="Author").grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.month_entry = ttk.Entry(tab, width=30)
        self.title_entry = ttk.Entry(tab, width=30)
        self.author_entry = ttk.Entry(tab, width=30)

        self.month_entry.grid(row=0, column=1)
        self.title_entry.grid(row=1, column=1)
        self.author_entry.grid(row=2, column=1)

        ttk.Button(tab, text="Add to To-Read", command=self.add_to_read).grid(row=3, column=0, columnspan=2, pady=10)

        self.to_read_listbox = tk.Listbox(tab, width=80, height=10)
        self.to_read_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_to_read(self):
        month = self.month_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()

        if month and title:
            book = Book(title=title, author=author, is_read=False)
            self.monthly_to_read[month].append(book)
            self.to_read_listbox.insert(tk.END, f"[{month}] {title} by {author}")
            self.month_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Month and Title are required.")

    # -------- Completed Books Tab --------
    def create_completed_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Completed Books')

        ttk.Label(tab, text="Title").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(tab, text="Author").grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.completed_title_entry = ttk.Entry(tab, width=30)
        self.completed_author_entry = ttk.Entry(tab, width=30)

        self.completed_title_entry.grid(row=0, column=1)
        self.completed_author_entry.grid(row=1, column=1)

        ttk.Button(tab, text="Add Completed Book", command=self.add_completed_book).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(tab, text="Search Completed Book Title").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.search_entry = ttk.Entry(tab, width=30)
        self.search_entry.grid(row=3, column=1)

        ttk.Button(tab, text="Search", command=self.search_completed_book).grid(row=4, column=0, columnspan=2, pady=5)

        self.completed_output = tk.Text(tab, height=6, width=70)
        self.completed_output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_completed_book(self):
        title = self.completed_title_entry.get()
        author = self.completed_author_entry.get()

        if title:
            book = Book(title=title, author=author, is_read=True)
            self.completed_tree.insert(book)
            self.completed_output.insert(tk.END, f"Added: {title} by {author}\n")
            self.completed_title_entry.delete(0, tk.END)
            self.completed_author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Book title is required.")

    def search_completed_book(self):
        title = self.search_entry.get()
        book = self.completed_tree.search(title)
        self.completed_output.delete(1.0, tk.END)
        if book:
            self.completed_output.insert(tk.END, f"Found: {book.title} by {book.author}\n")
        else:
            self.completed_output.insert(tk.END, f"No book found with title '{title}'\n")

# ------------------ Main ------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = BookTrackerApp(root)
    root.mainloop()
