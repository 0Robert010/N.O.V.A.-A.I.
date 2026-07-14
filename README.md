# N.O.V.A.-A.I.
Uma inteligência artificial experimental focada em aprendizado, memória artificial, aquisição de conhecimento e evolução cognitiva.

## Visão geral
A NOVA é um projeto experimental para estudar como um sistema pode aprender, armazenar e recuperar conhecimento de forma estruturada. Nesta versão, ela já possui:

- memória persistente em SQLite
- conceitos e relações entre conceitos
- respostas contextuais simples
- interface web visual com FastAPI
- interface terminal de apoio
- arquitetura de aprendizado autônomo para v0.2

## Versão atual
NOVA v0.2 — Autonomous Learning Simulation

## Objetivo desta versão
Criar uma NOVA capaz de processar conhecimento automaticamente enquanto está executando, sem depender de APIs externas de IA generativa. O foco é estruturar um ciclo simples de aquisição, registro e observação de conhecimento.

## Arquitetura da NOVA v0.2
- Banco de conhecimento em SQLite para persistência local.
- Módulo de conexão e inicialização em src/memory/database.py.
- Módulo de gestão de conceitos, relações e respostas contextuais em src/memory/knowledge.py.
- API FastAPI em api/main.py com rotas em api/routes/.
- Serviço de aprendizagem em api/services/learner.py.
- Módulo de aprendizado autônomo em learning/autonomous_learning.py.
- Interface visual em web/ com painel de status e diário de aprendizado.

## Como executar
### Instale as dependências
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

### API FastAPI
```bash
python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Interface web
Abra no navegador:
```text
http://127.0.0.1:8000/
```

### Aprendizado autônomo
Crie arquivos .txt dentro da pasta knowledge_input/ e rode o módulo de aprendizado:
```bash
python3 -c "from learning.autonomous_learning import AutonomousLearner; AutonomousLearner().scan_for_new_files()"
```

### Interface terminal
```bash
python3 src/main.py
```

## Como testar
```bash
python3 -m unittest discover -s tests -v
```

## Estrutura do projeto
```text
api/
  main.py
  routes/
    knowledge.py
    learning.py
  services/
    learner.py
learning/
  autonomous_learning.py
src/
  main.py
  memory/
    database.py
    knowledge.py
web/
  index.html
  style.css
  script.js
tests/
  test_memory.py
  test_main_cli.py
  test_reasoning.py
  test_web_api.py
  test_autonomous_learning.py
```

## Fluxo de funcionamento
1. A NOVA verifica arquivos .txt em knowledge_input/.
2. O módulo de aprendizado extrai um nome, categoria e descrição simples.
3. O conhecimento é salvo no banco SQLite.
4. O sistema registra a atividade em logs/learning.log.
5. A API expõe o estado da memória e os dados de estatísticas.
