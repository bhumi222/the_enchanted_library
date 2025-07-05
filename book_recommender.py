

from role_verifier import RoleVerifier

# Dummy book database for recommendations
BOOK_DATABASE = {
    "General": ["Tales of Eldoria", "Beginner Magic Books", "Legends & Lore"],
    "Scholar": ["Ancient Manuscripts", "Mystic Scrolls", "Runes & Research"],
    "Librarian": ["Library Logs", "Preservation Manuals", "Historical Bookkeeping"]
}

# Dummy research topic-wise suggestions
RESEARCH_TOPICS = {
    "History": ["Chronicles of Eldoria", "Timeline Scrolls"],
    "Magic": ["Advanced Spellwork", "Arcane Arts Volume II"],
    "Philosophy": ["Writings of the Wise", "Mystic Reflections"]
}

class BookRecommender:
    def __init__(self, all_books):
        self.all_books = all_books

    def recommend_books(self, reading_history, interest):
        read_tags = set()
        for book in reading_history:
            read_tags.update(book["tags"])

        recommended = []
        for book in self.all_books:
            if book["title"] in [b["title"] for b in reading_history]:
                continue  # Skip already read books
            if interest in book["tags"] or not read_tags.isdisjoint(book["tags"]):
                recommended.append(book)

        return recommended
