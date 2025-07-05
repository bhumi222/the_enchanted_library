from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class LendingStrategy(ABC):
    @abstractmethod
    def calculate_due_date(self, borrow_date):
        pass
    
    @abstractmethod
    def can_borrow(self, user, book):
        pass

class AcademicLendingStrategy(LendingStrategy):
    def calculate_due_date(self, borrow_date):
        return borrow_date + timedelta(days=30)  # 30 days for academic users
    
    def can_borrow(self, user, book):
        return user.role in ["Scholar", "Admin", "Librarian"]

class PublicLendingStrategy(LendingStrategy):
    def calculate_due_date(self, borrow_date):
        return borrow_date + timedelta(days=14)  # 14 days for public users
    
    def can_borrow(self, user, book):
        return not book.is_restricted

class RestrictedLendingStrategy(LendingStrategy):
    def calculate_due_date(self, borrow_date):
        return borrow_date + timedelta(days=7)  # 7 days for restricted books
    
    def can_borrow(self, user, book):
        return user.can_access_restricted