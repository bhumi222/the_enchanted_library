from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    """Abstract base class for all observers in the library system."""
    
    @abstractmethod
    def update(self, message: str) -> None:
        """Update method that must be implemented by concrete observers.
        
        Args:
            message: The notification message to be handled
        """
        pass


class Subject(ABC):
    """Abstract base class for all subjects that can notify observers."""
    
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer to this subject.
        
        Args:
            observer: The observer to be attached
        """
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from this subject.
        
        Args:
            observer: The observer to be removed
        """
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        """Notify all attached observers with a message.
        
        Args:
            message: The message to be sent to all observers
        """
        for observer in self._observers:
            observer.update(message)


class LibraryNotifier(Subject):
    """Handles library-wide notifications to different types of users."""
    
    def __init__(self):
        super().__init__()
        self.notifications = []
    
    def send_notification(self, message: str) -> None:
        """Send a notification to all observers and store it in history.
        
        Args:
            message: The notification message to be sent
        """
        self.notifications.append({
            'message': message,
            'timestamp': datetime.now()
        })
        self.notify(message)


class LibrarianObserver(Observer):
    """Observer for librarian users, handles staff-specific notifications."""
    
    def __init__(self, username: str):
        self.username = username
    
    def update(self, message: str) -> None:
        """Handle librarian-specific notifications.
        
        Args:
            message: The notification message for the librarian
        """
        print(f"Notification for {self.username}: {message}")


class OverdueNotifier(Subject):
    """Handles notifications for overdue books."""
    
    def check_overdue_books(self, books: list) -> None:
        """Check for overdue books and notify observers.
        
        Args:
            books: List of books to check for overdue status
        """
        current_date = datetime.now()
        for book in books:
            if book.due_date and book.due_date < current_date:
                self.notify(f"Book '{book.title}' is overdue!")


class GuestObserver(Observer):
    """Observer for guest users, handles guest-specific notifications."""
    
    def __init__(self, username: str):
        self.username = username
    
    def update(self, message: str) -> None:
        """Handle guest-specific notifications.
        
        Args:
            message: The notification message for the guest
        """
        print(f"Guest Notification for {self.username}: {message}")