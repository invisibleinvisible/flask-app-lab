from flask import render_template, abort
from . import products_bp

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Потужний ноутбук для роботи та навчання."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Сучасний смартфон із якісною камерою."
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп'ютер для роботи та ігор."
    }
]


@products_bp.route("/")
def products_list():
    return render_template(
        "products/products.html",
        products=products
    )


@products_bp.route("/<int:id>")
def detail_product(id):
    product = next(
        (item for item in products if item["id"] == id),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        product=product
    )