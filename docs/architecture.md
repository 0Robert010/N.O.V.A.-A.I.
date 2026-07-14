# Arquitetura da NOVA v0.1

A arquitetura atual da NOVA separa responsabilidades para manter o sistema simples, extensível e fácil de evoluir:

- Camada de persistência: responsável pelo banco SQLite e pela criação das tabelas.
- Camada de conhecimento: responsável por inserir, buscar, listar conceitos e registrar relações entre eles.
- Camada de interface: responsável por capturar comandos do usuário e apresentar os resultados em um menu visual de terminal.

## Estruturas principais
- Tabela knowledge: armazena conceitos com nome, categoria, descrição, fonte, confiança e data de criação.
- Tabela relationships: armazena relações entre conceitos, como "usa", "pertence" ou "depende".

## Fluxo principal
1. O programa inicia a conexão com o banco SQLite.
2. O banco é inicializado com as tabelas knowledge e relationships.
3. O usuário pode ensinar novos conceitos, consultar conceitos existentes, listar a memória, visualizar relações e criar novas relações.
4. Os dados ficam persistidos localmente em um arquivo SQLite.

## Próxima evolução planejada
- Inferência automática de relações.
- Memória contextual.
- Reforço de confiança em ligações entre conceitos.
