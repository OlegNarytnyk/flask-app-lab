from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Float, Boolean, DateTime, Text, Enum
from datetime import datetime

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String(150), nullable=False)
    content = db.Column(Text, nullable=False)
    posted = db.Column(DateTime, default=datetime.utcnow)
    category = db.Column(
        Enum("news", "publication", "tech", "other", name="post_category"),
        default="other"
    )
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title!r})>"

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )


    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name!r})>"