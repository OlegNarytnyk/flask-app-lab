from .forms import RegistrationForm
from flask_login import login_user, logout_user

from app import bcrypt
from .forms import LoginForm
import os, secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required

from app import db
from app.models import User
from . import auth_bp
from .forms import UpdateAccountForm
from datetime import datetime, timezone
from flask_login import current_user
from .forms import ChangePasswordForm
from app import bcrypt

@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))

        current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        db.session.commit()
        flash("Password updated successfully.", "success")
        return redirect(url_for("auth.account"))

    return render_template("auth/change_password.html", form=form, page_title="Change Password")

@auth_bp.before_app_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    filename = random_hex + ext.lower()

    save_path = os.path.join(current_app.root_path, "static", "profile_pics", filename)

    img = Image.open(form_picture)
    img.thumbnail((128, 128))
    img.save(save_path)

    return filename

@auth_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("auth.account"))

    return render_template("auth/account.html", user=current_user, form=form, page_title="Account")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password="")
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.register"))

    return render_template("auth/register.html", form=form, page_title="Register")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash("You logged in successfully!", "success")

            next_url = request.args.get("next")
            return redirect(next_url or url_for("auth.account"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form, page_title="Login")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/users")
@login_required
def users_list():
    users = db.session.query(User).order_by(User.id).all()
    return render_template("auth/users_list.html", users=users, page_title="Users")