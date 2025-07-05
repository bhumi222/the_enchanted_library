from abc import ABC, abstractmethod

# Observer interface
class Notifier(ABC):
    @abstractmethod
    def update(self, book_title):
        pass

# Concrete observer
class LibrarianNotifier(Notifier):
    def update(self, book_title):
        print(f"🔔 Notification: Book '{book_title}' was returned and may need review or restoration.")
