

from abc import ABC, abstractmethod

# Receiver
class Book:
    def __init__(self, title):
        self.title = title
        self.status = "Available"

    def borrow(self):
        if self.status == "Available":
            self.status = "Borrowed"
            print(f"'{self.title}' has been borrowed.")
        else:
            print(f"'{self.title}' cannot be borrowed. Current status: {self.status}")

    def return_book(self):
        if self.status == "Borrowed":
            self.status = "Available"
            print(f"'{self.title}' has been returned.")
        else:
            print(f"'{self.title}' cannot be returned. Current status: {self.status}")

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Concrete Commands
class BorrowBookCommand(Command):
    def __init__(self, book):
        self.book = book

    def execute(self):
        self.book.borrow()

    def undo(self):
        self.book.return_book()

class ReturnBookCommand(Command):
    def __init__(self, book):
        self.book = book

    def execute(self):
        self.book.return_book()

    def undo(self):
        self.book.borrow()

# Invoker
class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if self.history:
            last_command = self.history.pop()
            last_command.undo()
        else:
            print("Nothing to undo.")
