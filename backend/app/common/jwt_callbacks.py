"""JWT lifecycle callbacks: blocklist check + consistent 401 envelopes."""
from ..models.token_blocklist import TokenBlocklist


def register_jwt_callbacks(jwt):
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
        return TokenBlocklist.objects(jti=jwt_payload["jti"]).first() is not None

    def _unauthorized(message):
        return {
            "status": "error",
            "error": {"code": "UNAUTHORIZED", "message": message},
        }, 401

    @jwt.unauthorized_loader
    def missing_token(reason):
        return _unauthorized("Missing or invalid authentication token")

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return _unauthorized("Missing or invalid authentication token")

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return _unauthorized("Token has expired")

    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        return _unauthorized("Token has been revoked")
