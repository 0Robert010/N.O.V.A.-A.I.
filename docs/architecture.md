# Arquitetura da NOVA v0.1

A arquitetura atual da NOVA separa responsabilidades para manter o sistema simples, extensível e fácil de evoluir:

- Camada de persistência: responsável pelo banco SQLite e pela criação das tabelas.
- Camada de conhecimento: responsável por inserir, buscar, listar conceitos e registrar relações entre eles.
- Camada backend: expõe uma API simples com FastAPI para consulta e aprendizado.
- Camada de resposta: transforma o conteúdo da memória em respostas contextuais simples e naturais.
- Camada frontend: apresenta uma interface web visual em HTML, CSS e JavaScript puro.

## Estruturas principais
- Tabela knowledge: armazena conceitos com nome, categoria, descrição, fonte, confiança e data de criação.
- Tabela relationships: armazena relações entre conceitos, como "usa", "pertence" ou "depende".

## Fluxo principal
1. O backend inicia a conexão com o banco SQLite.
2. O banco é inicializado com as tabelas knowledge e relationships.
3. A interface web envia perguntas e novos conceitos para o backend.
4. O backend consulta a memória SQLite e devolve respostas contextuais, confirmações e a lista atual de conceitos para a interface.
5. Os dados ficam persistidos localmente em um arquivo SQLite.

## Estrutura de pastas
- web/app.py: servidor FastAPI.
- web/templates/index.html: página principal da interface.
- web/static/style.css: estilo futurista da aplicação.
- web/static/script.js: interação do frontend com o backend.

## Próxima evolução planejada
- Inferência automática de relações.
- Memória contextual.
- Reforço de confiança em ligações entre conceitos.
