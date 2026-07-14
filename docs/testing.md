# Como testar a NOVA

## 1. Testes automatizados
Execute:

```bash
python3 -m unittest discover -s tests -v
```

## 2. Teste manual do CLI
Execute:

```bash
python3 src/main.py
```

### Cenários recomendados
- Cadastrar um conceito novo.
- Consultar o conceito por palavra-chave.
- Visualizar a memória inteira.
- Criar uma relação entre dois conceitos.
- Confirmar que a relação aparece na lista.

## 3. Exemplo de cadastro rápido
Use os seguintes dados:
- Nome: Python
- Categoria: Programação
- Descrição: Linguagem de programação de alto nível
- Fonte: Manual Python
- Confiança: 0.9

Depois cadastre outro conceito, por exemplo:
- Nome: SQLite
- Categoria: Banco de dados
- Descrição: Banco leve e local
- Fonte: Documentação SQLite
- Confiança: 0.85

E crie uma relação do tipo:
- usa
