"""Diet business logic — macro recalculation lives here, not in routes."""
from datetime import date, datetime

from bson import ObjectId

from ....common.errors import BadRequestError, NotFoundError
from ....models import DietLog, DietLogEntry, DietPlan, DietPlanItem, DietPlanMeal, FoodItem, User


# ── helpers ──────────────────────────────────────────────────────────────────

def _food_or_404(food_id: str) -> FoodItem:
    food = FoodItem.objects(id=food_id).first()
    if not food:
        raise NotFoundError(f"Food item {food_id} not found")
    return food


def _calc_macros_for_quantity(food: FoodItem, quantity_g: float) -> dict:
    ratio = quantity_g / 100
    return {
        "calories": round(food.calories_per_100g * ratio, 2),
        "protein_g": round(food.protein_per_100g * ratio, 2),
        "carbs_g": round(food.carbs_per_100g * ratio, 2),
        "fat_g": round(food.fat_per_100g * ratio, 2),
        "fiber_g": round((food.fiber_per_100g or 0) * ratio, 2),
    }


def _recompute_log_totals(log: DietLog) -> None:
    """Recalculate day totals from embedded entries and persist."""
    log.total_calories = round(sum(e.calories or 0 for e in log.entries), 2)
    log.total_protein_g = round(sum(e.protein_g or 0 for e in log.entries), 2)
    log.total_carbs_g = round(sum(e.carbs_g or 0 for e in log.entries), 2)
    log.total_fat_g = round(sum(e.fat_g or 0 for e in log.entries), 2)
    log.updated_at = datetime.utcnow()
    log.save()


def _recompute_plan_totals(plan: DietPlan) -> None:
    plan.total_calories = round(sum(i.calories or 0 for m in plan.meals for i in m.items), 2)
    plan.total_protein_g = round(sum(i.protein_g or 0 for m in plan.meals for i in m.items), 2)
    plan.total_carbs_g = round(sum(i.carbs_g or 0 for m in plan.meals for i in m.items), 2)
    plan.total_fat_g = round(sum(i.fat_g or 0 for m in plan.meals for i in m.items), 2)
    plan.updated_at = datetime.utcnow()
    plan.save()


# ── plans ─────────────────────────────────────────────────────────────────────

def create_plan(user: User, data: dict) -> DietPlan:
    meals = []
    for meal_data in data.get("meals", []):
        items = []
        for item_data in meal_data.get("items", []):
            food = _food_or_404(item_data["food_item_id"])
            macros = _calc_macros_for_quantity(food, item_data["quantity_g"])
            items.append(DietPlanItem(
                food_item=food,
                quantity_g=item_data["quantity_g"],
                food_name=food.name,
                **macros,
            ))
        meals.append(DietPlanMeal(meal_type=meal_data["meal_type"], items=items))

    plan = DietPlan(user=user, name=data["name"], description=data.get("description"), meals=meals)
    _recompute_plan_totals(plan)
    return plan


def update_plan(plan: DietPlan, data: dict) -> DietPlan:
    if "name" in data:
        plan.name = data["name"]
    if "description" in data:
        plan.description = data["description"]
    if "meals" in data:
        meals = []
        for meal_data in data["meals"]:
            items = []
            for item_data in meal_data.get("items", []):
                food = _food_or_404(item_data["food_item_id"])
                macros = _calc_macros_for_quantity(food, item_data["quantity_g"])
                items.append(DietPlanItem(
                    food_item=food,
                    quantity_g=item_data["quantity_g"],
                    food_name=food.name,
                    **macros,
                ))
            meals.append(DietPlanMeal(meal_type=meal_data["meal_type"], items=items))
        plan.meals = meals
    _recompute_plan_totals(plan)
    return plan


def activate_plan(user: User, plan: DietPlan) -> DietPlan:
    DietPlan.objects(user=user, is_active=True).update(is_active=False)
    plan.update(is_active=True)
    plan.reload()
    return plan


def duplicate_plan(user: User, plan: DietPlan) -> DietPlan:
    new_plan = DietPlan(
        user=user,
        name=f"{plan.name} (copy)",
        description=plan.description,
        meals=plan.meals,
        total_calories=plan.total_calories,
        total_protein_g=plan.total_protein_g,
        total_carbs_g=plan.total_carbs_g,
        total_fat_g=plan.total_fat_g,
    )
    new_plan.save()
    return new_plan


