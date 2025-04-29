# tests/conftest.py
"""
Shared pytest fixtures.

• tmp_path fixture from pytest gives a throw-away directory per test run.
• monkeypatch swaps the real students.data path so tests never touch
  your actual database.
"""

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from pathlib import Path
from data import database
from models.student import Student


def _fake_file(tmp_path) -> Path:
    """Return tmp_path/students.data (json array '[]')."""
    fake = tmp_path / "students.data"
    fake.write_text("[]")
    return fake


@pytest.fixture(autouse=True)
def patch_data_file(tmp_path, monkeypatch):
    """Redirect the global _DB_FILE to a temp file for the whole test run."""
    fake = _fake_file(tmp_path)
    monkeypatch.setattr(database, "_DB_FILE", fake)
    yield    # run tests
    # nothing to clean up – tmp_path is auto-deleted


@pytest.fixture
def fresh_student() -> Student:
    """Return a brand-new Student (not saved)."""
    return Student("Test User", "test.user@university.com", "Abcde123")
