"""Integration tests for auth HTTP endpoints."""
import json
import pytest


BASE = "/api/v1/auth"

REGISTER_PAYLOAD = {
    "email": "user@example.com",
    "password": "Password123!",
    "first_name": "Jane",
}


def test_register_201(client):
    rv = client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["status"] == "success"
    assert data["data"]["access_token"]


def test_register_duplicate_409(client):
    client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    rv = client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    assert rv.status_code == 409


def test_register_invalid_email_400(client):
    rv = client.post(f"{BASE}/register", json={"email": "not-email", "password": "Abc12345!"})
    assert rv.status_code == 400


def test_login_200(client):
    client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    rv = client.post(f"{BASE}/login", json={"email": REGISTER_PAYLOAD["email"], "password": REGISTER_PAYLOAD["password"]})
    assert rv.status_code == 200
    assert rv.get_json()["data"]["access_token"]


def test_login_wrong_password_401(client):
    client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    rv = client.post(f"{BASE}/login", json={"email": REGISTER_PAYLOAD["email"], "password": "wrong"})
    assert rv.status_code == 401


def test_protected_without_token_401(client):
    rv = client.get("/api/v1/users/me")
    assert rv.status_code == 401


def test_protected_with_token_200(client):
    rv = client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    token = rv.get_json()["data"]["access_token"]
    rv = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert rv.status_code == 200


def test_password_change(client):
    rv = client.post(f"{BASE}/register", json=REGISTER_PAYLOAD)
    token = rv.get_json()["data"]["access_token"]
    rv = client.post(
        f"{BASE}/password/change",
        json={"current_password": REGISTER_PAYLOAD["password"], "new_password": "NewPass99!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert rv.status_code == 200
