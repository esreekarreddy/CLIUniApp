"""
controllers/admin_controller.py
───────────────────────────────
Admin-side operations:

• show all students
• group students by overall grade
• partition students into PASS / FAIL
• remove a student by ID
• clear the entire database
"""

from __future__ import annotations
from typing import Dict, List

from data.database import load, save
from models.student import Student


class AdminController:
    """Light façade around database-level CRUD for admins."""

    # ── initialisation ────────────────────────────────────────
    def __init__(self) -> None:
        self.refresh()     # prime the cache

    # ── cache handling ----------------------------------------
    def refresh(self) -> None:
        """Reload the latest snapshot from *students.data* into `self.students`."""
        self.students: List[Student] = load()

    @staticmethod
    def _snapshot() -> List[Student]:
        """Always pull the newest copy straight from disk."""
        return load()

    # ── read-only queries -------------------------------------
    def show_students(self) -> List[Student]:
        """Return all students (sorted by ID for nicer CLI output)."""
        return sorted(self._snapshot(), key=lambda s: s.id)

    def group_by_grade(self) -> Dict[str, List[Student]]:
        """
        Return { grade (HD/D/C/P/Z) : [students] }.

        Uses each student's **overall grade** (average of their subjects),
        so a student appears in *one* group only – exactly as illustrated
        in the sample I/O.
        """
        grouped: Dict[str, List[Student]] = {}
        for stu in self._snapshot():
            grouped.setdefault(stu.overall_grade, []).append(stu)
        return grouped

    def partition_pass_fail(self) -> Dict[str, List[Student]]:
        """
        Return two buckets keyed 'PASS' / 'FAIL'.

        • PASS  ➜ average mark ≥ 50  
        • FAIL  ➜ average mark < 50  *or* no subjects enrolled
        """
        buckets = {"PASS": [], "FAIL": []}
        for stu in self._snapshot():
            bucket = "PASS" if stu.average_mark >= 50 else "FAIL"
            buckets[bucket].append(stu)
        return buckets

    # ── mutating actions --------------------------------------
    def remove_student(self, student_id: str) -> bool:
        """
        Delete a student by ID.

        Returns **True** if a record was removed, otherwise **False**.
        """
        current = self._snapshot()
        updated = [s for s in current if s.id != student_id]

        if len(updated) == len(current):        # nothing removed
            return False

        save(updated)
        return True

    def clear_database(self) -> None:
        """Erase *all* student records."""
        save([])        # write empty list
