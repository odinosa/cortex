# Plano de Implementação do CORTEX

*Última atualização:* 07-07-2024

Este documento descreve o plano de implementação iterativo do CORTEX, com foco em entregar valor o mais rápido possível.

## Filosofia de Desenvolvimento

O CORTEX seguirá um modelo de desenvolvimento iterativo com fases bem definidas:

1. **MVP Funcional**: Implementar apenas funções essenciais, mas completas
2. **Desenvolvimento Incremental**: Adicionar funcionalidades em ciclos curtos
3. **"Dogfooding"**: Usar o CORTEX no desenvolvimento dele mesmo

## Fases de Implementação

O projeto será desenvolvido em 5 fases principais, com entregas incrementais em cada uma:

### Fase 1: Fundação (Sprint 1-2) - 2 Semanas

**Objetivo:** Sistema básico funcionando com gestão de sessões.

#### Sprint 1: Esqueleto e MCP Básico
- [x] Estrutura de diretórios e dependências
- [ ] Esquema SQLite básico (projects, sessions, messages)
- [ ] MCP Server com loop básico de stdio
- [ ] Integração com Cursor via `~/.cursor/mcp.json`
- [ ] Comandos básicos:
  - [ ] `/cortex:start` para iniciar sessão
  - [ ] `/cortex:end` para finalizar sessão

#### Sprint 2: Gestão de Projetos e Persistência
- [ ] Detecção de workspace e project
- [ ] Persistência de contexto entre sessões
- [ ] Comandos:
  - [ ] `/cortex:resume` para retomar sessão
  - [ ] `/cortex:context` para obter contexto atual

#### Entregável Fase 1:
- Sistema MCP funcionando com capacidade de persistir e restaurar sessões
- Detecção automática de projeto com base no workspace

### Fase 2: Gestão de Tarefas (Sprint 3-4) - 2 Semanas

**Objetivo:** Implementação do sistema hierárquico de tarefas e comandos relacionados.

#### Sprint 3: Modelo de Tarefas
- [ ] Esquema SQLite para tarefas (tasks, task_relations)
- [ ] Implementação do modelo hierárquico de 4 níveis
- [ ] Template para criar projeto com estrutura de tarefas
- [ ] Comandos:
  - [ ] `/cortex:task` para criar tarefa
  - [ ] `/cortex:task-status` para atualizar estado

#### Sprint 4: Utilidades de Tarefas
- [ ] Propagação de estado entre níveis hierárquicos
- [ ] Listagem e filtragem de tarefas
- [ ] Exportação para formato Markdown
- [ ] Comandos:
  - [ ] `/cortex:list-tasks` para listar tarefas
  - [ ] `/cortex:project` para criar/editar projeto

#### Entregável Fase 2:
- Modelo completo de gestão hierárquica de tarefas
- Capacidade de criar e manter projetos com suas tarefas

### Fase 3: Análise de Código (Sprint 5-6) - 2 Semanas

**Objetivo:** Implementação do sistema de marcadores e análise de código.

#### Sprint 5: Marcadores de Continuidade
- [ ] Escaneamento de código para encontrar marcadores
- [ ] Associação de marcadores com tarefas
- [ ] Comando:
  - [ ] `/cortex:scan-markers` para buscar marcadores
  - [ ] `/cortex:link-marker` para associar marcador com tarefa

#### Sprint 6: Relatórios e Continuidade
- [ ] Relatórios de resumo de sessão
- [ ] Extração de contexto para próxima sessão
- [ ] Comandos:
  - [ ] `/cortex:summarize` para resumir sessão
  - [ ] `/cortex:todo-report` para gerar relatório de TODOs

#### Entregável Fase 3:
- Sistema completo de rastreamento de marcadores
- Relatórios de progresso e continuidade

### Fase 4: Motor Contextual (Sprint 7-8) - 2 Semanas

**Objetivo:** Implementação do sistema de regras e contextos.

