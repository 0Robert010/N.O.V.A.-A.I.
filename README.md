# N.O.V.A.-A.I.
Uma inteligência artificial experimental focada em aprendizado, memória artificial, aquisição de conhecimento e evolução cognitiva.

## Versão atual
NOVA v0.1 — Artificial Memory System

## Objetivo desta versão
Criar o primeiro sistema de memória artificial da NOVA, com armazenamento local em SQLite e uma interface simples de terminal para ensinar e consultar conhecimento.

## Arquitetura inicial
- Banco de conhecimento em SQLite para persistência local.
- Módulo de conexão e inicialização em src/memory/database.py.
- Módulo de gestão de conceitos em src/memory/knowledge.py.
- Interface de terminal em src/main.py para interação básica.

## Como executar
```bash
python3 src/main.py
```

## Como testar
```bash
python3 -m unittest discover -s tests -v
```
