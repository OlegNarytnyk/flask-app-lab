from flask import render_template
from . import products_bp


@products_bp.route("/")
def list_products():
    products = [
        {"name": "USB-C Charger", "price": 29.99},
        {"name": "Mechanical Keyboard", "price": 89.99},
        {"name": "Gaming Mouse", "price": 49.99},
    ]
    return render_template("products/products.html", products=products)