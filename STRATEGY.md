# CORTEX – Visão Estratégica

**Data:** 04-06-2024 17:46

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
| Problemas de performance com datasets grandes | Estratégia de cache LRU + summarização automática |
| Ausência de gestão hierárquica de tarefas | Sistema de 4 níveis com propagação automática de estado |

---

## 2. Propósito do Módulo

Proporcionar **memória persistente** e **gestão de sessões** para o Cursor, de forma que o utilizador possa pausar, retomar e analisar o seu trabalho sem perda de contexto. O CORTEX visa eliminar as "bolhas de amnésia" entre sessões que limitam a produtividade dos desenvolvedores, através de um sistema inteligente que detecta contextos e adapta comportamentos.

### Princípios de Design

1. **Simplicidade na interface** - Comandos intuitivos no chat do Cursor
2. **Robustez no armazenamento** - Garantia de persistência e consistência de dados
3. **Adaptabilidade contextual** - Detecção e aplicação automática de regras por contexto
4. **Acesso transparente** - O modelo LLM pode acessar o contexto sem configuração adicional
5. **Baixa latência** - Respostas rápidas (<50ms) para não prejudicar experiência do utilizador

---

## 3. Funcionalidades Planeadas

| Área | Funcionalidade | Descrição |
|------|----------------|-----------|
| **Sessões** | `start_session` | Inicia uma nova sessão de trabalho, guarda objectivo & metadados |
| | `end_session` | Finaliza sessão, opcionalmente gera resumo & métricas |
| | `list_sessions` | Lista sessões recentes com filtros (data, status) |
| | `resume_session` | Restaura sessão anterior com contexto completo |
| **Mensagens** | `record_message` | Grava passo de conversa (role, content, tokens) |
| | `get_context` | Devolve as últimas *n* mensagens ou a síntese |
| | `summarize_conversation` | Produz resumo automático quando o contexto excede *k* tokens |
| | `search_conversations` | Pesquisa semântica em mensagens anteriores |
| **Estado** | `save_state` | Armazena snapshot de variáveis/ficheiros importantes |
| | `load_state` | Restaura estado previamente guardado |
| | `diff_state` | Compara estados para visualizar alterações |
| **Operações Avançadas** | `export_session` | Exporta sessão completa em JSON/Markdown |
| | `import_session` | Importa sessão externa (para migração SUGSE→CORTEX) |
| | `merge_sessions` | Combina contextos de múltiplas sessões |
| **Gestão de Tarefas** | `create_task` | Cria tarefa em hierarquia de 4 níveis (Fase → Etapa → Tarefa → Actividade) |
| | `update_task_status` | Actualiza estado, progresso e relação hierárquica |
| | `list_tasks` | Lista tarefas filtradas por nível, estado ou sessão |
| | `propagate_status` | Propaga conclusões entre níveis (ex.: concluir todas as subtarefas fecha a Story) |
| | `task_metrics` | Calcula métricas (percentual concluído, lead-time) |
| | `relate_tasks` | Cria relações entre tarefas (bloqueia, depende, duplica) |
| **Marcadores** | `scan_markers` | Extrai TODO/FIXME e gera relatório de pontos de continuidade |
| | `link_markers_to_tasks` | Associa marcadores a tarefas existentes |
| **Contexto** | `detect_context` | Detecta contexto da sessão com base em palavras-chave e actividade |
| | `apply_context_rules` | Motor que aplica regras adaptativas conforme contexto |
| | `register_context_rule` | Permite adicionar novas regras contextuais |
| **Observabilidade** | Métricas Prometheus | Latência, QPS, tamanho de logs |
| | Logging estruturado | JSON logs para fácil ingestão |
| | Dashboard Grafana | Visualização de métricas e uso |
| **Segurança** | Autorização API Key | Para deployments remotos |
| | Criptografia em repouso | Para dados sensíveis |
| | Controle de acesso | Para ambientes multi-utilizador |

---

## 4. Arquitectura de Alto Nível
```
┌─────────────────┐     MCP stdio     ┌─────────────────────────┐     SQL     ┌──────────────┐
│    Cursor AI    │◄────────────────►│    CORTEX MCP Server    │◄───────────►│  PostgreSQL  │
└─────────────────┘                  └─────────────────────────┘             └──────────────┘
                                         │                                       ▲
                                         │                                       │
                                         ▼                                       │
┌─────────────────┐     HTTP/REST    ┌─────────────────────────┐     S3      ┌──────────────┐
│ CLI & Dashboard │◄────────────────►│ FastAPI (Opcional)      │◄───────────►│ Armazenamento│
└─────────────────┘                  └─────────────────────────┘    Backup   └──────────────┘
                                         │
                                         ▼
┌─────────────────┐     Prometheus   ┌─────────────────────────┐
│     Grafana     │◄────────────────►│ Observabilidade         │
└─────────────────┘                  └─────────────────────────┘
```

