# N.O.V.A.-A.I.
Uma inteligência artificial experimental focada em aprendizado, memória artificial, aquisição de conhecimento e evolução cognitiva.

## Visão geral
A NOVA é um projeto experimental para estudar como um sistema pode aprender, armazenar e recuperar conhecimento de forma estruturada. Nesta versão, ela já possui:

- memória persistente em SQLite
- conceitos e relações entre conceitos
- respostas contextuais simples
- interface web visual com FastAPI
- interface terminal de apoio

## Versão atual
NOVA v0.1 — Artificial Memory System

## Objetivo desta versão
Criar uma NOVA com memória artificial persistente, respostas baseadas em contexto e uma interface web visual para ensinar, consultar e organizar conhecimento de forma mais humana.

## Arquitetura atual
- Banco de conhecimento em SQLite para persistência local.
- Módulo de conexão e inicialização em src/memory/database.py.
- Módulo de gestão de conceitos, relações e respostas contextuais em src/memory/knowledge.py.
- Backend web com FastAPI em web/app.py.
- Interface visual em HTML, CSS e JavaScript puro em web/templates e web/static.

## Como executar
### Interface web
Instale as dependências:
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

Inicie o servidor:
```bash
python3 -m uvicorn web.app:app --reload --host 0.0.0.0 --port 8000
```

Abra no navegador:
```text
http://127.0.0.1:8000/
```

### Interface terminal
```bash
python3 src/main.py
```

## Como testar
### Testes automatizados
```bash
python3 -m unittest discover -s tests -v
```

### Fluxo manual da interface web
1. Acesse a página inicial.
2. Pergunte algo como "O que é Python?".
3. Ensine um novo conceito no formulário.
4. Veja a memória atual sendo atualizada.

### Exemplo rápido de conhecimento
- Nome: Python
- Categoria: Programação
- Descrição: Linguagem de programação de alto nível
- Fonte: Manual Python
- Confiança: 0.9

## Estrutura do projeto
```text
src/
  main.py
  memory/
    database.py
    knowledge.py
web/
  app.py
  templates/
    index.html
  static/
    style.css
    script.js
tests/
  test_memory.py
  test_main_cli.py
  test_reasoning.py
  test_web_api.py
```

## Próximo passo
A próxima evolução da NOVA pode incluir inferência automática de relações, memória episódica e respostas ainda mais naturais, mantendo tudo local e sem dependência de APIs externas.
