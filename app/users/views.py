# app/users/views.py
from flask import render_template, request, redirect, url_for
from . import users_bp   # імпортуємо blueprint з __init__.py

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)