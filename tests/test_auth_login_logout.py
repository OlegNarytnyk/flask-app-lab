from app import db
from app.models import User


def create_user(app, username="u1", email="u1@example.com", password_plain="pass123"):
    with app.app_context():
        u = User(username=username, email=email, password="temp")
        # якщо у тебе є метод set_password
        if hasattr(u, "set_password"):
            u.set_password(password_plain)
        else:
            # якщо ти хешуєш в іншому місці — тоді треба вставити вже хеш.
            # Але в твоїй лабі зазвичай є set_password(), тому сюди не дійде.
            u.password = password_plain

        db.session.add(u)
        db.session.commit()
        return u.id


def test_login_logout_flow(client, app):
    create_user(app, email="login@example.com", password_plain="secret123")

    # LOGIN
    resp = client.post(
        "/login",
        data={
            "email": "login@example.com",
            "password": "secret123",
            "remember_me": "y",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200


    assert b"Logout" in resp.data or b"Account" in resp.data

    # LOGOUT
    resp2 = client.get("/logout", follow_redirects=True)
    assert resp2.status_code == 200

    assert b"Login" in resp2.data or b"You have successfully logged out" in resp2.data