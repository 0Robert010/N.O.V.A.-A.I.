# N.O.V.A.-A.I.
NOVA é um experimento local de memória artificial, aprendizado estrutural e interface cognitiva sem depender de APIs externas de IA generativa.

## Visão geral
A NOVA v0.2 combina três camadas principais:
- memória persistente local em SQLite
- aprendizado autônomo a partir de arquivos de texto em uma pasta de entrada
- API e interface web para visualizar o estado da memória e acionar o ciclo de aprendizado

## Versão atual
NOVA v0.2 — Autonomous Learning Simulation

## Objetivo desta versão
Criar uma NOVA capaz de processar conhecimento automaticamente enquanto está executando, sem depender de APIs externas. O foco é simular um ciclo simples de aquisição, registro e observação de conhecimento.

## Arquitetura
- Banco de dados SQLite em nova_memory.db
- Gerenciador de memória em src/memory/knowledge.py
- Inicialização do banco em src/memory/database.py
- API FastAPI em api/main.py
- Rotas de conhecimento e aprendizado em api/routes/
- Serviço de estatísticas e aprendizado em api/services/learner.py
- Módulo de aprendizado autônomo em learning/autonomous_learning.py
- Interface web em web/index.html, web/style.css e web/script.js

## Como executar
### 1. Instalar dependências
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

### 2. Rodar a API
```bash
python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acessar a interface web
Abra o navegador em:
```text
http://127.0.0.1:8000/
```

### 4. Rodar a interface através do app web separado
```bash
python3 -m uvicorn web.app:app --reload --host 0.0.0.0 --port 8000
```

## Aprendizado autônomo
Coloque arquivos .txt na pasta knowledge_input/ para simular aprendizado automático.
Exemplo:
```text
knowledge_input/python.txt
```

Depois execute o ciclo de aprendizado com uma das opções abaixo:
```bash
python3 -c "from learning.autonomous_learning import AutonomousLearner; AutonomousLearner().scan_for_new_files()"
```
ou via API:
```bash
curl -X POST http://127.0.0.1:8000/learning/run
```

## Endpoints da API
- GET /knowledge — lista os conhecimentos salvos
- GET /stats — retorna quantidade de conhecimentos, categorias, última atividade e tempo de execução
- POST /learn — salva um novo conhecimento
- POST /learning/run — executa o ciclo de aprendizado sobre os arquivos da pasta knowledge_input/
- GET /health — verificação de saúde da API

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
  app.py
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

## Como testar
```bash
python3 -m unittest discover -s tests -v
```

## Fluxo de funcionamento
1. A NOVA verifica arquivos .txt em knowledge_input/.
2. O módulo de aprendizado extrai um nome, categoria e descrição simples.
3. O conhecimento é salvo no banco SQLite.
4. A atividade é registrada em logs/learning.log.
5. A API expõe o estado da memória e os dados de estatísticas.
