from abc import ABC, abstractmethod

class Book(ABC):
    def __init__(self, title, author, isbn, condition="Good"):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._condition = condition
        self._status = "Available"  # For state pattern

    @abstractmethod
    def get_book_type(self):
        pass

    def get_details(self):
        return {
            "Title": self._title,
            "Author": self._author,
            "ISBN": self._isbn,
            "Condition": self._condition,
            "Status": self._status
        }

    def set_status(self, status):
        self._status = status

    def get_status(self):
        return self._status


class AncientScript(Book):
    def get_book_type(self):
        return "Ancient Script"

class RareBook(Book):
    def get_book_type(self):
        return "Rare Book"

class GeneralBook(Book):
    def get_book_type(self):
        return "General Book"
class AncientScript(Book):
    def __init__(self, title, author, isbn, condition="Good"):
        super().__init__(title, author, isbn, condition)
        self.is_restricted = True

    def get_book_type(self):
        return "Ancient Script"
