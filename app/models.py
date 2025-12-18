from app import bcrypt
from app import db, login_manager
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    image: Mapped[str] = mapped_column(String(255), nullable=True, default="profile_default.jpg")
    about_me: Mapped[str | None] = mapped_column(String(140), nullable=True)
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.now(timezone.utc),
    )

    @property
    def is_active(self) -> bool:
        return True

    def set_password(self, raw_password: str) -> None:
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))