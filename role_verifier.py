

valid_scholar_codes = [
    "SCH-2024-XX12",
    "SCH-2024-AZ78",
    "SCH-2024-QW34"
]

def verify_scholar_role(email, code):
    """
    Verifies if the given email is from a valid domain AND the code is in the valid scholar codes.
    """
    if email.endswith("@eldoria.edu") and code in valid_scholar_codes:
        return True
    return False

def verify_guest_role(email):
    """
    All emails allowed for guest access.
    """
    return True

def verify_librarian_role(secret_key):
    """
    Verifies librarian using a secret predefined key.
    """
    LIBRARIAN_KEY = "LIB-2024-MAGIC"
    return secret_key == LIBRARIAN_KEY


class RoleVerifier:
    def verify(self, user):
        return user.verified
