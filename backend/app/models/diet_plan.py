from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack", "pre_workout", "post_workout"]


class DietPlanItem(EmbeddedDocument):
    food_item = ReferenceField("FoodItem", required=True)
    quantity_g = FloatField(required=True, min_value=0.1)

    # Snapshot of macros for this quantity (kept in sync when plan is written)
    food_name = StringField()
    calories = FloatField(default=0)
    protein_g = FloatField(default=0)
    carbs_g = FloatField(default=0)
    fat_g = FloatField(default=0)

    def to_dict(self) -> dict:
        return {
            "food_item_id": str(self.food_item.id) if self.food_item else None,
            "food_name": self.food_name,
            "quantity_g": self.quantity_g,
            "calories": self.calories,
            "protein_g": self.protein_g,
            "carbs_g": self.carbs_g,
            "fat_g": self.fat_g,
        }


class DietPlanMeal(EmbeddedDocument):
    meal_type = StringField(required=True, choices=MEAL_TYPES)
    items = ListField(EmbeddedDocumentField(DietPlanItem))

    def to_dict(self) -> dict:
        return {
            "meal_type": self.meal_type,
            "items": [i.to_dict() for i in self.items],
        }


class DietPlan(Document):
    user = ReferenceField("User", required=True)
    name = StringField(required=True, max_length=100)
    description = StringField(max_length=500)
    meals = ListField(EmbeddedDocumentField(DietPlanMeal))
    is_active = BooleanField(default=False)

    # Plan totals — recalculated on every write
    total_calories = FloatField(default=0)
    total_protein_g = FloatField(default=0)
    total_carbs_g = FloatField(default=0)
    total_fat_g = FloatField(default=0)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "diet_plans",
        "indexes": ["user", ("user", "is_active")],
    }

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "meals": [m.to_dict() for m in self.meals],
            "total_calories": self.total_calories,
            "total_protein_g": self.total_protein_g,
            "total_carbs_g": self.total_carbs_g,
            "total_fat_g": self.total_fat_g,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
