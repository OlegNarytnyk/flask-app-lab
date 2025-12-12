from flask import render_template, request, redirect, url_for, flash, session
from . import users_bp

VALID_USERNAME = "oleg"
VALID_PASSWORD = "1234"

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            flash("Успішний вхід", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", page_title="Login")


@users_bp.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    return render_template("users/profile.html", page_title="Profile", user=user)


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("users.login"))