class FineCalculator:
    def __init__(self, role):
        self.role = role.lower()
        self.fine_rates = {
            "guest": 10,       # ₹10 per day late
            "scholar": 5,      # ₹5 per day late
            "librarian": 0     # No fine
        }

    def calculate_fine(self, days_late):
        rate = self.fine_rates.get(self.role, 10)
        return days_late * rate
