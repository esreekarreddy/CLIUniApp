"""
models/student.py
─────────────────
• Private attributes (`__`) with @property getters
• Registration-time validation handled by StudentController
• Up to 4 subjects; auto-grade mark on enrol
• JSON (de)serialise helpers for Database layer
"""

from __future__ import annotations
from typing import List
from utils.utility import validate_password, generate_student_id
from models.subject import Subject

# ── Grade cut-offs (spec) ────────────────────────────────
_GRADE_BANDS = [
    (85, "HD"),
    (75, "D"),
    (65, "C"),
    (50, "P"),
    (0,  "Z"),
]


class Student:
    """Domain model representing ONE student."""

    # ---------- construction ----------------------------------
    def __init__(self, name: str, email: str, password: str) -> None:
        self.__id: str = generate_student_id()
        self.__name: str = name
        self.__email: str = email
        self.__password: str = password
        self.__subjects: List[Subject] = []

    # ---------- read-only / controlled attributes -------------
    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def subjects(self) -> List[Subject]:
        """Exposes the list for iteration; list itself remains private."""
        return self.__subjects

    # ---------- derived academic info -------------------------
    @property
    def average_mark(self) -> float:
        if not self.__subjects:
            return 0.0
        return sum(s.mark for s in self.__subjects) / len(self.__subjects)

    @property
    def overall_grade(self) -> str:
        for cut, g in _GRADE_BANDS:
            if self.average_mark >= cut:
                return g
        return "Z"

    # ---------- authentication --------------------------------
    def check_login(self, email: str, pwd: str) -> bool:
        return self.__email == email and self.__password == pwd

    # ---------- password management ---------------------------
    def change_password(self, old: str, new: str) -> bool:
        if self.__password == old and validate_password(new):
            self.__password = new
            return True
        return False

    # ---------- subject enrolment -----------------------------
    def enrol(self):
        """Add a subject (auto-generated) if under the 4-subject limit."""
        if len(self.__subjects) >= 4:
            return False, "Subject limit (4) reached."
        sub = Subject.auto_create()
        self.__subjects.append(sub)
        return True, sub

    def remove_subject(self, sub_id: str) -> bool:
        before = len(self.__subjects)
        self.__subjects = [s for s in self.__subjects if s.id != sub_id]
        return len(self.__subjects) < before

    # ---------- (de)serialise helpers -------------------------
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "name": self.__name,
            "email": self.__email,
            "password": self.__password,
            "subjects": [s.to_dict() for s in self.__subjects],
        }

    @staticmethod
    def from_dict(d: dict) -> "Student":
        obj = Student.__new__(Student)        # bypass __init__
        obj.__id = d["id"]
        obj.__name = d["name"]
        obj.__email = d["email"]
        obj.__password = d["password"]
        obj.__subjects = [Subject.from_dict(x) for x in d.get("subjects", [])]
        return obj

    # ---------- identity / equality ---------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return False
        return self.__id == other.__id

    def __hash__(self) -> int:
        return hash(self.__id)

    # ---------- pretty CLI string -----------------------------
    def __str__(self) -> str:
        return (
            f"{self.__id}  {self.__name:<20}  "
            f"subjects:{len(self.__subjects)}  "
            f"AVG:{self.average_mark:5.2f}  GRADE:{self.overall_grade}"
        )
