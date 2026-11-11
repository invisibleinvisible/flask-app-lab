
import pytest
from decimal import Decimal
from tinydb import TinyDB

from app import app
from app.products import views


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Створення окремої тестової бази TinyDB."""

    db_path = tmp_path / "test_products.json"
    db = TinyDB(str(db_path))
    table = db.table("products")

    monkeypatch.setattr(views, "products_table", table)

    # Окрема папка для тестових зображень
    upload_folder = tmp_path / "uploads"
    upload_folder.mkdir()

    monkeypatch.setattr(
        views,
        "UPLOAD_FOLDER",
        upload_folder
    )

    yield table

    db.close()


@pytest.fixture
def client(test_db):
    """Створення тестового клієнта Flask."""

    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with app.test_client() as client:
        yield client


def sample_product():
    """Тестові дані товару."""

    return {
        "name": "Laptop",
        "content": "Потужний ноутбук для роботи та навчання.",
        "price": "1200.00",
        "category": "electronics",
        "quantity": 5
    }


# CREATE — додавання товару

def test_add_product(client, test_db):
    response = client.post(
        "/product/add",
        data=sample_product(),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert len(test_db.all()) == 1

    product = test_db.all()[0]

    assert product["name"] == "Laptop"
    assert product["price"] == "1200.00"
    assert product["category"] == "electronics"
    assert product["quantity"] == 5
    assert product["id"] == 1
    assert product["created_at"]


# READ — перегляд списку товарів

def test_products_list(client, test_db):
    test_db.insert({
        "id": 1,
        **sample_product(),
        "image": None,
        "created_at": "2026-01-01T12:00:00"
    })

    response = client.get("/product/")

    assert response.status_code == 200
    assert "Laptop" in response.get_data(as_text=True)


# READ — перегляд окремого товару

def test_detail_product(client, test_db):
    test_db.insert({
        "id": 1,
        **sample_product(),
        "image": None,
        "created_at": "2026-01-01T12:00:00"
    })

    response = client.get("/product/1")

    assert response.status_code == 200
    assert "Laptop" in response.get_data(as_text=True)


# READ — товар не знайдено

def test_detail_product_not_found(client):
    response = client.get("/product/999")

    assert response.status_code == 404


# UPDATE — редагування товару

def test_edit_product(client, test_db):
    test_db.insert({
        "id": 1,
        **sample_product(),
        "image": None,
        "created_at": "2026-01-01T12:00:00"
    })

    updated_data = {
        "name": "Gaming PC",
        "content": "Потужний комп'ютер для ігор.",
        "price": "2500.50",
        "category": "computers",
        "quantity": 10
    }

    response = client.post(
        "/product/1/edit",
        data=updated_data,
        follow_redirects=True
    )

    assert response.status_code == 200

    product = test_db.all()[0]

    assert product["name"] == "Gaming PC"
    assert product["price"] == "2500.50"
    assert product["category"] == "computers"
    assert product["quantity"] == 10

    # ID та дата створення не повинні змінюватися
    assert product["id"] == 1
    assert product["created_at"] == "2026-01-01T12:00:00"


# UPDATE — товар не знайдено

def test_edit_product_not_found(client):
    response = client.get("/product/999/edit")

    assert response.status_code == 404


# DELETE — видалення товару

def test_delete_product(client, test_db):
    test_db.insert({
        "id": 1,
        **sample_product(),
        "image": None,
        "created_at": "2026-01-01T12:00:00"
    })

    response = client.post(
        "/product/1/delete",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert len(test_db.all()) == 0


# DELETE — товар не знайдено

def test_delete_product_not_found(client):
    response = client.post("/product/999/delete")

    assert response.status_code == 404


# ВАЛІДАЦІЯ — неправильні дані

def test_add_product_invalid_data(client, test_db):
    invalid_data = {
        "name": "PC",
        "content": "Опис товару",
        "price": "-100",
        "category": "electronics",
        "quantity": -5
    }

    response = client.post(
        "/product/add",
        data=invalid_data
    )

    assert response.status_code == 200
    assert len(test_db.all()) == 0
