# CORTEX – Roadmap & Gestão de Tarefas

*Última actualização:* 06-06-2024 14:15

> Usa este ficheiro para marcar progresso. Assinala com `[x]` quando concluíres.

---

## Marcos de Entrega (Milestones)

| Milestone | Data Prevista | Descrição |
|-----------|---------------|-----------|
| **MVP Básico** | 18-06-2024 | Servidor MCP funcional com gestão de sessões básica |
| **Integração Cursor** | 02-07-2024 | Funcionalidades completas, integradas ao Cursor |
| **Sistema de Tarefas** | 16-07-2024 | Gestão hierárquica de tarefas funcionando |
| **Versão 1.0** | 30-07-2024 | Release estável com documentação completa |

---

## Sprint 0 – Bootstrapping (04/06 - 10/06)
- [x] Configurar estrutura de directórios
- [x] `pyproject.toml` com dependências principais
  - [x] FastAPI, Typer, Pydantic, SQLAlchemy, Alembic
  - [x] Pytest, Black, isort, mypy
  - [x] Prometheus client, structlog
- [x] `README.md` com visão geral + quickstart
- [x] Script `scripts/bootstrap.sh` (venv + pip install + migrate)
- [ ] Pre-commit (black + isort + flake8)
- [x] Git inicial + 1º commit
- [x] Esqueleto básico de módulos
  - [x] `cortex/mcp/`
  - [x] `cortex/core/`
  - [x] `cortex/cli/`
  - [x] `tests/`

## Sprint 1 – Data Layer MVP (11/06 - 17/06)
- [x] Modelagem completa do banco de dados
  - [x] `core/db.py` com engine + Session
  - [x] `core/models/session.py` (Session, SessionMetadata)
  - [x] `core/models/message.py` (Message, MessageRole)
  - [x] `core/models/task.py` (Task, TaskStatus, TaskLevel)
  - [x] `core/models/state.py` (State, StateSnapshot)
  - [x] `core/models/marker.py` (Marker, MarkerType)
- [x] Alembic config + migração inicial
  - [x] `alembic/env.py`
  - [x] Migração base com todas as tabelas
- [ ] DAO (Data Access Objects)
  - [ ] `core/dao/session_dao.py`
  - [ ] `core/dao/message_dao.py`
  - [ ] `core/dao/task_dao.py`
- [ ] Testes PyTest
  - [ ] Fixture para BD de teste (SQLite em memória)
  - [ ] Testes unitários para cada DAO
  - [ ] Testes de integração com BD

## Sprint 2 – MCP Core & scan_markers (18/06 - 24/06)
- [x] Implementação base do servidor MCP
  - [x] `mcp/server.py` com loop de leitura stdio
  - [ ] `mcp/protocol.py` com classes para request/response MCP
  - [ ] `mcp/registry.py` para registro de ferramentas
  - [ ] `mcp/logging.py` configuração de logs estruturados
- [x] Ferramentas de sessão
  - [x] `mcp/tools/session.py` (start/end/list)
  - [x] `mcp/tools/conversation.py` (record_message, get_context)
  - [x] `mcp/tools/markers.py` (scan_markers)
- [ ] Implementação básica da API principal
  - [ ] `core/session_manager.py`
  - [ ] `core/message_manager.py`
  - [ ] `core/marker_scanner.py`
- [ ] Testes de integração
  - [ ] Mocking de entradas/saídas MCP
  - [ ] Verificação de respostas corretas
  - [ ] Teste end-to-end de sessão completa

## Sprint 3 – Integração Cursor & Context Engine MVP (25/06 - 01/07)
- [x] Template `~/.cursor/mcp.json` para documentação
- [ ] Detecção e gestão de contexto
  - [ ] `core/context/detector.py` para identificar contextos
  - [ ] `core/context/rules.py` para aplicar regras
  - [ ] `core/context/registry.py` para registrar regras
- [ ] Teste de integração com Cursor (mock)
  - [ ] Simulação de interações com Cursor
  - [ ] Verificação de latência
  - [ ] Teste de recuperação de contexto
- [ ] Suporte a comandos de chat
  - [ ] Parser para comandos `/cortex:*`
  - [ ] Handler para traduzir comandos em chamadas de API

## Sprint 4 – Funcionalidades Avançadas & Observabilidade (02/07 - 08/07)
- [ ] Resumo automático de conversas
  - [ ] `core/summarizer.py` com lógica de resumo
  - [ ] Configuração de gatilhos (tokens, tempo)
- [ ] Cache LRU para contexto
  - [ ] `core/cache.py` com implementação
  - [ ] Estratégia de invalidação
