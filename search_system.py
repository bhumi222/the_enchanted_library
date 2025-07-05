class BookSearchFilter:
    def __init__(self, books):
        self.books = books

    def search_by_title(self, keyword):
        return [book for book in self.books if keyword.lower() in book.get_details()['Title'].lower()]

    def search_by_author(self, keyword):
        return [book for book in self.books if keyword.lower() in book.get_details()['Author'].lower()]

    def filter_by_type(self, book_type):
        return [book for book in self.books if book.__class__.__name__ == book_type]

    def filter_by_availability(self, status):
        return [book for book in self.books if book.get_details()["Status"] == status]
