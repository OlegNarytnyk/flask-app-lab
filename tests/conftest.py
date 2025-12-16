import os
import tempfile
import pytest

from app import create_app, db


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="test-secret-key",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()