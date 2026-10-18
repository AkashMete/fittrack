from datetime import datetime

from mongoengine import (
    BooleanField,
    DateField,
    DateTimeField,
    Document,
    EmailField,
    FloatField,
    IntField,
    StringField,
)


class User(Document):
    # Auth
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)  # bcrypt hash — NEVER plain text

    # Profile
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    date_of_birth = DateField()
    gender = StringField(choices=["male", "female", "other", "prefer_not_to_say"])
    height_cm = FloatField(min_value=0)
    profile_image_url = StringField()

    # Preferences
    units = StringField(choices=["metric", "imperial"], default="metric")
    timezone = StringField(default="UTC")

    # Daily targets (denormalized for single-query dashboard reads)
    daily_calorie_target = IntField(default=2000)
    daily_protein_target_g = IntField(default=150)
    daily_carbs_target_g = IntField(default=200)
    daily_fat_target_g = IntField(default=65)
    daily_water_target_ml = IntField(default=2000)
    weekly_workout_target = IntField(default=4)

    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    is_active = BooleanField(default=True)

    meta = {"collection": "users", "indexes": ["email"]}

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "height_cm": self.height_cm,
            "profile_image_url": self.profile_image_url,
            "units": self.units,
            "timezone": self.timezone,
            "daily_calorie_target": self.daily_calorie_target,
            "daily_protein_target_g": self.daily_protein_target_g,
            "daily_carbs_target_g": self.daily_carbs_target_g,
            "daily_fat_target_g": self.daily_fat_target_g,
            "daily_water_target_ml": self.daily_water_target_ml,
            "weekly_workout_target": self.weekly_workout_target,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
