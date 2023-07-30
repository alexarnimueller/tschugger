import os
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman


db = SQLAlchemy()
migrate = Migrate()
sess = Session()
csrf = CSRFProtect()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "01a42a64a4057c737f0118e8bfb92126"),
        SQLALCHEMY_DATABASE_URI=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=1800,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_TYPE="redis",
        SESSION_REDIS=redis.from_url(os.environ.get("SESSION_REDIS")),
        RECAPTCHA_PUBLIC_KEY=os.environ.get("RECAPTCHA_PUBLIC_KEY"),
        RECAPTCHA_PRIVATE_KEY=os.environ.get("RECAPTCHA_PRIVATE_KEY"),
    )

    # register the database commands
    db.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)
    csrf.init_app(app)

    # apply the blueprints to the app
    import auth, views, people

    # add rate limit for login atempts
    storage = os.environ.get("LIMITER_REDIS")
    limiter = Limiter(get_remote_address, storage_uri=storage, default_limits=["2/second"], app=app)
    limiter.limit("60/hour")(auth.bp)

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(people.bp)

    app.add_url_rule("/", endpoint="index")

    # configure Talisman to handle CSP
    talisman = Talisman(
        app,
        content_security_policy={
            "default-src": "'self'",
            "img-src": [
                "'self' data:",
                "*.printfriendly.com",
                "*.w.org",
                "*.w3.org",
                "*.gravatar.com",
                "cdn.datatables.net",
                "*.openstreetmap.org",
                "unpkg.com",
            ],
            "script-src": [
                "'self'",
                "*.w.org",
                "*.w3.org",
                "*.gravatar.com",
                "*.gstatic.com",
                "*.google.com",
                "*.googleapis.com",
                "*.googletagmanager.com",
                "*.jsdelivr.net",
                "cdnjs.cloudflare.com",
                "cdn.datatables.net",
                "unpkg.com",
            ],
            "style-src": [
                "'self'",
                "*.googleapis.com",
                "*.bootstrapcdn.com",
                "*.jsdelivr.net",
                "cdnjs.cloudflare.com",
                "cdn.datatables.net",
                "unpkg.com",
            ],
            "font-src": [
                "'self'",
                "*.googleapis.com",
                "*.bootstrapcdn.com",
                "*.gstatic.com",
                "*.jsdelivr.net",
                "cdnjs.cloudflare.com",
                "cdn.datatables.net",
            ],
            "frame-src": [
                "'self'",
                "*.google.com",
            ],
            "connect-src": "*.google-analytics.com",
            "object-src": "'self'",
            "frame-ancestors": "'self'",
            "form-action": "'self'",
        },
        content_security_policy_nonce_in=["script-src", "style-src"],
        feature_policy={"geolocation": "'none'"},
    )

    return app
