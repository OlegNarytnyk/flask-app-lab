from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum

from app import db


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

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title!r}, category={self.category})>"