#### Sprint 7: Contextos
- [ ] Esquema SQLite para contextos e regras
- [ ] Motor de detecção de contexto
- [ ] Comandos:
  - [ ] `/cortex:add-context` para adicionar contexto
  - [ ] `/cortex:detect-context` para detectar contexto atual

#### Sprint 8: Regras
- [ ] Motor de aplicação de regras por contexto
- [ ] Templates de regras para casos comuns
- [ ] Comandos:
  - [ ] `/cortex:add-rule` para adicionar regra
  - [ ] `/cortex:list-rules` para listar regras ativas

#### Entregável Fase 4:
- Sistema completo de detecção e aplicação de regras contextuais
- Capacidade de adaptar comportamento com base no contexto

### Fase 5: Integração e Polimento (Sprint 9-10) - 2 Semanas

**Objetivo:** Integração com sistemas externos e melhorias de usabilidade.

#### Sprint 9: Integração Jira
- [ ] Conector bidirecional com Jira
- [ ] Sincronização de tarefas e estados
- [ ] Comando:
  - [ ] `/cortex:sync-jira` para sincronizar com Jira

#### Sprint 10: Polimento Geral
- [ ] Melhorias de UI/UX nos comandos
- [ ] Documentação completa
- [ ] Otimizações de performance
- [ ] Exportação/importação de dados

#### Entregável Fase 5:
- Sistema completo com integrações e documentação
- Produto finalizando para uso pessoal contínuo

## Priorização

A priorização do desenvolvimento segue os seguintes princípios:

1. **Valor Imediato**: Funcionalidades que podem ser usadas imediatamente têm prioridade
2. **Build-Measure-Learn**: Implementar, testar no uso real, ajustar
3. **Interdependências**: Construir fundações sólidas antes de recursos avançados

### Prioridades por Sessão

O sistema de Tarefas é prioritário porque:
- Fornece estrutura para organizar o trabalho
- Permite rastreamento de progresso
- Facilita a continuidade entre sessões

O sistema de Marcadores é o segundo porque:
- Complementa a gestão de tarefas
- Ajuda a não perder detalhes importantes
- Integra-se naturalmente ao fluxo de desenvolvimento

O motor contextual é o terceiro porque:
- Depende dos fundamentos das fases anteriores
- Oferece maior personalização da experiência
- Aumenta o poder das integrações

## Dependências e Requisitos

### Dependências Técnicas

```
# Em pyproject.toml

[project]
name = "cortex"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "click>=8.1.0",  # CLI
    "pydantic>=2.0.0",  # Modelos e validação
    "watchdog>=3.0.0",  # Monitorar alterações
    "rich>=13.0.0",  # UI para terminal
    "jira>=3.5.0",  # Integração Jira (opcional)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]
```

### Requisitos de Sistema

- **SO**: macOS (Apple Silicon M3)
- **Python**: 3.10 ou superior
- **Espaço em Disco**: <50MB para CORTEX + banco SQLite
- **Memória**: <100MB RAM em execução

## Monitoramento e Métricas

Para avaliar o sucesso do CORTEX, serão rastreadas as seguintes métricas:

1. **Uso**: Frequência de início/fim de sessões
2. **Continuidade**: Taxa de conclusão de tarefas
3. **Produtividade**: Tempo médio para completar tarefas
4. **Consistência**: Regularidade de sessões de trabalho

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Complexidade do MCP | Alta | Alto | Começar com subset mínimo de ferramentas |
| Latência em resposta | Média | Alto | Otimizar acesso ao SQLite, usar cache |
| Conflitos com Cursor | Média | Alto | Teste extensivo, versão-pin do Cursor |
| Erro na detecção de projetos | Média | Médio | UI para forçar seleção de projeto |
| Falta de usabilidade | Alta | Médio | Dogfooding intensivo, simplificar UX |

## Próximos Passos Imediatos

1. **Estrutura Base**:
   - Criar diretórios e arquivo pyproject.toml
   - Implementar CLI básico com Click

2. **MCP Minimal**:
   - Implementar servidor MCP com uma única ferramenta
   - Testar integração com Cursor 