import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_status_code(self):
        """
        Сторінка зі списком продуктів повинна відкриватися (HTTP 200).
        Якщо у тебе роут всередині blueprint'а виглядає як @products_bp.route("/")
        і зареєстрований з url_prefix="/products", тоді URL /products/
        """
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

    def test_products_list_contains_products(self):
        """
        Перевіряємо, що в HTML є назви наших товарів.
        """
        response = self.client.get("/products/")
        html = response.data.decode("utf-8")

        self.assertIn("USB-C Charger", html)
        self.assertIn("Mechanical Keyboard", html)
        self.assertIn("Gaming Mouse", html)


if __name__ == "__main__":
    unittest.main()