
import customtkinter as ctk
from lending import LendingPolicy

class BorrowBookWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Borrow Book")
        self.geometry("400x300")
        self.role = ctk.StringVar(value="scholar")

        ctk.CTkLabel(self, text="Select Role:").pack(pady=5)
        ctk.CTkOptionMenu(self, variable=self.role, values=["guest", "scholar", "librarian"]).pack()

        ctk.CTkLabel(self, text="Book Title:").pack(pady=5)
        self.book_title_entry = ctk.CTkEntry(self)
        self.book_title_entry.pack()

        ctk.CTkLabel(self, text="Book Type:").pack(pady=5)
        self.book_type = ctk.StringVar(value="GeneralBook")
        ctk.CTkOptionMenu(self, variable=self.book_type, values=["GeneralBook", "RareBook", "AncientScript"]).pack()

        ctk.CTkButton(self, text="Borrow Book", command=self.borrow_book).pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def borrow_book(self):
        role = self.role.get()
        title = self.book_title_entry.get()
        book_type = self.book_type.get()

        policy = LendingPolicy(role)
        result = policy.borrow_book(title, book_type)
        self.result_label.configure(text=result)

if __name__ == "__main__":
    app = BorrowBookWindow()
    app.mainloop()
