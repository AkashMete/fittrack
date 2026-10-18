"""Marshmallow input validation — reject bad data at the boundary."""
from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=128))
    first_name = fields.String(validate=validate.Length(max=50))
    last_name = fields.String(validate=validate.Length(max=50))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class PasswordChangeSchema(Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8, max=128))


register_schema = RegisterSchema()
login_schema = LoginSchema()
password_change_schema = PasswordChangeSchema()
