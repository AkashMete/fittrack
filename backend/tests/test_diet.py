"""Tests for diet service layer — macro calculations and log management."""
import pytest
from app.api.v1.auth.services import register_user
from app.api.v1.diet import services as diet_svc
from app.models import FoodItem


CHICKEN = dict(
    name="Test Chicken",
    category="protein",
    calories_per_100g=120.0,
    protein_per_100g=22.5,
    carbs_per_100g=0.0,
    fat_per_100g=2.6,
    is_global=True,
)

USER_DATA = {"email": "dieter@example.com", "password": "Pass1234!", "first_name": "D"}


@pytest.fixture
def user():
    return register_user(USER_DATA.copy())


@pytest.fixture
def chicken():
    f = FoodItem(**CHICKEN)
    f.save()
    return f


def test_get_or_create_log_creates(user):
    from datetime import date
    log = diet_svc.get_or_create_log(user, date.today())
    assert log.id is not None
    assert log.total_calories == 0


def test_add_entry_calculates_macros(user, chicken):
    from datetime import date
    log, entry = diet_svc.add_entry(
        user, date.today(),
        {"food_item_id": str(chicken.id), "quantity_g": 150, "meal_type": "lunch"}
    )
    # 150g * 22.5 / 100 = 33.75
    assert entry.protein_g == pytest.approx(33.75, rel=0.01)
    assert log.total_calories == pytest.approx(150 * 120 / 100, rel=0.01)


def test_delete_entry_removes_and_recalculates(user, chicken):
    from datetime import date
    log, entry = diet_svc.add_entry(
        user, date.today(),
        {"food_item_id": str(chicken.id), "quantity_g": 100, "meal_type": "breakfast"}
    )
    log = diet_svc.delete_entry(user, date.today(), entry.entry_id)
    assert len(log.entries) == 0
    assert log.total_calories == 0


def test_macro_recalc_on_update(user, chicken):
    from datetime import date
    log, entry = diet_svc.add_entry(
        user, date.today(),
        {"food_item_id": str(chicken.id), "quantity_g": 100, "meal_type": "lunch"}
    )
    log = diet_svc.update_entry(user, date.today(), entry.entry_id, {"quantity_g": 200})
    assert log.total_calories == pytest.approx(200 * 120 / 100, rel=0.01)


def test_monthly_report_empty(user):
    report = diet_svc.monthly_report(user, 2025, 1)
    assert report["days_logged"] == 0
    assert report["avg_calories"] == 0
