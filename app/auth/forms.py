from wtforms.validators import EqualTo, Regexp
from wtforms import PasswordField, BooleanField
from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import EqualTo

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Change Password")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

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
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(max=140)])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        user = db.session.query(User).filter(User.email == email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("That email is taken. Please choose a different one.")