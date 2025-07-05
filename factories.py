from abc import ABC, abstractmethod
from datetime import datetime

# Abstract Factory Interface
class LibraryFactory(ABC):
    @abstractmethod
    def create_book(self, title, author, book_type):
        pass
    
    @abstractmethod
    def create_user(self, username, role):
        pass

# Concrete Factory
class EnchantedLibraryFactory(LibraryFactory):
    def create_book(self, title, author, book_type):
        if book_type.lower() == "ancientscript":
            return AncientScript(title, author)
        elif book_type.lower() == "rarebook":
            return RareBook(title, author)
        else:
            return GeneralBook(title, author)
    
    def create_user(self, username, role):
        if role.lower() == "admin":
            return AdminUser(username)
        elif role.lower() == "librarian":
            return LibrarianUser(username)
        elif role.lower() == "scholar":
            return ScholarUser(username)
        else:
            return GuestUser(username)

# Book Classes
class Book(ABC):
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.status = "Available"
        self.created_at = datetime.now()

class AncientScript(Book):
    def __init__(self, title, author):
        super().__init__(title, author)
        self.is_restricted = True
        self.requires_special_handling = True

class RareBook(Book):
    def __init__(self, title, author):
        super().__init__(title, author)
        self.is_restricted = True
        self.requires_preservation = True

class GeneralBook(Book):
    def __init__(self, title, author):
        super().__init__(title, author)
        self.is_restricted = False

# User Classes
class User(ABC):
    def __init__(self, username):
        self.username = username
        self.created_at = datetime.now()

class AdminUser(User):
    def __init__(self, username):
        super().__init__(username)
        self.role = "Admin"
        self.can_access_restricted = True
        self.can_manage_users = True

class LibrarianUser(User):
    def __init__(self, username):
        super().__init__(username)
        self.role = "Librarian"
        self.can_access_restricted = True
        self.can_manage_books = True

class ScholarUser(User):
    def __init__(self, username):
        super().__init__(username)
        self.role = "Scholar"
        self.can_access_restricted = True

class GuestUser(User):
    def __init__(self, username):
        super().__init__(username)
        self.role = "Guest"
        self.can_access_restricted = False