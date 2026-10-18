from datetime import datetime

from bson import ObjectId
from mongoengine import (
    DateField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

from .diet_plan import MEAL_TYPES


class DietLogEntry(EmbeddedDocument):
    """Embedded — entries are only ever read together with their day's log."""

    entry_id = StringField(default=lambda: str(ObjectId()))
    food_item = ReferenceField("FoodItem", required=True)
    quantity_g = FloatField(required=True, min_value=0.1)
    meal_type = StringField(choices=MEAL_TYPES)

    # Snapshot at log time — history stays correct even if the food is edited/deleted
    food_name = StringField()
    calories = FloatField(default=0)
    protein_g = FloatField(default=0)
    carbs_g = FloatField(default=0)
    fat_g = FloatField(default=0)

    logged_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "food_item_id": str(self.food_item.id) if self.food_item else None,
            "food_name": self.food_name,
            "quantity_g": self.quantity_g,
            "meal_type": self.meal_type,
            "calories": self.calories,
            "protein_g": self.protein_g,
            "carbs_g": self.carbs_g,
            "fat_g": self.fat_g,
            "logged_at": self.logged_at.isoformat() if self.logged_at else None,
        }


class DietLog(Document):
    user = ReferenceField("User", required=True)
    date = DateField(required=True)  # one document per user per day
    entries = ListField(EmbeddedDocumentField(DietLogEntry))

    # Day totals — recalculated on every write (cheap reads for dashboard/report)
    total_calories = FloatField(default=0)
    total_protein_g = FloatField(default=0)
    total_carbs_g = FloatField(default=0)
    total_fat_g = FloatField(default=0)
    total_fiber_g = FloatField(default=0)

    notes = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "diet_logs",
        "indexes": [
            {"fields": ["user", "date"], "unique": True},
            "date",
        ],
    }

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "date": self.date.isoformat() if self.date else None,
            "entries": [e.to_dict() for e in self.entries],
            "total_calories": self.total_calories,
            "total_protein_g": self.total_protein_g,
            "total_carbs_g": self.total_carbs_g,
            "total_fat_g": self.total_fat_g,
            "total_fiber_g": self.total_fiber_g,
            "notes": self.notes,
        }
