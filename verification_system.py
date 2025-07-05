import random
import string

class VerificationSystem:
    def __init__(self):
        self.pending_verifications = {}  # email: code

    def generate_code(self, email):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.pending_verifications[email] = code
        return code

    def verify(self, email, entered_code):
        if email in self.pending_verifications and self.pending_verifications[email] == entered_code:
            del self.pending_verifications[email]
            return True
        return False
