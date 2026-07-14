import tempfile
import unittest
from pathlib import Path

from src.memory.database import connect_database, initialize_database
from src.memory.knowledge import KnowledgeManager


class MemorySystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_nova.db"
        self.connection = connect_database(self.db_path)
        initialize_database(self.db_path, self.connection)
        self.manager = KnowledgeManager(self.connection)

    def tearDown(self) -> None:
        self.connection.close()
        self.temp_dir.cleanup()

    def test_database_initializes_required_tables(self) -> None:
        cursor = self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge'"
        )
        self.assertEqual(cursor.fetchone()[0], "knowledge")

    def test_knowledge_manager_can_add_and_search_concepts(self) -> None:
        concept_id = self.manager.add_concept(
            name="Python",
            category="Programação",
            description="Linguagem de programação de alto nível.",
            source="Manual Python",
            confidence=0.9,
        )

        self.assertIsNotNone(concept_id)

        stored_concept = self.manager.get_concept_by_name("Python")
        self.assertEqual(stored_concept["category"], "Programação")
        self.assertAlmostEqual(stored_concept["confidence"], 0.9)

        results = self.manager.search_concepts("program")
        self.assertTrue(any(item["name"] == "Python" for item in results))

        all_concepts = self.manager.list_concepts()
        self.assertEqual(len(all_concepts), 1)


if __name__ == "__main__":
    unittest.main()
