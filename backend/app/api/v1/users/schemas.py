from marshmallow import Schema, fields, validate


class UpdateProfileSchema(Schema):
    first_name = fields.String(validate=validate.Length(max=50))
    last_name = fields.String(validate=validate.Length(max=50))
    date_of_birth = fields.Date()
    gender = fields.String(validate=validate.OneOf(["male", "female", "other", "prefer_not_to_say"]))
    height_cm = fields.Float(validate=validate.Range(min=0))
    units = fields.String(validate=validate.OneOf(["metric", "imperial"]))
    timezone = fields.String(validate=validate.Length(max=50))
    daily_calorie_target = fields.Integer(validate=validate.Range(min=0))
    daily_protein_target_g = fields.Integer(validate=validate.Range(min=0))
    daily_carbs_target_g = fields.Integer(validate=validate.Range(min=0))
    daily_fat_target_g = fields.Integer(validate=validate.Range(min=0))
    daily_water_target_ml = fields.Integer(validate=validate.Range(min=0))
    weekly_workout_target = fields.Integer(validate=validate.Range(min=0))


update_profile_schema = UpdateProfileSchema()
