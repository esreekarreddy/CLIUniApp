"""
models/subject.py
─────────────────
Represents a single subject enrolment.

• Auto-generates a 3-digit ID (001-999).
• Auto-assigns a random mark (25-100) and calculates grade
  using the UTS band rules defined in the spec.
"""

from __future__ import annotations
import random
from utils.utility import generate_subject_id

# ── Grade cut-offs (spec) ───────────────────────────────
#   85-100  HD
#   75-84   D
#   65-74   C
#   50-64   P
#   <50     Z
_GRADE_BANDS = [(85, "HD"), (75, "D"), (65, "C"), (50, "P"), (0, "Z")]


# -----------------------------------------------------------------
# Module-level helper – also used internally by the class.
# -----------------------------------------------------------------
def _grade_from_mark(mark: int) -> str:
    """Return the letter-grade that corresponds to a numeric mark."""
    for threshold, letter in _GRADE_BANDS:
        if mark >= threshold:
            return letter
    return "Z"                     # safety fallback


# -----------------------------------------------------------------
# Domain model
# -----------------------------------------------------------------
class Subject:
    """Immutable data object for a single subject enrolment."""

    # ---------- construction -----------------------------------
    def __init__(self, sub_id: str, mark: int, grade: str) -> None:
        self.id: str = sub_id
        self.mark: int = mark
        self.grade: str = grade

    # ---------- factory helper ---------------------------------
    @classmethod
    def auto_create(cls) -> "Subject":
        """
        Convenience constructor:
        • id    : random 3-digit string
        • mark  : random 25-100
        • grade : derived from mark
        """
        sub_id = generate_subject_id()
        mark = random.randint(25, 100)
        return cls(sub_id, mark, _grade_from_mark(mark))

    # ---------- helper required by unit-tests ------------------
    @staticmethod
    def _grade_from_mark(mark: int) -> str:
        """
        Thin wrapper around the module helper so tests can call
        `Subject._grade_from_mark()` or `instance._grade_from_mark()`.
        """
        return _grade_from_mark(mark)

    # ---------- grade recalculation ----------------------------
    def recalculate_grade(self) -> str:
        """Re-evaluate and update `self.grade` from current mark."""
        self.grade = _grade_from_mark(self.mark)
        return self.grade

    # ---------- (de)serialise for JSON persistence -------------
    def to_dict(self) -> dict:
        return {"id": self.id, "mark": self.mark, "grade": self.grade}

    @staticmethod
    def from_dict(d: dict) -> "Subject":
        return Subject(d["id"], d["mark"], d["grade"])

    # ---------- pretty string for CLI output -------------------
    def __str__(self) -> str:
        return f"{self.id}  {self.mark:3d}  {self.grade}"
