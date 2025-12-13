# app/__init__.py
from flask import Flask, render_template
from .config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app