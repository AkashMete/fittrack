"""Food item CRUD — users can only edit/delete their own custom foods (spec 3.3)."""
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from ....common.errors import ForbiddenError, NotFoundError
from ....common.pagination import get_page_args, paginate
from ....common.responses import success
from ....models import FoodItem, User
from .schemas import food_item_schema, food_item_update_schema

foods_ns = Namespace("foods", description="Food library")

food_model = foods_ns.model("Food", {
    "name": fields.String(required=True),
    "brand": fields.String,
    "category": fields.String,
    "calories_per_100g": fields.Float(required=True),
    "protein_per_100g": fields.Float,
    "carbs_per_100g": fields.Float,
    "fat_per_100g": fields.Float,
    "fiber_per_100g": fields.Float,
    "sugar_per_100g": fields.Float,
    "default_serving_g": fields.Float,
    "serving_unit": fields.String,
    "serving_description": fields.String,
    "tags": fields.List(fields.String),
})


def _get_food_or_404(food_id: str) -> FoodItem:
    food = FoodItem.objects(id=food_id).first()
    if not food:
        raise NotFoundError(f"Food item {food_id} not found")
    return food


def _assert_owner(food: FoodItem, user_id: str) -> None:
    if food.is_global or food.created_by is None:
        raise ForbiddenError("Cannot modify a global food item")
    if str(food.created_by.id) != user_id:
        raise ForbiddenError("You can only modify your own food items")


@foods_ns.route("")
class FoodList(Resource):
    @jwt_required()
    @foods_ns.param("q", "Search term (name)")
    @foods_ns.param("category", "Filter by category")
    @foods_ns.param("page", "Page number")
    @foods_ns.param("per_page", "Items per page")
    def get(self):
        """List foods — global + own custom foods, with optional search"""
        from flask import request
        user_id = get_jwt_identity()
        from bson import ObjectId

        q = request.args.get("q", "").strip()
        category = request.args.get("category", "").strip()
        page, per_page = get_page_args()

        # Global foods or this user's custom foods
        qs = FoodItem.objects(__raw__={
            "$or": [
                {"is_global": True},
                {"created_by": ObjectId(user_id)},
            ]
        })
        if q:
            qs = qs.filter(__raw__={"$text": {"$search": q}})
        if category:
            qs = qs.filter(category=category)

        items, meta = paginate(qs.order_by("name"), page, per_page)
        return success([f.to_dict() for f in items], meta=meta)

    @jwt_required()
    @foods_ns.expect(food_model)
    @foods_ns.response(201, "Food created")
    def post(self):
        """Create a custom food item"""
        data = food_item_schema.load(foods_ns.payload or {})
        user = User.objects(id=get_jwt_identity()).first()
        food = FoodItem(**data, created_by=user, is_global=False)
        food.save()
        return success(food.to_dict(), status_code=201)


@foods_ns.route("/<string:food_id>")
class FoodDetail(Resource):
    @jwt_required()
    def get(self, food_id: str):
        """Get food item details"""
        return success(_get_food_or_404(food_id).to_dict())

    @jwt_required()
    @foods_ns.expect(food_model)
    def patch(self, food_id: str):
        """Update a custom food item (own foods only)"""
        food = _get_food_or_404(food_id)
        _assert_owner(food, get_jwt_identity())
        data = food_item_update_schema.load(foods_ns.payload or {})
        food.update(**data)
        food.reload()
        return success(food.to_dict())

    @jwt_required()
    @foods_ns.response(200, "Deleted")
    def delete(self, food_id: str):
        """Delete a custom food item (own foods only)"""
        food = _get_food_or_404(food_id)
        _assert_owner(food, get_jwt_identity())
        food.delete()
        return success({"message": "Food item deleted"})
