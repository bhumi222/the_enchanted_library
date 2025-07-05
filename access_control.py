

class Role:
    GUEST = "Guest"
    SCHOLAR = "Scholar"
    LIBRARIAN = "Librarian"

# Base class for access control
class AccessControl:
    def __init__(self, role):
        self.role = role

    def can_view_books(self):
        return True  # Everyone can view general books

    def can_borrow_rare_books(self):
        return self.role in [Role.SCHOLAR, Role.LIBRARIAN]

    def can_access_restricted_section(self):
        return self.role == Role.LIBRARIAN

    def can_manage_users(self):
        return self.role == Role.LIBRARIAN

    def can_restore_books(self):
        return self.role == Role.LIBRARIAN
