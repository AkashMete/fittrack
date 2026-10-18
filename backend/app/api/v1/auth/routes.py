"""Auth routes — thin: parse input → call service → return envelope."""
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, set_refresh_cookies, unset_jwt_cookies
from flask_restx import Namespace, Resource, fields

from ....common.responses import success
from ....extensions import limiter
from . import services
from .schemas import login_schema, password_change_schema, register_schema

auth_ns = Namespace("auth", description="Authentication operations")

register_model = auth_ns.model("Register", {
    "email": fields.String(required=True, example="me@example.com"),
    "password": fields.String(required=True, example="s3cretPass!"),
    "first_name": fields.String,
    "last_name": fields.String,
})

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

password_change_model = auth_ns.model("PasswordChange", {
    "current_password": fields.String(required=True),
    "new_password": fields.String(required=True),
})


def _token_response(user, access_token, refresh_token, status_code=200):
    body, _ = success({
        "user": user.to_dict(),
        "access_token": access_token,
        # Also returned in the body for Postman/mobile clients; the SPA relies
        # on the httpOnly cookie set below and never persists this value.
        "refresh_token": refresh_token,
    }, status_code=status_code)
    response = make_response(jsonify(body), status_code)
    set_refresh_cookies(response, refresh_token)
    return response


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, "User created")
    @auth_ns.response(409, "Email already registered")
    def post(self):
        """Register a new account"""
        data = register_schema.load(auth_ns.payload or {})
        user = services.register_user(data)
        access_token, refresh_token = services.issue_tokens(user)
        return _token_response(user, access_token, refresh_token, 201)


@auth_ns.route("/login")
class Login(Resource):
    # Spec: max 5 attempts/minute — brute-force defence
    decorators = [limiter.limit("5 per minute", methods=["POST"])]

    @auth_ns.expect(login_model)
    @auth_ns.response(200, "Logged in")
    @auth_ns.response(401, "Invalid credentials")
    def post(self):
        """Login → access token (15 min) + refresh token (30 days)"""
        data = login_schema.load(auth_ns.payload or {})
        user, access_token, refresh_token = services.login_user(data["email"], data["password"])
        return _token_response(user, access_token, refresh_token)


@auth_ns.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(200, "New access token")
    def post(self):
        """Exchange refresh token (cookie or Bearer) for a new access token"""
        return success({"access_token": services.refresh_access_token(get_jwt_identity())})


@auth_ns.route("/logout")
class Logout(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(200, "Logged out")
    def post(self):
        """Blacklist the refresh token and clear the cookie"""
        services.revoke_token(get_jwt())
        body, _ = success({"message": "Logged out"})
        response = make_response(jsonify(body), 200)
        unset_jwt_cookies(response)
        return response


@auth_ns.route("/password/change")
class PasswordChange(Resource):
    @jwt_required()
    @auth_ns.expect(password_change_model)
    @auth_ns.response(200, "Password updated")
    @auth_ns.response(401, "Current password incorrect")
    def post(self):
        """Change password (requires the current password)"""
        data = password_change_schema.load(auth_ns.payload or {})
        user = services.get_user_or_401(get_jwt_identity())
        services.change_password(user, data["current_password"], data["new_password"])
        return success({"message": "Password updated"})
