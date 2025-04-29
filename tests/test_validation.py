# tests/test_validation.py
from utils.utility import validate_email, validate_password


def test_validate_email_ok():
    assert validate_email("alice.smith@university.com")


def test_validate_email_bad_domain():
    assert not validate_email("bob@uni.com")


def test_password_ok():
    assert validate_password("Abcde123")


def test_password_requires_uppercase():
    assert not validate_password("abcde123")


def test_password_requires_at_least_five_letters():
    assert not validate_password("Abc1")   # only 3 letters


def test_password_requires_three_digits():
    assert not validate_password("Abcdef1")
