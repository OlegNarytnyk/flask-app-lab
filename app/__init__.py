import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.environ.get("FLASK_CONFIG", "development")
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"


    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/posts")

    from .products import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app