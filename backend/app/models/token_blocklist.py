from datetime import datetime

from mongoengine import DateTimeField, Document, ReferenceField, StringField


class TokenBlocklist(Document):
    """Revoked JWT ids (jti). TTL index purges rows once the token would have expired anyway."""

    jti = StringField(required=True, unique=True)
    token_type = StringField(choices=["access", "refresh"])
    user = ReferenceField("User")
    created_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField()

    meta = {
        "collection": "token_blocklist",
        "indexes": [
            "jti",
            {"fields": ["expires_at"], "expireAfterSeconds": 0},
        ],
    }
