# In some test or main file

from user import User
from book_recommender import BookRecommender

# Sample scholar user
scholar = User(name="Aanya", role="scholar", verified=True)
scholar.research_topic = "Magic"

recommender = BookRecommender(scholar)
books = recommender.recommend_books()

print("📚 Recommended Books:")
for book in books:
    print("-", book)

