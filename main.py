# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Book management
from book import AncientScript, RareBook, GeneralBook
from catalog import Catalog

# User and roles
from user import UserFactory, User
from lending import ScholarPolicy, GuestPolicy, LibrarianPolicy, LendingContext, ReturnSystem
from notifier import LibrarianNotifier

# Role Verification
from verification_system import VerificationSystem

# State, Command, Observer Patterns
from book_state import Book as StateBook, BorrowedState, RestorationNeededState, AvailableState
from command_pattern import Book as CmdBook, BorrowBookCommand, ReturnBookCommand, CommandInvoker
from observer_pattern import Librarian as ObserverLibrarian, BookMonitor

# Access Control, Fees, Condition
from role_verifier import verify_scholar_role, verify_guest_role, verify_librarian_role
from access_control import AccessControl, Role
from late_fee_calculator import LateFeeCalculator
from book_condition_checker import BookConditionChecker

# Book Recommendation
from book_recommender import BookRecommender

def main():
    # --- Book Catalog ---
    book1 = AncientScript("Scroll of Wisdom", "Elder Kai", "111-111", "Fragile")
    book2 = RareBook("Cursed Chronicles", "Morgana", "222-222")
    book3 = GeneralBook("Python for Beginners", "Guido", "333-333")

    library_catalog = Catalog.get_instance()
    for book in [book1, book2, book3]:
        library_catalog.add_book(book)

    print("\n📚 All Books in Library:")
    library_catalog.list_books()

    # --- Users ---
    librarian = UserFactory.create_user("Librarian", "Arya", "L001")
    scholar = UserFactory.create_user("Scholar", "Zane", "S001")
    guest = UserFactory.create_user("Guest", "Nora", "G001")

    print("\n🙋‍♀️ Users:")
    for user in [librarian, scholar, guest]:
        print(user.get_details())

    # --- Borrowing ---
    print("\n📖 Borrowing Attempts:")
    scholar_context = LendingContext(ScholarPolicy("scholar"))
    guest_context = LendingContext(GuestPolicy("guest"))
    librarian_context = LendingContext(LibrarianPolicy("librarian"))

    scholar_context.borrow_book(book1, scholar)      
    guest_context.borrow_book(book1, guest)          
    librarian_context.borrow_book(book2, librarian)  
    guest_context.borrow_book(book3, guest)          

    print("\n📚 Updated Book Status:")
    library_catalog.list_books()

    # --- Return System ---
    rs = ReturnSystem()
    notifier = LibrarianNotifier()
    rs.attach(notifier)

    rs.borrowed_books = {
        "Spellbound": {
            "due_date": "2024-04-01",
            "borrower": "scholar"
        }
    }
    print(rs.return_book("Spellbound"))

    # --- Observer Demo ---
    monitor = BookMonitor()
    l1 = ObserverLibrarian("Elara")
    l2 = ObserverLibrarian("Theron")
    monitor.add_observer(l1)
    monitor.add_observer(l2)
    monitor.book_overdue("Secrets of Eldoria")
    monitor.needs_restoration("Ancient Flames")

    # --- Command Demo ---
    cmd_book = CmdBook("Secrets of Eldoria")
    invoker = CommandInvoker()
    invoker.execute_command(BorrowBookCommand(cmd_book))
    invoker.execute_command(ReturnBookCommand(cmd_book))
    invoker.undo_last()
    invoker.undo_last()

    # --- Book Condition Check ---
    damaged_book = {
        "title": "Ancient Scroll of Time",
        "book_id": "B101",
        "condition": "Damaged"
    }
    BookConditionChecker().check_condition(damaged_book)

    # --- Late Fee ---
    fee_calc = LateFeeCalculator("Scholar", "RareBook", "2025-03-01", "2025-03-20")
    print(f"\n📚 Late fee: ₹{fee_calc.calculate_fee()}")

    # --- Book Recommendation ---
    all_books = [
        {"title": "Secrets of Quantum Realm", "tags": ["physics", "science", "quantum"]},
        {"title": "History of Ancient India", "tags": ["history", "ancient", "india"]},
        {"title": "Advanced Astrophysics", "tags": ["space", "science", "astrophysics"]},
        {"title": "Ancient Greek Scrolls", "tags": ["history", "mythology", "ancient"]},
        {"title": "Mysteries of the Mind", "tags": ["psychology", "mind", "philosophy"]},
    ]

    reading_history = [{"title": "Secrets of Quantum Realm", "tags": ["physics", "science", "quantum"]}]
    interest = "space"

    recommender = BookRecommender(all_books)
    suggestions = recommender.recommend_books(reading_history, interest)

    print("\n📚 Recommended Books:")
    for book in suggestions:
        print(f"• {book['title']}")

if __name__ == "__main__":
    main()


from lending import ReturnSystem
from notifier import LibrarianNotifier

rs = ReturnSystem()
librarian = LibrarianNotifier()
rs.attach(librarian)

rs.borrowed_books = {
    "The Lost Grimoire": {
        "due_date": "2024-03-25",
        "borrower": "scholar"
    }
}

print(rs.return_book("The Lost Grimoire"))


from lending import ReturnSystem
from notifier import LibrarianNotifier

rs = ReturnSystem()
librarian = LibrarianNotifier()
rs.attach(librarian)

# Sample borrowed book data
rs.borrowed_books = {
    "Spellbound": {
        "due_date": "2024-04-01",
        "borrower": "scholar"
    }
}

print(rs.return_book("Spellbound"))


from search_system import BookSearchFilter

def main():
    # --- Book Creation ---
    book1 = AncientScript("Scroll of Wisdom", "Elder Kai", "111-111", "Fragile")
    book2 = RareBook("Cursed Chronicles", "Morgana", "222-222")
    book3 = GeneralBook("Python for Beginners", "Guido", "333-333")

    library_catalog = Catalog.get_instance()
    library_catalog.add_book(book1)
    library_catalog.add_book(book2)
    library_catalog.add_book(book3)

    # ... rest of your logic ...

    # --- 🔍 Search & Filter Demo ---
    search_filter = BookSearchFilter(library_catalog.books)

    print("\n🔎 Searching for books by author 'Guido':")
    results = search_filter.search_by_author("Guido")
    for book in results:
        print(book.get_details())

    print("\n📚 Filtering GeneralBooks:")
    general_books = search_filter.filter_by_type("GeneralBook")
    for book in general_books:
        print(book.get_details())

    print("\n📘 Available Books Only:")
    available_books = search_filter.filter_by_availability("Available")
    for book in available_books:
        print(book.get_details())

if __name__ == "__main__":
    main()


from reservation import BookReservation, ReserveBookCommand, ReservationInvoker

# Reservation Test
book_reservation = BookReservation("Cursed Chronicles")
reserve_cmd1 = ReserveBookCommand(book_reservation, "Zane")
reserve_cmd2 = ReserveBookCommand(book_reservation, "Nora")

invoker = ReservationInvoker()
invoker.add_reservation(reserve_cmd1)
invoker.add_reservation(reserve_cmd2)


from db_connection import insert_book, get_books

def main():
    # Example of inserting data into books table
    insert_book(
        title="The Enchanted Forest",
        author="Eldor",
        isbn="1234567890",
        book_type="RareBook",
        status="Available",
        condition="Good",
        is_restricted=False
    )

    # Example of fetching and displaying books
    print("\nAll Books in the Library:")
    get_books()

if __name__ == "__main__":
    main()
