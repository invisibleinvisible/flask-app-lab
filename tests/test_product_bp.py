import unittest
from app import app


class ProductBlueprintTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()