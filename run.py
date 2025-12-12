from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET"])
def contacts():
    return render_template("contacts.html", title="Контакти")

from app import app
if __name__ == "__main__":
    app.run(debug=True)