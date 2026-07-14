import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app
from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager
from learning.autonomous_learning import AutonomousLearner


class AutonomousLearningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "memory.db"
        self.connection = initialize_database(self.db_path)
        self.manager = KnowledgeManager(self.connection)
        self.input_dir = self.temp_path / "knowledge_input"
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.temp_path / "learning.log"

    def tearDown(self) -> None:
        self.connection.close()
        self.temp_dir.cleanup()

    def test_autonomous_learner_processes_text_file(self) -> None:
        file_path = self.input_dir / "python.txt"
        file_path.write_text("Python is a programming language.", encoding="utf-8")

        learner = AutonomousLearner(
            manager=self.manager,
            input_dir=self.input_dir,
            log_path=self.log_path,
        )
        learned = learner.scan_for_new_files()

        self.assertEqual(1, len(learned))
        self.assertTrue(self.log_path.exists())
        self.assertEqual(1, len(self.manager.list_concepts()))
        self.assertEqual("Python", self.manager.list_concepts()[0]["name"])

    def test_api_endpoints_expose_memory_and_stats(self) -> None:
        client = TestClient(app)

        response = client.get("/knowledge")
        self.assertEqual(200, response.status_code)

        stats_response = client.get("/stats")
        self.assertEqual(200, stats_response.status_code)

        learn_response = client.post(
            "/learn",
            json={
                "name": "SQLite",
                "category": "Banco de dados",
                "description": "Banco local leve",
                "source": "teste",
                "confidence": 0.91,
            },
        )
        self.assertEqual(200, learn_response.status_code)
        self.assertTrue(learn_response.json()["success"])

    def test_learning_endpoint_runs_autonomous_cycle(self) -> None:
        file_path = self.input_dir / "demo.txt"
        file_path.write_text("This is a demo concept.", encoding="utf-8")

        os.environ["NOVA_INPUT_DIR"] = str(self.input_dir)
        os.environ["NOVA_LOG_PATH"] = str(self.log_path)
        os.environ["NOVA_DB_PATH"] = str(self.db_path)

        try:
            client = TestClient(app)
            response = client.post("/learning/run")
        finally:
            os.environ.pop("NOVA_INPUT_DIR", None)
            os.environ.pop("NOVA_LOG_PATH", None)
            os.environ.pop("NOVA_DB_PATH", None)

        self.assertEqual(200, response.status_code)
        self.assertGreaterEqual(response.json()["processed_count"], 1)
