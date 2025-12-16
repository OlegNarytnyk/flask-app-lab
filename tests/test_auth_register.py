from app import db
from app.models import User


def test_register_creates_user_in_db(client, app):
    resp = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        follow_redirects=True,
    )

    assert resp.status_code == 200

    with app.app_context():
        u = db.session.query(User).filter_by(email="testuser@example.com").first()
        assert u is not None
        assert u.username == "testuser"
        assert u.password != "secret123"
        assert len(u.password) > 10