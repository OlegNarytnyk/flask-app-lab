import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import config_by_name

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.environ.get("FLASK_CONFIG", "development")
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/posts")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app