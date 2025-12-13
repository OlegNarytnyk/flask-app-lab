from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import users_bp
from .forms import LoginForm

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
    form = LoginForm()

    if form.validate_on_submit():
        username = (form.username.data or "").strip()
        password = form.password.data or ""
        remember = bool(form.remember.data)

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            session["remember"] = remember
            flash("Успішний вхід", "success")
            flash(f"Remember: {'ON' if remember else 'OFF'}", "info")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль", "danger")

    elif request.method == "POST":
        flash("Перевірте форму. Є помилки у полях.", "danger")

    return render_template("users/login.html", page_title="Login", form=form)

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("Спочатку увійдіть у систему.", "danger")
        return redirect(url_for("users.login"))

    username = session["user"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_cookie":
            key = (request.form.get("cookie_key") or "").strip()
            value = (request.form.get("cookie_value") or "").strip()
            max_age_raw = (request.form.get("cookie_max_age") or "").strip()

            if not key:
                flash("Ключ cookie не може бути порожнім.", "warning")
                return redirect(url_for("users.profile"))

            max_age = None
            if max_age_raw:
                try:
                    max_age = int(max_age_raw)
                    if max_age <= 0:
                        max_age = None
                except ValueError:
                    flash("Термін дії (сек) має бути числом.", "warning")
                    return redirect(url_for("users.profile"))

            resp = make_response(redirect(url_for("users.profile")))
            resp.set_cookie(key, value, max_age=max_age)
            flash(f"Cookie '{key}' додано/оновлено.", "success")
            return resp

        if action == "delete_cookie":
            key = (request.form.get("delete_key") or "").strip()
            if not key:
                flash("Вкажіть ключ cookie для видалення.", "warning")
                return redirect(url_for("users.profile"))

            resp = make_response(redirect(url_for("users.profile")))
            resp.delete_cookie(key)
            flash(f"Cookie '{key}' видалено.", "success")
            return resp

        if action == "delete_all":
            resp = make_response(redirect(url_for("users.profile")))
            for k in request.cookies.keys():
                resp.delete_cookie(k)
            flash("Усі cookie видалено.", "success")
            return resp

        flash("Невідома дія.", "warning")
        return redirect(url_for("users.profile"))

    cookies = dict(request.cookies)

    theme = request.cookies.get("theme", "light")
    return render_template(
        "users/profile.html",
        page_title="Profile",
        username=username,
        cookies=cookies,
        theme = theme
    )


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/theme/<string:theme>")
def set_theme(theme):
    if theme not in ("light", "dark"):
        flash("Невідома тема.", "warning")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", theme, max_age=60 * 60 * 24 * 30)
    flash(f"Тему змінено на: {theme}", "info")
    return resp