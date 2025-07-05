
import customtkinter as ctk
from lending import ReturnSystem
from datetime import datetime, timedelta

# Dummy borrowed_books dict (in real case, connect with database or persistent file)
borrowed_books = {
    "Mystic Scroll": {
        "due_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "borrower": "scholar"
    },
    "General Knowledge": {
        "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "borrower": "guest"
    }
}

class ReturnBookWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Return Book")
        self.geometry("400x250")

        ctk.CTkLabel(self, text="Enter Book Title to Return:").pack(pady=10)
        self.book_title_entry = ctk.CTkEntry(self)
        self.book_title_entry.pack()

        ctk.CTkButton(self, text="Return Book", command=self.return_book).pack(pady=20)
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def return_book(self):
        book_title = self.book_title_entry.get()
        system = ReturnSystem(borrowed_books)
        result = system.return_book(book_title)
        self.result_label.configure(text=result)

if __name__ == "__main__":
    app = ReturnBookWindow()
    app.mainloop()
