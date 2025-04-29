"""
utils/utility.py
────────────────
Shared helper functions for validation and ID generation.
Keeps regex logic in ONE place so controllers & models stay clean.
"""

import re
import random

# ── Regular-expression patterns ──────────────────────────────
_EMAIL_RE = re.compile(r"^[\w\.]+@university\.com$")

def validate_email(email: str) -> bool:
    """Return True if e-mail ends with '@university.com'."""
    return bool(_EMAIL_RE.fullmatch(email))

def validate_password(pwd: str) -> bool:
    """
    Password rules (assignment spec):
    • Starts with uppercase
    • ≥ 5 letters total
    • ≥ 3 digits total
    """
    return (
        pwd[:1].isupper() and
        sum(c.isalpha() for c in pwd) >= 5 and
        sum(c.isdigit() for c in pwd) >= 3
    )

# ── ID generators ────────────────────────────────────────────
def generate_student_id() -> str:
    """Six-digit zero-padded student ID (000001-999999)."""
    return f"{random.randint(1, 999_999):06d}"

def generate_subject_id() -> str:
    """Three-digit zero-padded subject ID (001-999)."""
    return f"{random.randint(1, 999):03d}"