### Componentes principais:
1. **MCP Server** – Núcleo do sistema que:
   - Aceita chamadas stdio ou SSE via MCP
   - Processa comandos e ferramentas
   - Implementa lógica de gestão de contexto
   - Detecta automaticamente contextos

2. **Core Services** – Lógica funcional:
   - Gestor de sessões
   - Gestor de mensagens
   - Motor de contexto
   - Engine de tarefas
   - Persistência de estado

3. **Data Layer** – Armazenamento e acesso:
   - SQLAlchemy para ORM
   - Alembic para migrações
   - PostgreSQL para dados primários
   - Redis opcional para cache (alta performance)
   - S3/MinIO opcional para backups

4. **Observabilidade** – Monitorização:
   - structlog para logs estruturados
   - Prometheus para métricas
   - Grafana para visualização
   - Alertas configuráveis

5. **Interfaces Secundárias**:
   - CLI Typer para administração
   - REST FastAPI (opcional) para integrações
   - WebUI simples para visualizações

### Fluxo de Dados Principal

1. Cursor envia comando via MCP
2. Servidor processa comando e consulta/atualiza BD
3. Resultados retornam ao Cursor via MCP
4. Métricas são registadas em Prometheus
5. Logs estruturados são gerados

### Segurança e Privacidade

- Todos os dados são armazenados localmente por padrão
- Suporte para criptografia em repouso para dados sensíveis
- Modo "ephemeral" opcional que não armazena conteúdo das mensagens
- Controle granular de acesso para ambientes compartilhados

---

## 5. Roadmap de Entregas (Resumido)
| Sprint | Objetivo | Principais Entregas |
|--------|----------|---------------------|
| 0 | Bootstrapping | Estrutura repo, CI, dependências | 
| 1 | Data Layer | Modelos + Migrações + Testes |
| 2 | MCP Core | Servidor stdio + ferramentas básicas + scan_markers |
| 3 | Integração Cursor | Template `mcp.json`, testes latência + Context Engine MVP |
| 4 | Func. Avançadas | Resumo automático, cache + Observabilidade Prometheus |
| 5 | CLI & REST | Typer CLI + FastAPI minimal + export/import session |
| 6 | Gestão de Tarefas | Sistema hierárquico completo + propagação de status |
| 7 | Motor Contextual | Detecção e regras avançadas + métricas adaptativas |
| 8 | Hardening | Logging extra, testes de carga, segurança |
| 9 | Deployment | Dockerfile, compose, CI/CD para instalação one-click |

---

## 6. Indicadores-Chave de Desempenho (KPIs)
- **Confiabilidade de gravação** ≥ 99.9%
- **Latência média MCP** < 50 ms local, <150 ms remoto
- **Tempo de recuperação de contexto** < 10 ms p/ 20 mensagens
- **Cobertura de testes** ≥ 85% core, ≥ 70% global
- **Overhead de memória** < 200MB em idle
- **Taxa de detecção contextual** > 90% de precisão
- **Tempo médio para resumo** < 2 segundos por 100 mensagens

---

## 7. Riscos & Mitigações
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Complexidade do MCP | Alta | Alto | Começar com subset mínimo de ferramentas + testes automatizados |
| Crescimento de dados no Postgres | Média | Médio | Retenção configurável + compressão + particionamento automático |
| Quebra de compatibilidade Cursor | Média | Alto | Versão-pin em docs + integração de testes + detecção de versão |
| Desempenho em projetos grandes | Média | Médio | Estratégias de cache + índices + summarização progressiva |
| Falhas em persistência | Baixa | Alto | Journaling + backup automático + recuperação transacional |
| Complexidade de instalação | Alta | Médio | Scripts de bootstrap + instalador one-click + documentação clara |

---

## 8. Escalabilidade e Crescimento Futuro

### Plano de Escalabilidade
- **Vertical:** Suporte a PostgreSQL em cluster
- **Horizontal:** Possibilidade de MCP Server distribuído
- **Dados:** Particionamento automático por data e sessão
- **Cache:** Suporte a Redis para ambientes de alto desempenho

### Oportunidades de Expansão
1. **CORTEX Teams** - Suporte multi-utilizador para equipas
2. **CORTEX Insights** - Análise avançada de padrões de desenvolvimento
3. **CORTEX Cloud** - Versão SaaS com sincronização
4. **CORTEX IDE Bridges** - Expansão para outros IDEs além do Cursor

---

## 9. Próximos Passos Imediatos
1. Concluir **Fase 0**: preencher `pyproject.toml`, README, CI.
2. Migrar partes úteis do SUGSE (modelos sessão, schemas) para `core/`.
3. Definir schema inicial Alembic.
4. Implementar esqueleto do `mcp/server.py` com logging dummy.
5. Criar script de bootstrap para fácil instalação inicial.

---

*Documento gerado e mantido por CORTEX – actualiza sempre após cada sprint.* 