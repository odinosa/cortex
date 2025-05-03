# CORTEX – Visão Estratégica

**Data:** 03-05-2025 22:15

---

## 1. Contexto e Justificação

O SUGSE demonstrou o valor de gerir sessões e contexto de desenvolvimento, mas enfrentou problemas de complexidade e estabilidade devido à sua implementação via extensão TypeScript. O **CORTEX** surge como uma re-imaginação baseada nas lições aprendidas, posicionando-se como um *servidor MCP nativo* que actua como "cérebro" do ambiente Cursor.

### Lições Retiradas do SUGSE
| Desafio SUGSE | Estratégia CORTEX |
|---------------|------------------|
| Dependência forte da API de extensão do Cursor | Usar Model Context Protocol (MCP) nativo → menos acoplamento |
| Demasiadas camadas (Extensão TS ➜ HTTP ➜ API) | Simplificar para Cliente MCP ↔ Servidor MCP |
| Dificuldade de manutenção & logs dispersos | Logging estruturado + métrica Prometheus embutida |
| Fluxos de sessão complexos | Ferramentas MCP explícitas (`start_session`, `end_session`) |

---

## 2. Propósito do Módulo

Proporcionar **memória persistente** e **gestão de sessões** para o Cursor, de forma que o utilizador possa pausar, retomar e analisar o seu trabalho sem perda de contexto.

---

## 3. Funcionalidades Planeadas

| Área | Funcionalidade | Descrição |
|------|----------------|-----------|
| **Sessões** | `start_session` | Inicia uma nova sessão de trabalho, guarda objectivo & metadados |
| | `end_session` | Finaliza sessão, opcionalmente gera resumo & métricas |
| | `list_sessions` | Lista sessões recentes com filtros (data, status) |
| **Mensagens** | `record_message` | Grava passo de conversa (role, content, tokens) |
| | `get_context` | Devolve as últimas *n* mensagens ou a síntese |
| | `summarize_conversation` | Produz resumo automático quando o contexto excede *k* tokens |
| **Estado** | `save_state` | Armazena snapshot de variáveis/ficheiros importantes |
| | `load_state` | Restaura estado previamente guardado |
| **Operações Avançadas** | `export_session` | Exporta sessão completa em JSON/Markdown |
| | `import_session` | Importa sessão externa (para migração SUGSE→CORTEX) |
| **Gestão de Tarefas** | `create_task` | Cria tarefa em hierarquia de 4 níveis (Fase → Etapa → Tarefa → Actividade) |
| | `update_task_status` | Actualiza estado, progresso e relação hierárquica |
| | `list_tasks` | Lista tarefas filtradas por nível, estado ou sessão |
| | `propagate_status` | Propaga conclusões entre níveis (ex.: concluir todas as subtarefas fecha a Story) |
| | `task_metrics` | Calcula métricas (percentual concluído, lead-time) |
| **Marcadores** | `scan_markers` | Extrai TODO/FIXME e gera relatório de pontos de continuidade |
| **Contexto** | `detect_context` | Detecta contexto da sessão com base em palavras-chave e actividade |
| | `apply_context_rules` | Motor que aplica regras adaptativas conforme contexto |
| **Observabilidade** | Métricas Prometheus | Latência, QPS, tamanho de logs |
| | Logging estruturado | JSON logs para fácil ingestão |
| **Segurança** | Autorização API Key | Para deployments remotos |

---

## 4. Arquitectura de Alto Nível
```
┌──────────────┐     MCP stdio     ┌────────────────────┐     SQL     ┌──────────────┐
│   Cursor AI  │◄────────────────►│  CORTEX MCP Server  │◄───────────►│ PostgreSQL   │
└──────────────┘                  └────────────────────┘             └──────────────┘
                                     │ REST/CLI opc.                    ▲
                                     │                                 │
                                     ▼                                 │
                               Observability                          Backups
```

Componentes principais:
1. **MCP Server** – Aceita chamadas stdio ou SSE, processa ferramentas.
2. **Core Services** – Lógica de sessão, mensagens, estado.
3. **Data Layer** – SQLAlchemy + Alembic em PostgreSQL.
4. **Observabilidade** – structlog + Prometheus.
5. **Interfaces Secundárias** – CLI Typer e REST FastAPI (opcional).

---

## 5. Roadmap de Entregas (Resumo)
| Sprint | Objetivo | Principais Entregas |
|--------|----------|---------------------|
| 0 | Bootstrapping | Estrutura repo, CI, dependências | 
| 1 | Data Layer | Modelos + Migrações + Testes |
| 2 | MCP Core | Servidor stdio + ferramentas básicas + scan_markers |
| 3 | Integração Cursor (mock) | Template `mcp.json`, testes latência + Context Engine MVP |
| 4 | Funcionalidades Avançadas | Resumo automático, cache + Observabilidade Prometheus |
| 5 | CLI & REST | Typer CLI + FastAPI minimal + export/import session |
| 6 | Hardening | Logging extra, testes de carga |
| 7 | Deployment | Dockerfile, compose, CI/CD |

---

## 6. Indicadores-Chave de Desempenho (KPIs)
- **Confiabilidade de gravação** ≥ 95 %
- **Latência média MCP** < 50 ms local, <150 ms remoto
- **Tempo de recuperação de contexto** < 10 ms p/ 20 mensagens
- **Cobertura de testes** ≥ 80 % core

---

## 7. Riscos & Mitigações
| Risco | Mitigação |
|-------|-----------|
| Complexidade do MCP | Começar com subset mínimo de ferramentas |
| Crescimento de dados no Postgres | Retenção + rotatividade + compressão |
| Quebra de compatibilidade Cursor | Versão-pin em docs + integração de testes |

---

## 8. Próximos Passos Imediatos
1. Concluir **Fase 0**: preencher `pyproject.toml`, README, CI.
2. Migrar partes úteis do SUGSE (modelos sessão, schemas) para `core/`.
3. Definir schema inicial Alembic.
4. Implementar esqueleto do `mcp/server.py` com logging dummy.

---

*Documento gerado e mantido por CORTEX AI – actualiza sempre após cada sprint.* 