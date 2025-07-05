from abc import ABC, abstractmethod

class BookState(ABC):
    @abstractmethod
    def borrow(self, book):
        pass
    
    @abstractmethod
    def return_book(self, book):
        pass
    
    @abstractmethod
    def reserve(self, book):
        pass

class AvailableState(BookState):
    def borrow(self, book):
        book.state = BorrowedState()
        return True
    
    def return_book(self, book):
        return False
    
    def reserve(self, book):
        book.state = ReservedState()
        return True

class BorrowedState(BookState):
    def borrow(self, book):
        return False
    
    def return_book(self, book):
        book.state = AvailableState()
        return True
    
    def reserve(self, book):
        return False

class ReservedState(BookState):
    def borrow(self, book):
        return False
    
    def return_book(self, book):
        book.state = AvailableState()
        return True
    
    def reserve(self, book):
        return False

class RestorationState(BookState):
    def borrow(self, book):
        return False
    
    def return_book(self, book):
        return False
    
    def reserve(self, book):
        return False