- [ ] Observabilidade completa
  - [ ] `core/metrics.py` com configuração Prometheus
  - [ ] Dashboard Grafana básico (JSON)
  - [ ] Alertas para erros críticos
- [ ] Suporte a pesquisa em conversas
  - [ ] `core/search.py` com índice básico
  - [ ] API para busca de mensagens

## Sprint 5 – CLI & Export/Import (09/07 - 15/07)
- [x] CLI com Typer
  - [x] `cli/main.py` com comandos principais
  - [ ] `cli/session.py` para gestão de sessões
  - [ ] `cli/task.py` para gestão de tarefas
  - [ ] `cli/export.py` para exportação/importação
- [ ] Funcionalidades de exportação/importação
  - [ ] `core/export.py` com lógica de serialização
  - [ ] Formatos JSON e Markdown
  - [ ] Suporte para migração SUGSE→CORTEX
- [ ] Suporte a diff e merge de estados
  - [ ] `core/state/diff.py` para comparar estados
  - [ ] `core/state/merge.py` para combinar estados

## Sprint 6 – Gestão de Tarefas (16/07 - 22/07)
- [ ] Implementação do sistema hierárquico
  - [ ] `core/task/hierarchy.py` para gerir relacionamentos
  - [ ] `core/task/propagation.py` para propagar status
- [ ] Comandos de tarefas para chat
  - [ ] `/cortex:task`
  - [ ] `/cortex:task-status`
  - [ ] `/cortex:list-tasks`
- [ ] Painéis de visualização
  - [ ] `cli/task_view.py` para visualização em terminal
  - [ ] Exportação para formatos externos (Markdown)
- [ ] Integração com marcadores
  - [ ] `core/task/marker_linker.py` para associar TODOs com tarefas

## Sprint 7 – Motor Contextual & Detecção (23/07 - 29/07)
- [ ] Sistema avançado de detecção de contexto
  - [ ] `core/context/analyzer.py` para análise semântica
  - [ ] `core/context/fingerprint.py` para gerar assinaturas
- [ ] Regras adaptativas 
  - [ ] `core/context/rules_engine.py` motor completo
  - [ ] `core/context/templates.py` regras predefinidas
  - [ ] Interface para adicionar regras customizadas
- [ ] Métricas de eficácia adaptativa
  - [ ] Tracking de hit/miss de detecção
  - [ ] Ajuste automático de sensibilidade

## Sprint 8 – Hardening (30/07 - 05/08)
- [ ] Logging completo
  - [ ] Níveis configuráveis
  - [ ] Rotação de logs
  - [ ] Filtros de PII (informação pessoal)
- [ ] Testes de carga
  - [ ] Locust para simulação de uso intenso
  - [ ] Benchmarks de performance
  - [ ] Otimizações com base em resultados
- [ ] Segurança
  - [ ] Revisão de autenticação
  - [ ] Criptografia em repouso
  - [ ] Auditoria de acessos
- [ ] Tratamento de erros
  - [ ] Estratégias de retry
  - [ ] Fallbacks graceful
  - [ ] Recuperação automática

## Sprint 9 – Deployment & Docs (06/08 - 12/08)
- [x] `docker-compose.yml` completo
  - [x] Serviço PostgreSQL
  - [x] Serviço CORTEX
  - [ ] Grafana + Prometheus (opcional)
- [ ] README completo + documentação
  - [ ] Guia de instalação detalhado
  - [ ] Tutorial de uso com exemplos
  - [ ] Referência de APIs
  - [ ] Troubleshooting comum
- [ ] Scripts de deployment
  - [ ] `scripts/install.sh` com detecção de ambiente
  - [ ] `scripts/backup.sh` para backup de dados
  - [ ] `scripts/upgrade.sh` para atualizações

---

## Instalação de Dependências

Necessário para desenvolvimento:
- Python 3.12+
- PostgreSQL 14+
- Docker & Compose (desenvolvimento)
- Git

Instalação rápida:
```bash
# Clonar repositório
git clone https://github.com/odinosa/cortex.git
cd cortex

# Instalar todas as dependências
./scripts/bootstrap.sh

# Iniciar servidor modo desenvolvimento
python -m cortex.cli serve --dev
```

---

### Backlog / Ideias Futuras
- [ ] UI Web minimal (FastAPI + Jinja) para visualização de sessões
- [ ] Suporte opcional a SQLite para quem não quiser PostgreSQL
- [ ] Integração com Notion para logging de sessões
- [ ] Suporte multi-utilizador para equipas (CORTEX Teams)
- [ ] Análise avançada de padrões (CORTEX Insights)
- [ ] Versão SaaS com sincronização (CORTEX Cloud)
- [ ] Plugins para outros IDEs além do Cursor
- [ ] API GraphQL para integrações avançadas 