# ── daily logs ────────────────────────────────────────────────────────────────

def get_or_create_log(user: User, log_date: date) -> DietLog:
    log = DietLog.objects(user=user, date=log_date).first()
    if not log:
        log = DietLog(user=user, date=log_date)
        log.save()
    return log


def add_entry(user: User, log_date: date, data: dict) -> tuple[DietLog, DietLogEntry]:
    food = _food_or_404(data["food_item_id"])
    macros = _calc_macros_for_quantity(food, data["quantity_g"])
    entry = DietLogEntry(
        food_item=food,
        quantity_g=data["quantity_g"],
        meal_type=data["meal_type"],
        food_name=food.name,
        calories=macros["calories"],
        protein_g=macros["protein_g"],
        carbs_g=macros["carbs_g"],
        fat_g=macros["fat_g"],
    )
    log = get_or_create_log(user, log_date)
    log.entries.append(entry)
    _recompute_log_totals(log)
    return log, entry


def update_entry(user: User, log_date: date, entry_id: str, data: dict) -> DietLog:
    log = DietLog.objects(user=user, date=log_date).first()
    if not log:
        raise NotFoundError("Diet log not found for this date")
    entry = next((e for e in log.entries if e.entry_id == entry_id), None)
    if not entry:
        raise NotFoundError(f"Entry {entry_id} not found")

    if "quantity_g" in data:
        entry.quantity_g = data["quantity_g"]
        macros = _calc_macros_for_quantity(entry.food_item, entry.quantity_g)
        entry.calories = macros["calories"]
        entry.protein_g = macros["protein_g"]
        entry.carbs_g = macros["carbs_g"]
        entry.fat_g = macros["fat_g"]
    if "meal_type" in data:
        entry.meal_type = data["meal_type"]

    _recompute_log_totals(log)
    return log


def delete_entry(user: User, log_date: date, entry_id: str) -> DietLog:
    log = DietLog.objects(user=user, date=log_date).first()
    if not log:
        raise NotFoundError("Diet log not found for this date")
    original_count = len(log.entries)
    log.entries = [e for e in log.entries if e.entry_id != entry_id]
    if len(log.entries) == original_count:
        raise NotFoundError(f"Entry {entry_id} not found")
    _recompute_log_totals(log)
    return log


def import_from_plan(user: User, log_date: date) -> DietLog:
    plan = DietPlan.objects(user=user, is_active=True).first()
    if not plan:
        raise BadRequestError("No active diet plan found")
    log = get_or_create_log(user, log_date)
    for meal in plan.meals:
        for item in meal.items:
            food = item.food_item
            if not food:
                continue
            macros = _calc_macros_for_quantity(food, item.quantity_g)
            log.entries.append(DietLogEntry(
                food_item=food,
                quantity_g=item.quantity_g,
                meal_type=meal.meal_type,
                food_name=food.name,
                calories=macros["calories"],
                protein_g=macros["protein_g"],
                carbs_g=macros["carbs_g"],
                fat_g=macros["fat_g"],
            ))
    _recompute_log_totals(log)
    return log


# ── monthly report ────────────────────────────────────────────────────────────

def monthly_report(user: User, year: int, month: int) -> dict:
    import calendar

    start = date(year, month, 1)
    end = date(year, month, calendar.monthrange(year, month)[1])

    logs = list(DietLog.objects(user=user, date__gte=start, date__lte=end))
    if not logs:
        return {
            "year": year, "month": month, "days_logged": 0,
            "avg_calories": 0, "avg_protein_g": 0, "avg_carbs_g": 0, "avg_fat_g": 0,
            "calorie_trend": [],
        }

    calorie_trend = [{"date": l.date.isoformat(), "calories": l.total_calories} for l in logs]
    n = len(logs)
    return {
        "year": year,
        "month": month,
        "days_logged": n,
        "avg_calories": round(sum(l.total_calories for l in logs) / n, 1),
        "avg_protein_g": round(sum(l.total_protein_g for l in logs) / n, 1),
        "avg_carbs_g": round(sum(l.total_carbs_g for l in logs) / n, 1),
        "avg_fat_g": round(sum(l.total_fat_g for l in logs) / n, 1),
        "calorie_trend": calorie_trend,
    }
