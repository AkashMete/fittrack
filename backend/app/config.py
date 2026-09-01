"""Environment-based configuration (ARCHITECTURE.md: Development / Testing / Production)."""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # Spec 1.2: access 15 min, refresh 30 days
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Access token travels in the Authorization header; the refresh token also
    # rides an httpOnly cookie so the SPA can restore a session after reload
    # without persisting anything readable by JavaScript (XSS defence).
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_REFRESH_COOKIE_PATH = "/api/v1/auth"
    JWT_COOKIE_SAMESITE = "Lax"   # blocks cross-site POSTs from sending the cookie
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False  # SameSite=Lax covers the refresh-cookie CSRF case here

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/fittrack_dev")

    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_ENABLED = True

    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")]

    # Let flask-jwt-extended / our handlers see exceptions instead of flask-restx swallowing them
    PROPAGATE_EXCEPTIONS = True

    RESTX_MASK_SWAGGER = False
    ERROR_404_HELP = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    RATELIMIT_ENABLED = False
    MONGODB_URI = "mongomock://localhost/fittrack_test"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(BaseConfig):
    DEBUG = False
    JWT_COOKIE_SECURE = True      # HTTPS only
    JWT_COOKIE_SAMESITE = "None"  # frontend (Vercel) and API (Render) are cross-site


def get_config(name: str | None = None):
    name = name or os.getenv("FLASK_ENV", "development")
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(name, DevelopmentConfig)
