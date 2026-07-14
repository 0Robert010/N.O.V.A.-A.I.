# N.O.V.A.-A.I.
Uma inteligência artificial experimental focada em aprendizado, memória artificial, aquisição de conhecimento e evolução cognitiva.

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

## Como executar a interface web
Instale as dependências:
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

Depois inicie o servidor:
```bash
python3 -m uvicorn web.app:app --reload --host 0.0.0.0 --port 8000
```

Depois abra o navegador em:
```text
http://127.0.0.1:8000/
```

## Como executar o terminal antigo
```bash
python3 src/main.py
```

## Como testar
### Testes automatizados
```bash
python3 -m unittest discover -s tests -v
```

### Fluxo manual no terminal
1. Execute o programa.
2. Escolha a opção 1 para ensinar um conceito.
3. Escolha a opção 2 para consultar por palavra-chave.
4. Escolha a opção 3 para visualizar os conceitos salvos.
5. Escolha a opção 4 para ver relações entre conceitos.
6. Escolha a opção 5 para criar uma nova relação.

### Exemplo rápido
- Nome: Python
- Categoria: Programação
- Descrição: Linguagem de programação de alto nível
- Fonte: Manual Python
- Confiança: 0.9

## Próximo passo
A próxima evolução da NOVA pode incluir inferência automática de relações, memória episódica e respostas ainda mais naturais, mantendo tudo local e sem dependência de APIs externas.
