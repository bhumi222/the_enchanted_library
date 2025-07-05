import json
from datetime import datetime

class BookConditionChecker:
    def __init__(self):
        self.log_file = "restoration_log.json"

    def check_condition(self, book):
        """
        Checks the book condition and flags it if needed.
        """
        if book["condition"] in ["Damaged", "Worn"]:
            self.flag_for_restoration(book)

    def flag_for_restoration(self, book):
        print(f"🔧 Book '{book['title']}' marked for restoration.")
        log_entry = {
            "title": book["title"],
            "book_id": book.get("book_id", "N/A"),
            "condition": book["condition"],
            "flagged_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Load existing log
        try:
            with open(self.log_file, "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []

        logs.append(log_entry)

        # Save updated log
        with open(self.log_file, "w") as file:
            json.dump(logs, file, indent=4)

        print("📢 Librarian notified. Entry added to restoration log.\n")
