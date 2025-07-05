from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fine_summary import FineSummary
from notifier import Notifier, LibrarianNotifier  # if you have observers
from fine_calculator import FineCalculator  # keep this in a separate file

# ---- Strategy Interface ----
class LendingPolicy(ABC):
    @abstractmethod
    def get_lending_days(self):
        pass

    @abstractmethod
    def can_access_restricted(self):
        pass

# ---- Concrete Policies ----
class ScholarPolicy(LendingPolicy):
    def __init__(self, role):
        self.role = role

    def get_lending_days(self):
        return 21

    def can_access_restricted(self):
        return True

class GuestPolicy(LendingPolicy):
    def __init__(self, role):
        self.role = role

    def get_lending_days(self):
        return 7

    def can_access_restricted(self):
        return False

class LibrarianPolicy(LendingPolicy):
    def __init__(self, role):
        self.role = role

    def get_lending_days(self):
        return 60

    def can_access_restricted(self):
        return True

# ---- Lending Context ----
class LendingContext:
    def __init__(self, policy: LendingPolicy):
        self.policy = policy

    def borrow_book(self, book, user):
        if getattr(book, "is_restricted", False) and not self.policy.can_access_restricted():
            print(f"❌ Access denied! {user.get_details()['Role']} can't borrow restricted book '{book.get_details()['Title']}'")
            return

        book.set_status("Borrowed")
        print(f"✅ {user.get_details()['Name']} borrowed '{book.get_details()['Title']}' for {self.policy.get_lending_days()} days.")

# ---- Return System ----
from datetime import datetime
from fine_calculator import FineCalculator
from fine_summary import FineSummary

class ReturnSystem:
    def __init__(self):
        self.borrowed_books = {}
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify_observers(self, book_title):
        for observer in self.observers:
            observer.update(book_title)

    def return_book(self, book_title):
        if book_title not in self.borrowed_books:
            return "Book not found in borrowed records."

        record = self.borrowed_books[book_title]
        due_date = datetime.strptime(record["due_date"], "%Y-%m-%d")
        now = datetime.now()
        borrower = record["borrower"]

        days_late = (now - due_date).days if now > due_date else 0
        fine = FineCalculator(borrower).calculate_fine(days_late) if days_late > 0 else 0

        summary = FineSummary(
            borrower, book_title, due_date.strftime("%Y-%m-%d"),
            now.strftime("%Y-%m-%d"), fine, days_late
        )

        self.notify_observers(book_title)
        return summary.generate_summary()
