from abc import ABC, abstractmethod

# Base User Class
class User(ABC):
    def __init__(self, name, user_id):
        self._name = name
        self._user_id = user_id

    @abstractmethod
    def get_role(self):
        pass

    def get_details(self):
        return {
            "Name": self._name,
            "ID": self._user_id,
            "Role": self.get_role()
        }

# Inherited Roles
class Librarian(User):
    def get_role(self):
        return "Librarian"

class Scholar(User):
    def get_role(self):
        return "Scholar"

class Guest(User):
    def get_role(self):
        return "Guest"

# Factory Pattern for Users
class UserFactory:
    @staticmethod
    def create_user(role, name, user_id):
        role = role.lower()
        if role == "librarian":
            return Librarian(name, user_id)
        elif role == "scholar":
            return Scholar(name, user_id)
        elif role == "guest":
            return Guest(name, user_id)
        else:
            raise ValueError(f"Unknown role: {role}")



# user.py

from verification_system import VerificationSystem

class User:
    def __init__(self, name, email, role, verified=False):
        self.name = name
        self.email = email
        self.role = role
        self.verified = verified
        self.research_topic = None  # optional, used only by scholars

    def request_verification(self):
        self.verified = VerificationSystem().verify_user(self)
        return self.verified


    def request_verification(self, vsys):
        if self.role == "scholar":
            code = vsys.generate_code(self.email)
            print(f"Verification code for {self.name} sent: {code}")

    def verify_code(self, vsys, code):
        if vsys.verify(self.email, code):
            self.verified = True
            print(f"{self.name} verified successfully.")
        else:
            print(f"Verification failed for {self.name}.")
