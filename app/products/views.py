import uuid
from datetime import datetime
from pathlib import Path
from decimal import Decimal

from tinydb import Query

from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    current_app,
    request
)

from werkzeug.utils import secure_filename

from . import products_bp
from .forms import ProductForm
from .database import products_table

# Шлях до каталогу завантажених зображень
UPLOAD_FOLDER = Path(__file__).resolve().parent / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@products_bp.route("/")
def products_list():
    products = products_table.all()

    return render_template(
        "products/products.html",
        products=products
    )


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = None

            image_file = form.image.data

            if image_file and image_file.filename:
                original_name = secure_filename(image_file.filename)
                extension = Path(original_name).suffix.lower()

                if extension not in (".jpg", ".jpeg", ".png"):
                    flash("Недопустимий формат зображення.", "danger")
                    return redirect(url_for("products.add_product"))

                filename = f"{uuid.uuid4().hex}{extension}"

                image_file.save(UPLOAD_FOLDER / filename)

                image_path = f"uploads/{filename}"

            product = {
                "id": max(
                    (item["id"] for item in products_table.all()),
                    default=0
                ) + 1,
                "name": form.name.data.strip(),
                "content": form.content.data,
                "price": str(form.price.data.quantize(Decimal("0.01"))),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path,
                "created_at": datetime.now().isoformat(timespec="seconds")
            }

            products_table.insert(product)

            flash("Товар успішно додано!", "success")

            return redirect(url_for("products.products_list"))

        except Exception:
            current_app.logger.exception("Помилка додавання товару")
            flash("Не вдалося додати товар.", "danger")
            return redirect(url_for("products.add_product"))

    return render_template(
        "products/add_product.html",
        form=form
    )


@products_bp.route("/<int:id>")
def detail_product(id):
    product = products_table.get(Query().id == id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        product=product
    )


@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = products_table.get(Query().id == id)

    if product is None:
        abort(404)

    form = ProductForm()

    # Заповнюємо форму поточними даними товару
    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(str(product["price"]))
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    if form.validate_on_submit():
        try:
            image_path = product.get("image")

            image_file = form.image.data

            # Якщо користувач завантажив нове зображення
            if image_file and image_file.filename:
                original_name = secure_filename(image_file.filename)
                extension = Path(original_name).suffix.lower()

                if extension not in (".jpg", ".jpeg", ".png"):
                    flash("Недопустимий формат зображення.", "danger")
                    return redirect(
                        url_for("products.edit_product", id=id)
                    )

                filename = f"{uuid.uuid4().hex}{extension}"

                image_file.save(UPLOAD_FOLDER / filename)

                image_path = f"uploads/{filename}"

            # Оновлюємо тільки змінювані поля
            updated_data = {
                "name": form.name.data.strip(),
                "content": form.content.data,
                "price": str(
                    form.price.data.quantize(Decimal("0.01"))
                ),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path
            }

            products_table.update(
                updated_data,
                doc_ids=[product.doc_id]
            )

            # Видаляємо старе зображення, якщо його замінили
            old_image = product.get("image")

            if image_path != old_image and old_image:
                old_file = UPLOAD_FOLDER.parent / old_image

                if old_file.exists():
                    old_file.unlink()

            flash("Товар успішно оновлено!", "success")

            return redirect(
                url_for("products.detail_product", id=id)
            )

        except Exception:
            current_app.logger.exception(
                "Помилка редагування товару"
            )

            flash("Не вдалося оновити товар.", "danger")

            return redirect(
                url_for("products.edit_product", id=id)
            )

    return render_template(
        "products/edit_product.html",
        form=form,
        product=product
    )

