from flask import render_template, redirect, url_for, flash
from . import auth_bp
from .forms import RegistrationForm

from app import db
from app.models import User

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password="")
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.register"))

    return render_template("auth/register.html", form=form, page_title="Register")