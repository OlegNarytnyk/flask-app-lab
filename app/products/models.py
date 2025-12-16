from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    # 1 category -> many products
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Category {self.name!r}>"


class Product(db.Model):
    __tablename__ = "products"
    active = db.Column(db.Boolean, nullable=False, default=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    created_at = db.Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    # FK (product -> category)
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True,
    )

    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="products",
    )

    def __repr__(self) -> str:
        return f"<Product {self.name!r} - {self.price}>"