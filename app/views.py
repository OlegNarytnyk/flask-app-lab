from flask import render_template, redirect, url_for, flash
from app.forms import ContactForm
from app.utils_logger import logger
from . import app


@app.route("/")
def index():
    return render_template("resume.html", page_title="Резюме")


@app.route("/resume")
def resume():
    return render_template("resume.html", page_title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            logger.info(
                "Contact form: name=%s email=%s phone=%s subject=%s message=%s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data,
            )
            flash(f"Повідомлення відправлено і записано: {form.name.data} ({form.email.data})", "success")
        except Exception:
            flash("Помилка запису повідомлення у log-файл.", "danger")

        return redirect(url_for("contacts"))

    if form.is_submitted() and not form.validate():
        flash("Форма містить помилки. Перевірте поля.", "warning")
        return redirect(url_for("contacts"))

    return render_template("contacts.html", page_title="Контакти", form=form)