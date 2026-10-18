"""Unit tests for auth service layer (no HTTP layer involved)."""
import pytest
from app import create_app
from app.api.v1.auth.services import (
    hash_password,
    login_user,
    register_user,
    verify_password,
)
from app.common.errors import ConflictError, UnauthorizedError


VALID_USER = {"email": "test@example.com", "password": "Password123!", "first_name": "Test"}


def test_hash_and_verify():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed)
    assert not verify_password("wrong", hashed)


def test_bcrypt_hash_not_plaintext():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"
    assert hashed.startswith("$2b$")


def test_register_creates_user():
    user = register_user(VALID_USER.copy())
    assert user.email == "test@example.com"
    assert user.password_hash != VALID_USER["password"]


def test_register_lowercases_email():
    user = register_user({**VALID_USER, "email": "UPPER@Example.COM"})
    assert user.email == "upper@example.com"


def test_register_duplicate_email_raises():
    register_user(VALID_USER.copy())
    with pytest.raises(ConflictError):
        register_user(VALID_USER.copy())


def test_login_success():
    register_user(VALID_USER.copy())
    user, access, refresh = login_user(VALID_USER["email"], VALID_USER["password"])
    assert user.email == "test@example.com"
    assert access
    assert refresh


def test_login_wrong_password():
    register_user(VALID_USER.copy())
    with pytest.raises(UnauthorizedError):
        login_user(VALID_USER["email"], "wrongpassword")


def test_login_unknown_email():
    with pytest.raises(UnauthorizedError):
        login_user("nobody@example.com", "pass")
