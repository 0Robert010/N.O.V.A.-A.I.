import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from web.app import app


class WebApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_home_page_is_available(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_can_query_memory(self) -> None:
        response = self.client.post(
            "/ask",
            json={"question": "O que é Python?"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", response.json())


if __name__ == "__main__":
    unittest.main()
