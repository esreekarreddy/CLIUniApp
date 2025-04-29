"""
controllers/student_controller.py
─────────────────────────────────
Student-side use-cases:

• register
• login
• (persistence delegations)

─────────────────────────────────
"""

from __future__ import annotations
from typing import Tuple
from utils.utility import validate_email, validate_password
from data.database import load, save
from models.student import Student


class StudentController:
    def __init__(self) -> None:
        # pull the current snapshot each time the controller is instantiated
        self.students = load()

    # ── registration ────────────────────────────────────────────
    def register(self, name: str, email: str, password: str) -> Tuple[bool, str | Student]:
        """
        Returns (True, Student) if success,
                (False, reason) otherwise.
        """
        if not validate_email(email):
            return False, "Invalid email format (must end with @university.com)."

        if not validate_password(password):
            return False, (
                "Password must start with uppercase, contain ≥5 letters "
                "and ≥3 digits."
            )

        if any(s.email == email for s in self.students):
            return False, "A student with this email already exists."

        stu = Student(name, email, password)
        self.students.append(stu)
        save(self.students)
        return True, stu

    # ── login  ──────────────────────────────────────────────────
    def login(self, email: str, password: str) -> Tuple[bool, Student | None]:
        """
        Returns (True, Student) if credentials match,
                (False, None) otherwise.
        """
        # refresh list in case of external changes
        self.students = load()
        for stu in self.students:
            if stu.check_login(email, password):
                return True, stu
        return False, None
