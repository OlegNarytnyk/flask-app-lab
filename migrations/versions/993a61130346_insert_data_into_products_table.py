"""Insert data into products table

Revision ID: 993a61130346
Revises: 5ab6ce53949e
Create Date: 2025-12-15 22:26:36.244512

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '993a61130346'
down_revision = '5ab6ce53949e'
branch_labels = None
depends_on = None


def upgrade():
    categories = table(
        "categories",
        column("id", sa.Integer),
        column("name", sa.String),
    )

    products = table(
        "products",
        column("id", sa.Integer),
        column("name", sa.String),
        column("price", sa.Float),
        column("active", sa.Boolean),
        column("category_id", sa.Integer),
    )

    op.bulk_insert(
        categories,
        [
            {"name": "Electronics"},
            {"name": "Books"},
            {"name": "Clothing"},
        ],
    )

    conn = op.get_bind()

    cat_id = {
        row[0]: row[1]
        for row in conn.execute(sa.text("SELECT name, id FROM categories")).fetchall()
    }

    op.bulk_insert(
        products,
        [
            {"name": "Laptop",      "price": 1200.0, "active": True,  "category_id": cat_id["Electronics"]},
            {"name": "Smartphone",  "price": 800.0,  "active": True,  "category_id": cat_id["Electronics"]},
            {"name": "Novel",       "price": 20.0,   "active": True,  "category_id": cat_id["Books"]},
            {"name": "T-Shirt",     "price": 25.0,   "active": False, "category_id": cat_id["Clothing"]},
        ],
    )


def downgrade():
    op.execute(sa.text("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """))

    op.execute(sa.text("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """))