

from datetime import datetime

class LateFeeCalculator:
    def __init__(self, role, book_type, borrow_date_str, return_date_str):
        self.role = role
        self.book_type = book_type
        self.borrow_date = datetime.strptime(borrow_date_str, "%Y-%m-%d")
        self.return_date = datetime.strptime(return_date_str, "%Y-%m-%d")

        self.fee_rates = {
            "Guest": {
                "GeneralBook": 5,
                "RareBook": 10,
                "AncientScript": 20,
            },
            "Scholar": {
                "GeneralBook": 2,
                "RareBook": 5,
                "AncientScript": 10,
            },
            "Librarian": {
                "GeneralBook": 0,
                "RareBook": 0,
                "AncientScript": 0,
            },
        }

        self.allowed_days = {
            "Guest": 7,
            "Scholar": 14,
            "Librarian": 30,
        }

    def calculate_fee(self):
        delta_days = (self.return_date - self.borrow_date).days
        free_limit = self.allowed_days[self.role]

        if delta_days <= free_limit:
            return 0
        else:
            overdue_days = delta_days - free_limit
            rate = self.fee_rates[self.role][self.book_type]
            return overdue_days * rate
