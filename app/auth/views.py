from .forms import RegistrationForm

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db, bcrypt
from app.models import User
from . import auth_bp
from .forms import LoginForm

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

@auth_bp.route("/account")
@login_required
def account():
    return render_template("auth/account.html", user=current_user, page_title="Account")

@auth_bp.route("/users")
@login_required
def users_list():
    users = db.session.query(User).order_by(User.id).all()
    return render_template("auth/users_list.html", users=users, page_title="Users")