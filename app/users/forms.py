from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username / Email", validators=[DataRequired(message="Це поле обов'язкове")])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Це поле обов'язкове"),
            Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів"),
        ],
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")