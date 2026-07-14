from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager


class NovaCli:
    """Interface simples em terminal para a NOVA v0.1."""

    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else None
        self.connection = initialize_database(self.db_path)
        self.manager = KnowledgeManager(self.connection)

    def run(self) -> None:
        self._print_banner()
        while True:
            print("\nDigite:")
            print("1 - Ensinar conhecimento")
            print("2 - Consultar conhecimento")
            print("3 - Mostrar memória")
            print("0 - Sair")
            choice = input("Escolha uma opção: ").strip()

            if choice == "1":
                self._teach_knowledge()
            elif choice == "2":
                self._consult_knowledge()
            elif choice == "3":
                self._show_memory()
            elif choice == "0":
                print("Encerrando NOVA...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def _print_banner(self) -> None:
        print("=" * 40)
        print("NOVA v0.1")
        print("Artificial Memory System")
        print("Memória local e conhecimento persistente")
        print("=" * 40)

    def _teach_knowledge(self) -> None:
        try:
            name = input("Nome do conceito: ").strip()
            category = input("Categoria: ").strip()
            description = input("Descrição: ").strip()
            source = input("Fonte: ").strip()
            confidence_input = input("Nível de confiança (0.0 a 1.0): ").strip()
            confidence = float(confidence_input)
            concept_id = self.manager.add_concept(
                name=name,
                category=category,
                description=description,
                source=source,
                confidence=confidence,
            )
            print(f"Conhecimento ensinado com sucesso. ID: {concept_id}")
            print("A informação foi salva na memória da NOVA.")
        except ValueError as error:
            print(f"Erro de validação: {error}")
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")

    def _consult_knowledge(self) -> None:
        try:
            query = input("Digite o termo para consultar: ").strip()
            if not query:
                print("Consulta vazia.")
                return
            results = self.manager.search_concepts(query)
            if not results:
                print("Nenhum conceito encontrado.")
                return
            for concept in results:
                print("-" * 30)
                print(f"Nome: {concept['name']}")
                print(f"Categoria: {concept['category']}")
                print(f"Descrição: {concept['description']}")
                print(f"Fonte: {concept['source']}")
                print(f"Confiança: {concept['confidence']}")
                print(f"Criado em: {concept['created_at']}")
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")

    def _show_memory(self) -> None:
        try:
            concepts = self.manager.list_concepts()
            if not concepts:
                print("A memória da NOVA está vazia.")
                return
            print("Memória da NOVA:")
            print("-" * 40)
            for concept in concepts:
                print(f"[{concept['id']}] {concept['name']} | {concept['category']} | {concept['confidence']}")
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")


if __name__ == "__main__":
    NovaCli().run()
