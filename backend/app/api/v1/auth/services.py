"""Auth business logic — bcrypt hashing, JWT issuing, blocklisting. No HTTP in here."""
from datetime import datetime

import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

from ....common.errors import ConflictError, NotFoundError, UnauthorizedError
from ....models import TokenBlocklist, User

BCRYPT_ROUNDS = 12  # each +1 doubles hashing time — brute-force defence


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def register_user(data: dict) -> User:
    if User.objects(email=data["email"].lower()).first():
        raise ConflictError("An account with this email already exists")
    user = User(
        email=data["email"].lower(),
        password_hash=hash_password(data["password"]),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
    )
    user.save()
    return user


def login_user(email: str, password: str) -> tuple[User, str, str]:
    user = User.objects(email=email.lower()).first()
    # Same generic message for both cases — don't reveal which emails exist
    if not user or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    if not user.is_active:
        raise UnauthorizedError("This account has been deactivated")

    user.update(last_login=datetime.utcnow())
    return user, *issue_tokens(user)


def issue_tokens(user: User) -> tuple[str, str]:
    identity = str(user.id)
    return create_access_token(identity=identity), create_refresh_token(identity=identity)


def refresh_access_token(user_id: str) -> str:
    user = User.objects(id=user_id).first()
    if not user or not user.is_active:
        raise UnauthorizedError("User no longer exists or is inactive")
    return create_access_token(identity=user_id)


def revoke_token(jwt_payload: dict) -> None:
    from bson import ObjectId

    sub = jwt_payload.get("sub")
    TokenBlocklist(
        jti=jwt_payload["jti"],
        token_type=jwt_payload.get("type", "refresh"),
        user=ObjectId(sub) if sub else None,
        expires_at=datetime.utcfromtimestamp(jwt_payload["exp"]),
    ).save()


def change_password(user: User, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.password_hash):
        raise UnauthorizedError("Current password is incorrect")
    user.update(password_hash=hash_password(new_password), updated_at=datetime.utcnow())


def get_user_or_401(user_id: str) -> User:
    user = User.objects(id=user_id).first()
    if not user:
        raise NotFoundError("User not found")
    return user
