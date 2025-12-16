from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

from app import db
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=4, max=16),
        Regexp(r"^[A-Za-z][A-Za-z0-9._]*$",
               message="Username must start with a letter and contain only letters, numbers, dots or underscores.")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError("Email is already registered.")

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first():
            raise ValidationError("Username is already taken.")