# Arquitetura da NOVA v0.1

A arquitetura inicial da NOVA separa claramente responsabilidades para manter o sistema simples e extensível:

- Camada de persistência: responsável pelo banco SQLite e pela criação das tabelas.
- Camada de conhecimento: responsável por inserir, buscar e listar conceitos.
- Camada de interface: responsável por capturar comandos do usuário e apresentar os resultados no terminal.

## Fluxo principal
1. O programa inicia a conexão com o banco SQLite.
2. O banco é inicializado com a tabela knowledge.
3. O usuário pode ensinar novos conceitos, consultar conceitos existentes ou listar a memória.
4. Os dados ficam persistidos localmente em um arquivo SQLite.
