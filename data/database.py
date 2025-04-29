"""
data/database.py
────────────────
Light-weight persistence layer.

• Ensures `students.data` exists.
• Uses JSON so the file is human-readable for markers.
• All model <--> dict (de)serialisation is handled by Student / Subject.
"""

import os
import json
import pathlib
from typing import List
from models.student import Student

_DB_FILE = pathlib.Path(__file__).with_name("students.data")


# ── internal helper ───────────────────────────────────────────
def _ensure_file() -> None:
    """Create an empty JSON array file if it does not exist."""
    if not os.path.exists(_DB_FILE):
        with open(_DB_FILE, "w") as f:
            json.dump([], f)


# ── public API ------------------------------------------------
def load() -> List[Student]:
    """Read students.data → list[Student]."""
    _ensure_file()
    with open(_DB_FILE) as f:
        raw = json.load(f)
    return [Student.from_dict(d) for d in raw]


def save(students: List[Student]) -> None:
    """Write list[Student] → students.data (pretty-printed)."""
    _ensure_file()
    with open(_DB_FILE, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=2)
