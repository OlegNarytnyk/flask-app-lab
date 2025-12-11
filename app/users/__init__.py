from flask import Blueprint

# створюємо Blueprint з префіксом /users
users_bp = Blueprint(
    'users',              # ім'я blueprint-а (для url_for: 'users.greetings')
    __name__,
    url_prefix='/users',  # усі маршрути будуть починатися з /users
    template_folder='templates'
)

from . import views  # імпортуємо маршрути, щоб вони зареєструвалися