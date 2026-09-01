"""Shared pytest fixtures — app + test client reused across all test modules."""
import pytest

from app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app("testing")


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Push an app context and wipe all collections before each test."""
    from app.models import DietLog, DietPlan, FoodItem, TokenBlocklist, User
    ctx = app.app_context()
    ctx.push()
    for model in (TokenBlocklist, DietLog, DietPlan, FoodItem, User):
        model.drop_collection()
    yield
    ctx.pop()
