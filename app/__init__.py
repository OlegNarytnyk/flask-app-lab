from flask import Flask

app = Flask(__name__)


# імпортуємо звичайні маршрути (резюме, контакти)
from . import views
from .users import users_bp

app.register_blueprint(users_bp, url_prefix="/users")