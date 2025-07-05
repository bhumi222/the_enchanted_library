from abc import ABC, abstractmethod

# --- State Interface and Concrete States ---

class BookState(ABC):
    @abstractmethod
    def handle(self, book):
        pass

class AvailableState(BookState):
    def handle(self, book):
        print(f"'{book.title}' is now Available.")
        book.status = "Available"

class BorrowedState(BookState):
    def handle(self, book):
        print(f"'{book.title}' has been Borrowed.")
        book.status = "Borrowed"

class ReservedState(BookState):
    def handle(self, book):
        print(f"'{book.title}' is Reserved.")
        book.status = "Reserved"

class RestorationNeededState(BookState):
    def handle(self, book):
        print(f"'{book.title}' needs Restoration.")
        book.status = "Restoration Needed"

# --- Book Class using State ---

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.state = AvailableState()
        self.status = "Available"

    def set_state(self, state):
        self.state = state
        self.state.handle(self)

    def get_status(self):
        return self.status
