from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

FOOD_CATEGORIES = [
    "protein",
    "carbs",
    "fats",
    "vegetables",
    "fruits",
    "dairy",
    "grains",
    "supplements",
]


class FoodItem(Document):
    name = StringField(required=True, max_length=200)
    brand = StringField(max_length=100)
    category = StringField(choices=FOOD_CATEGORIES)

    # Nutrition per 100g — consistent baseline for every calculation
    calories_per_100g = FloatField(required=True, min_value=0)
    protein_per_100g = FloatField(default=0, min_value=0)
    carbs_per_100g = FloatField(default=0, min_value=0)
    fat_per_100g = FloatField(default=0, min_value=0)
    fiber_per_100g = FloatField(default=0, min_value=0)
    sugar_per_100g = FloatField(default=0, min_value=0)

    # Serving info
    default_serving_g = FloatField(default=100)
    serving_unit = StringField(default="g")
    serving_description = StringField()

    image_url = StringField()
    tags = ListField(StringField())

    # Ownership — created_by None + is_global True = seeded food visible to all
    created_by = ReferenceField("User", null=True)
    is_global = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "food_items",
        "indexes": [
            "name",
            "created_by",
            ("name", "created_by"),
            {"fields": ["$name"], "default_language": "english"},  # full-text search
        ],
    }

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "calories_per_100g": self.calories_per_100g,
            "protein_per_100g": self.protein_per_100g,
            "carbs_per_100g": self.carbs_per_100g,
            "fat_per_100g": self.fat_per_100g,
            "fiber_per_100g": self.fiber_per_100g,
            "sugar_per_100g": self.sugar_per_100g,
            "default_serving_g": self.default_serving_g,
            "serving_unit": self.serving_unit,
            "serving_description": self.serving_description,
            "image_url": self.image_url,
            "tags": list(self.tags or []),
            "is_global": self.is_global,
            "is_custom": not self.is_global,
        }
