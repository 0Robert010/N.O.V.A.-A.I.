# N.O.V.A.-A.I.
Uma inteligência artificial experimental focada em aprendizado, memória artificial, aquisição de conhecimento e evolução cognitiva.

## Versão atual
NOVA v0.1 — Artificial Memory System

## Objetivo desta versão
Criar o primeiro sistema de memória artificial da NOVA, com armazenamento local em SQLite, relações entre conceitos e uma interface visual em terminal para ensinar, consultar e organizar conhecimento.

## Arquitetura atual
- Banco de conhecimento em SQLite para persistência local.
- Módulo de conexão e inicialização em src/memory/database.py.
- Módulo de gestão de conceitos e relações em src/memory/knowledge.py.
- Interface visual em terminal em src/main.py.

## Como executar
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
A próxima evolução da NOVA pode incluir inferência automática de relações entre conceitos, maior peso semântico nas ligações e uma camada de memória contextual.
