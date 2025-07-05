
from abc import ABC, abstractmethod

class ReservationCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class BookReservation:
    def __init__(self, book_title):
        self.book_title = book_title
        self.reserved_by = []

    def reserve(self, user_name):
        if user_name not in self.reserved_by:
            self.reserved_by.append(user_name)
            print(f"✅ Book '{self.book_title}' reserved by {user_name}")
        else:
            print(f"⚠️ {user_name} has already reserved the book '{self.book_title}'")


class ReserveBookCommand(ReservationCommand):
    def __init__(self, reservation_system, user_name):
        self.reservation_system = reservation_system
        self.user_name = user_name

    def execute(self):
        self.reservation_system.reserve(self.user_name)


class ReservationInvoker:
    def __init__(self):
        self.commands = []

    def add_reservation(self, command: ReservationCommand):
        self.commands.append(command)
        command.execute()
