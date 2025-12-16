import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from .config import config_by_name

class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_name=None):
    flask_app = Flask(__name__)   # <-- НЕ app

    config_name = config_name or os.environ.get("FLASK_CONFIG", "development")
    flask_app.config.from_object(config_by_name[config_name])

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)

    # імпорт моделей після init_app
    import app.models  # noqa
    import app.posts.models  # noqa
    import app.products.models  # noqa

    from app.posts import post_bp
    flask_app.register_blueprint(post_bp, url_prefix="/posts")

    from app.products import products_bp
    flask_app.register_blueprint(products_bp, url_prefix="/products")

    from app.auth import auth_bp
    flask_app.register_blueprint(auth_bp, url_prefix="/auth")

    @flask_app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return flask_app