import unittest

from src.memory.knowledge import KnowledgeManager
from src.memory.database import initialize_database


class ReasoningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = initialize_database(':memory:')
        self.manager = KnowledgeManager(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_reasoning_can_build_contextual_answer(self) -> None:
        self.manager.add_concept(
            name='Python',
            category='Programação',
            description='Linguagem de programação de alto nível.',
            source='Manual Python',
            confidence=0.9,
        )
        self.manager.add_concept(
            name='SQLite',
            category='Banco de dados',
            description='Banco leve e local.',
            source='Documentação SQLite',
            confidence=0.85,
        )
        self.manager.add_relationship(source_name='Python', target_name='SQLite', relation_type='usa')

        answer = self.manager.build_contextual_answer('O que é Python?')
        self.assertIn('Python', answer)
        self.assertIn('Programação', answer)


if __name__ == '__main__':
    unittest.main()
