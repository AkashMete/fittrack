from marshmallow import Schema, fields, validate

MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack", "pre_workout", "post_workout"]


class DietPlanItemSchema(Schema):
    food_item_id = fields.String(required=True)
    quantity_g = fields.Float(required=True, validate=validate.Range(min=0.1))


class DietPlanMealSchema(Schema):
    meal_type = fields.String(required=True, validate=validate.OneOf(MEAL_TYPES))
    items = fields.List(fields.Nested(DietPlanItemSchema), load_default=[])


class DietPlanSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    meals = fields.List(fields.Nested(DietPlanMealSchema), load_default=[])


class DietPlanUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    meals = fields.List(fields.Nested(DietPlanMealSchema))


class DietLogEntrySchema(Schema):
    food_item_id = fields.String(required=True)
    quantity_g = fields.Float(required=True, validate=validate.Range(min=0.1))
    meal_type = fields.String(required=True, validate=validate.OneOf(MEAL_TYPES))


class DietLogEntryUpdateSchema(Schema):
    quantity_g = fields.Float(validate=validate.Range(min=0.1))
    meal_type = fields.String(validate=validate.OneOf(MEAL_TYPES))


class DietLogNotesSchema(Schema):
    notes = fields.String(validate=validate.Length(max=500))


diet_plan_schema = DietPlanSchema()
diet_plan_update_schema = DietPlanUpdateSchema()
diet_log_entry_schema = DietLogEntrySchema()
diet_log_entry_update_schema = DietLogEntryUpdateSchema()
diet_log_notes_schema = DietLogNotesSchema()
