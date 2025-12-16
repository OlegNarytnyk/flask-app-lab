from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app import bcrypt
from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
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