# CORTEX – Plano Estratégico de Desenvolvimento

**Data:** 03-05-2025 22:10

---

## 1. Objetivos e Intenções

### 1.1 Propósito
Construir um "cérebro" de sessões que armazena, recupera e resume contexto de trabalho no Cursor através do Model Context Protocol (MCP).

### 1.2 Objetivos de Alto Nível
1. MVP estável em 30 dias:
   - Ferramentas MCP: `start_session`, `end_session`, `record_message`, `get_context`
   - Persistência em PostgreSQL
2. Integração contínua com Cursor (via MCP)
3. Documentação, testes unitários & integração
4. Deployment local (docker-compose) + opcional cloud (Render/Fly.io)

### 1.3 Métricas de Sucesso
- Latência média < **50 ms** nas chamadas MCP locais
- Confiabilidade ≥ **95 %** na gravação de passos
- Cobertura de testes ≥ **80 %** no core

---

## 2. Inventário de Infraestrutura Disponível

| Componente            | Estado |
|-----------------------|--------|
| macOS 23.4.0 (local)  | ✅ |
| Python 3.10+          | ✅ |
| Node.js 18+           | ✅ |
| Docker & Compose      | ✅ |
| PostgreSQL 14 (porta 5433) | ✅ |
| Repositório Git       | A criar (`odinosa/cortex`) |

---

## 3. Roadmap de Fases

| Fase | Descrição | Duração |
|------|-----------|---------|
| **0** | Setup do repositório, estrutura & CI | 1 dia |
| **1** | Data Layer (SQLAlchemy + Alembic) | 3 dias |
| **2** | MCP Core (servidor stdio + ferramentas base + scan_markers) | 4 dias |
| **3** | Integração Cursor (mock) + Context Engine MVP | 2 dias |
| **4** | Funcionalidades avançadas (summaries, cache) + Observabilidade Prometheus | 5 dias |
| **5** | CLI & REST wrapper (opcional) | 3 dias |
| **6** | Observabilidade & hardening | 3 dias |
| **7** | Deployment (Docker & CI/CD) | 3 dias |
| **Total** | **≈ 24 dias úteis** (margem ≤ 30 dias) | |

---

## 4. Estrutura de Diretório Proposta
```text
cortex/
├─ core/
│  ├─ models.py
│  ├─ services/
│  └─ db.py
├─ mcp/
│  ├─ server.py
│  └─ tools/
│     ├─ session.py
│     ├─ conversation.py
│     └─ state.py
├─ cli.py
├─ pyproject.toml
├─ docker-compose.yml
└─ tests/
```

---

## 5. Dependências Iniciais
- fastapi (REST opcional), uvicorn
- sqlalchemy 2.x, psycopg2-binary
- alembic
- pydantic v2
- structlog
- pytest + pytest-asyncio

---

## 6. Próximas Ações Imediatas
1. `mkdir cortex && cd cortex`
2. `git init`
3. Criar `pyproject.toml` com dependências básicas
4. Adicionar `README.md` com visão geral
5. Configurar virtualenv + instalar dependências
6. Esboçar `core/db.py` (engine, sessionmaker)
7. Implementar migração inicial 