from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from ....common.errors import NotFoundError
from ....common.responses import success
from ....models import User
from .schemas import update_profile_schema

users_ns = Namespace("users", description="User profile management")

profile_update_model = users_ns.model("ProfileUpdate", {
    "first_name": fields.String,
    "last_name": fields.String,
    "date_of_birth": fields.String(description="YYYY-MM-DD"),
    "gender": fields.String(enum=["male", "female", "other", "prefer_not_to_say"]),
    "height_cm": fields.Float,
    "units": fields.String(enum=["metric", "imperial"]),
    "timezone": fields.String,
    "daily_calorie_target": fields.Integer,
    "daily_protein_target_g": fields.Integer,
    "daily_carbs_target_g": fields.Integer,
    "daily_fat_target_g": fields.Integer,
    "daily_water_target_ml": fields.Integer,
    "weekly_workout_target": fields.Integer,
})


def _get_user(user_id: str) -> User:
    user = User.objects(id=user_id).first()
    if not user:
        raise NotFoundError("User not found")
    return user


@users_ns.route("/me")
class Me(Resource):
    @jwt_required()
    @users_ns.response(200, "Profile data")
    def get(self):
        """Get own profile"""
        return success(_get_user(get_jwt_identity()).to_dict())

    @jwt_required()
    @users_ns.expect(profile_update_model)
    @users_ns.response(200, "Profile updated")
    def patch(self):
        """Update profile fields (send only fields you want to change)"""
        data = update_profile_schema.load(users_ns.payload or {})
        user = _get_user(get_jwt_identity())
        for field, value in data.items():
            setattr(user, field, value)
        user.updated_at = datetime.utcnow()
        user.save()
        return success(user.to_dict())

    @jwt_required()
    @users_ns.response(200, "Account deleted")
    def delete(self):
        """Delete own account and all associated data"""
        from ....models import DietLog, DietPlan
        user = _get_user(get_jwt_identity())
        DietLog.objects(user=user).delete()
        DietPlan.objects(user=user).delete()
        user.delete()
        return success({"message": "Account and all data deleted"})
