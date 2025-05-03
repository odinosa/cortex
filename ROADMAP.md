# CORTEX – Roadmap & Gestão de Tarefas

*Última actualização:* 03-05-2025 22:53

> Usa este ficheiro para marcar progresso. Assinala com `[x]` quando concluíres.

---

## Sprint 0 – Bootstrapping
- [ ] `pyproject.toml` minimal com dependências
- [ ] `README.md` inicial com visão geral + quickstart
- [ ] Script `scripts/bootstrap.sh` (venv + pip install + migrate)
- [ ] Pre-commit (black + isort) opcional
- [ ] Git inicial + 1º commit

## Sprint 1 – Data Layer MVP
- [ ] `core/db.py` com engine + Session
- [ ] `core/models.py` (Session, Message)
- [ ] Alembic config + migração inicial
- [ ] Teste PyTest: create session & insert message

## Sprint 2 – MCP Core & scan_markers
- [ ] `mcp/server.py` loop stdio + registo tools
- [ ] `mcp/tools/session.py` (start/end/list)
- [ ] `mcp/tools/conversation.py` (record message, get context)
- [ ] `mcp/tools/markers.py` (scan_markers)
- [ ] Testes integração stdio

## Sprint 3 – Integração Cursor & Context Engine MVP
- [ ] Template `~/.cursor/mcp.json` docs
- [ ] `detect_context` + `apply_context_rules` (stub)
- [ ] Teste latência & fiabilidade via stdin

## Sprint 4 – Funcionalidades Avançadas & Observabilidade
- [ ] `summarize_conversation`
- [ ] Cache LRU contexto
- [ ] structlog + Prometheus metrics

## Sprint 5 – CLI & Export/Import
- [ ] `cli.py` com Typer (`session`, `task`, `export`)
- [ ] `export_session` / `import_session`

## Sprint 6 – Hardening
- [ ] Logging extra + níveis
- [ ] Testes carga (Locust)

## Sprint 7 – Bootstrap & Docs
- [ ] `docker-compose.yml` (Postgres + comando cortex)
- [ ] README completo + HOWTO instalar & ligar ao Cursor
- [ ] Script `scripts/migrate.sh` se necessário

---

### Backlog / Ideias Futuras
- [ ] UI Web minimal (FastAPI + Jinja) para visualização de sessões
- [ ] Suporte opcional a SQLite para quem não quiser Postgres
- [ ] Integração com Notion para logging de sessões 