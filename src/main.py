from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager
from web.app import app as web_app

app = web_app


class NovaCli:
    """Interface visual em terminal para a NOVA v0.1."""

    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else None
        self.connection = initialize_database(self.db_path)
        self.manager = KnowledgeManager(self.connection)

    def run(self) -> None:
        self._print_banner()
        while True:
            self._print_menu()
            choice = input("Escolha uma opção: ").strip()

            if choice == "1":
                self._teach_knowledge()
            elif choice == "2":
                self._consult_knowledge()
            elif choice == "3":
                self._show_memory()
            elif choice == "4":
                self._show_relationships()
            elif choice == "5":
                self._create_relationship()
            elif choice == "0":
                self._print_goodbye()
                break
            else:
                self._print_error("Opção inválida. Tente novamente.")

    def _print_menu(self) -> None:
        print("\n┌─ NOVA MENU ───────────────────────────┐")
        print("│ 1 - Ensinar conhecimento            │")
        print("│ 2 - Consultar conhecimento          │")
        print("│ 3 - Mostrar memória                 │")
        print("│ 4 - Mostrar relações                │")
        print("│ 5 - Criar relação                   │")
        print("│ 0 - Sair                            │")
        print("└────────────────────────────────────┘")

    def _print_banner(self) -> None:
        print("\n╔══════════════════════════════════════╗")
        print("║          NOVA v0.1                   ║")
        print("║     Artificial Memory System        ║")
        print("║  Memória local e conhecimento       ║")
        print("║         persistente                 ║")
        print("╚══════════════════════════════════════╝")

    def _print_goodbye(self) -> None:
        print("\nAté logo! A NOVA guarda sua memória localmente.")

    def _print_error(self, message: str) -> None:
        print(f"\n[ERRO] {message}")

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
            print(f"\n✓ Conhecimento ensinado com sucesso. ID: {concept_id}")
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
                print("\n╭─ Conceito ─────────────────────────╮")
                print(f"│ Nome: {concept['name']:<24}│")
                print(f"│ Categoria: {concept['category']:<18}│")
                print(f"│ Descrição: {concept['description'][:24]:<20}│")
                print(f"│ Fonte: {concept['source'][:24]:<24}│")
                print(f"│ Confiança: {concept['confidence']:<20}│")
                print(f"│ Criado em: {concept['created_at']:<20}│")
                print("╰──────────────────────────────────╯")
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
                print(f"[{concept['id']}] {concept['name']} | {concept['category']} | confiança {concept['confidence']}")
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")

    def _show_relationships(self) -> None:
        try:
            relationships = self.manager.list_relationships()
            if not relationships:
                print("Ainda não há relações registradas.")
                return
            print("Relações da NOVA:")
            for relationship in relationships:
                print(
                    f"[{relationship['id']}] {relationship['source_name']} {relationship['relation_type']} {relationship['target_name']}"
                )
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")

    def _create_relationship(self) -> None:
        try:
            source_name = input("Conceito origem: ").strip()
            target_name = input("Conceito destino: ").strip()
            relation_type = input("Tipo de relação (ex.: usa, pertence, depende): ").strip()
            relationship_id = self.manager.add_relationship(
                source_name=source_name,
                target_name=target_name,
                relation_type=relation_type,
            )
            print(f"\n✓ Relação criada com sucesso. ID: {relationship_id}")
        except ValueError as error:
            print(f"Erro de validação: {error}")
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
        except Exception as error:  # pragma: no cover - proteção básica
            print(f"Erro inesperado: {error}")


if __name__ == "__main__":
    NovaCli().run()
