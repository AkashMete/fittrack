from marshmallow import Schema, fields, validate

CATEGORIES = ["protein", "carbs", "fats", "vegetables", "fruits", "dairy", "grains", "supplements"]


class FoodItemSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    brand = fields.String(validate=validate.Length(max=100))
    category = fields.String(validate=validate.OneOf(CATEGORIES))
    calories_per_100g = fields.Float(required=True, validate=validate.Range(min=0))
    protein_per_100g = fields.Float(validate=validate.Range(min=0), load_default=0)
    carbs_per_100g = fields.Float(validate=validate.Range(min=0), load_default=0)
    fat_per_100g = fields.Float(validate=validate.Range(min=0), load_default=0)
    fiber_per_100g = fields.Float(validate=validate.Range(min=0), load_default=0)
    sugar_per_100g = fields.Float(validate=validate.Range(min=0), load_default=0)
    default_serving_g = fields.Float(validate=validate.Range(min=0.1), load_default=100)
    serving_unit = fields.String(validate=validate.Length(max=20), load_default="g")
    serving_description = fields.String(validate=validate.Length(max=100))
    tags = fields.List(fields.String())


class FoodItemUpdateSchema(FoodItemSchema):
    name = fields.String(validate=validate.Length(min=1, max=200))
    calories_per_100g = fields.Float(validate=validate.Range(min=0))


food_item_schema = FoodItemSchema()
food_item_update_schema = FoodItemUpdateSchema()
