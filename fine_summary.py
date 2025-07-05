class FineSummary:
    def __init__(self, borrower, book_title, due_date, return_date, fine_amount, days_late):
        self.borrower = borrower
        self.book_title = book_title
        self.due_date = due_date
        self.return_date = return_date
        self.fine_amount = fine_amount
        self.days_late = days_late

    def generate_summary(self):
        if self.days_late > 0:
            return (
                f"📚 Book: {self.book_title}\n"
                f"👤 Borrower: {self.borrower}\n"
                f"📅 Due Date: {self.due_date}\n"
                f"📅 Returned On: {self.return_date}\n"
                f"⚠️ Late by {self.days_late} days\n"
                f"💰 Fine: ₹{self.fine_amount}"
            )
        else:
            return (
                f"📚 Book: {self.book_title}\n"
                f"👤 Borrower: {self.borrower}\n"
                f"✅ Returned on time. No fine!"
            )
