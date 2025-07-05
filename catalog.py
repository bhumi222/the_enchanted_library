class Catalog:
    __instance = None

    def __init__(self):
        if Catalog.__instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            self.books = []
            Catalog.__instance = self

    @staticmethod
    def get_instance():
        if Catalog.__instance is None:
            Catalog()
        return Catalog.__instance

    def add_book(self, book):
        self.books.append(book)
        print(f"[+] Book added: {book.get_details()['Title']}")

    def list_books(self):
        for book in self.books:
            details = book.get_details()
            print(f"{details['Title']} by {details['Author']} | Status: {details['Status']}")

    def find_by_title(self, title):
        for book in self.books:
            if book.get_details()["Title"].lower() == title.lower():
                return book
        return None
