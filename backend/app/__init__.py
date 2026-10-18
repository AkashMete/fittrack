"""Application factory (ARCHITECTURE.md middleware chain: CORS → limiter → JWT → validation → routes)."""
import mongoengine

from flask import Flask

from .config import get_config
from .extensions import cors, jwt, limiter


def _connect_db(app: Flask) -> None:
    uri = app.config["MONGODB_URI"]
    if uri.startswith("mongomock://"):
        import mongomock

        mongoengine.connect(
            "fittrack_test",
            mongo_client_class=mongomock.MongoClient,
            uuidRepresentation="standard",
        )
    else:
        mongoengine.connect(host=uri, uuidRepresentation="standard")


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    _connect_db(app)

    jwt.init_app(app)
    limiter.init_app(app)
    cors.init_app(
        app,
        origins=app.config["CORS_ORIGINS"],
        supports_credentials=True,  # required for the httpOnly refresh cookie
    )

    from .common.errors import register_error_handlers
    from .common.jwt_callbacks import register_jwt_callbacks

    register_jwt_callbacks(jwt)
    register_error_handlers(app)

    from .api.v1 import blueprint as api_v1

    app.register_blueprint(api_v1)

    @app.get("/health")
    def health():  # Render.com health check
        return {"status": "success", "data": {"service": "fittrack-api"}}

    return app
