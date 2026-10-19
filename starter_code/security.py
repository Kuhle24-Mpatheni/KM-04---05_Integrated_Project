
"""
security.py
Basic password access control for sales reports.
"""

import hashlib
import getpass


def hash_password(plain_text_password: str) -> str:
    """Return the SHA-256 hash of a password."""
    return hashlib.sha256(
        plain_text_password.encode("utf-8")
    ).hexdigest()


# Store the hash, not the original password.
STORED_PASSWORD_HASH = hash_password("Spaza2026!")


def check_password(attempt: str, stored_hash: str) -> bool:
    """Check a password attempt against a stored hash."""
    attempt_hash = hash_password(attempt)
    return attempt_hash == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:
    """Allow access after a successful password check."""
    for attempt_number in range(max_attempts):
        attempt = getpass.getpass(
            "Enter password to view reports: "
        )

        if check_password(attempt, stored_hash):
            print("Access granted.")
            return True
        else:
            print("Incorrect password. Try again.")

    print("Access denied - too many failed attempts.")
    return False
