# CORTEX

> Assistente de Contexto para Cursor via Model Context Protocol (MCP)

![Status: Em Desenvolvimento](https://img.shields.io/badge/status-em_desenvolvimento-orange)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![SQLite: 3.x](https://img.shields.io/badge/sqlite-3.x-blue)

## Índice

1. [Visão Geral](#visão-geral)
2. [Quickstart](#quickstart)
3. [Arquitetura](#arquitetura)
   - [Diagrama de Componentes](ARCHITECTURE.md#diagrama-de-componentes)
   - [Fluxo de Dados](ARCHITECTURE.md#fluxo-de-dados)
4. [Modelo de Dados](DATA_MODEL.md)
   - [Esquema SQLite](DATA_MODEL.md#esquema-sqlite)
   - [Relações](DATA_MODEL.md#relações)
5. [Plano do Projeto](PROJECT_PLAN.md)
   - [Fases de Implementação](PROJECT_PLAN.md#fases-de-implementação)
   - [Priorização](PROJECT_PLAN.md#priorização)
6. [Integração com Cursor](INTEGRATION.md)
   - [Setup MCP](INTEGRATION.md#setup-mcp)
   - [Comandos Disponíveis](INTEGRATION.md#comandos-disponíveis)
7. [Gestão de Tarefas](#gestão-de-tarefas)
8. [Desenvolvimento Local](#desenvolvimento-local)
9. [FAQ](#faq)

## Visão Geral

O CORTEX funciona como um assistente de contexto para o ambiente de desenvolvimento Cursor, permitindo:

- Manter contexto estruturado entre sessões de desenvolvimento
- Gerir hierarquias de tarefas em 4 níveis
- Guardar e restaurar sessões de desenvolvimento
- Aplicar templates e regras conforme contexto do projeto

O CORTEX implementa o [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) para fornecer ferramentas que qualquer LLM pode utilizar para manter e recuperar estado.

## Quickstart

```bash
# Clone o repositório
git clone https://github.com/odinosa/cortex.git
cd cortex

# Configura o ambiente Python
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Inicializa o banco de dados
python -m cortex.cli init

# Inicia o servidor MCP (em background)
python -m cortex.cli serve &

# Configura o Cursor (se ainda não configurado)
python -m cortex.cli setup-cursor
```

## Gestão de Tarefas

O CORTEX utiliza uma abordagem híbrida SQLite + Markdown para gestão de tarefas, combinando o melhor de ambos os mundos:

### Características da Abordagem Híbrida

- **Armazenamento Primário em SQLite:** Todos os dados estruturados como tarefas, relações, datas e progresso são armazenados em SQLite.
- **Exportação para Markdown:** Visualização amigável das tarefas em formato Markdown a qualquer momento.
- **Edição Bidirecional:** Possibilidade de edição tanto via comandos quanto diretamente nos arquivos Markdown (sincronização bidirecional).

### Fluxo de Trabalho

1. **Criar e Gerir Tarefas:** Utilize comandos CORTEX para criar e atualizar tarefas (armazenadas em SQLite).
2. **Exportar para Visualização:** Exporte tarefas para Markdown quando precisar de visualização ou edição manual.
3. **Importar Alterações:** Sincronize alterações feitas em arquivos Markdown de volta para o SQLite.

### Comandos de Tarefas Híbridas

```
/cortex:export-tasks "caminho/para/arquivo.md" [filtros]   # Exporta tarefas para Markdown
/cortex:import-tasks "caminho/para/arquivo.md"            # Importa tarefas de arquivo Markdown
/cortex:sync-tasks "caminho/para/arquivo.md"              # Sincronização bidirecional
```

### Benefícios da Abordagem Híbrida

- **Desempenho:** SQLite para consultas rápidas e filtros complexos
- **Legibilidade:** Markdown para visualização e edição humana
- **Flexibilidade:** Edição por diversos meios (comandos, API, arquivos Markdown)
- **Integração:** Compatibilidade com ferramentas de versionamento como Git
- **Portabilidade:** Exportação para compartilhamento simples com outros membros da equipe

## Desenvolvimento Local

```bash
# Modo de desenvolvimento com auto-reload
python -m cortex.cli serve --dev

# Executar testes
pytest

# Verificar formatação
black cortex tests
```

## FAQ

**P: Como funciona a integração com o Cursor?**
R: O CORTEX utiliza o Model Context Protocol (MCP) para fornecer ferramentas que o Cursor pode utilizar. Quando configurado, o Cursor chamará estas ferramentas para guardar e restaurar contexto de desenvolvimento.

**P: Como é garantida a segurança dos dados?**
R: Todos os dados são armazenados localmente em SQLite, e o sistema funciona inteiramente no teu Macbook M3, sem enviar dados para serviços externos (exceto quando explicitamente configurado para integração com Jira).

**P: É possível migrar dados de outro sistema?**
R: Sim, o CORTEX inclui ferramentas para importar dados de sistemas anteriores como o SUGSE.

**P: Como escolher entre editar no SQLite ou no Markdown?**
R: Use comandos para operações rápidas durante o desenvolvimento e edição de Markdown para planejamento mais detalhado ou quando precisar visualizar a estrutura completa de tarefas.

## Principais Benefícios

- **Continuidade:** Nunca perca o fio condutor do seu desenvolvimento
- **Estrutura:** Organização clara do trabalho e progresso
- **Rastreabilidade:** Histórico completo de decisões e alterações
- **Adaptabilidade:** Sistema contextual ajusta regras automaticamente
- **Gerenciamento:** Controle hierárquico de tarefas (Fase → Etapa → Tarefa → Actividade)
- **Simplicidade:** Comandos directamente no chat do Cursor

## Comandos Disponíveis no Chat

Usa estes comandos directamente no chat do Cursor:

```
/cortex:start "Nome da Sessão" "Objetivo principal"
/cortex:list-sessions
/cortex:resume <session_id>
/cortex:task "Nova tarefa"
/cortex:task-status <task_id> "done"
/cortex:list-tasks [filtro]
/cortex:export-tasks "caminho/para/arquivo.md" [filtros]
/cortex:import-tasks "caminho/para/arquivo.md"
/cortex:sync-tasks "caminho/para/arquivo.md"
/cortex:save-state "nome_do_snapshot"
/cortex:load-state "nome_do_snapshot"
/cortex:scan-todos
/cortex:summarize
/cortex:help
```

## Fluxo de Trabalho Recomendado

1. **Início do dia:**
   - `/cortex:resume` para continuar sessão anterior, ou
   - `/cortex:start` para iniciar nova sessão

2. **Durante o desenvolvimento:**
   - Trabalha normalmente com o Cursor AI
   - O CORTEX grava automaticamente todas as interações
   - Cria tarefas com `/cortex:task` quando necessário
   - Usa `/cortex:save-state` em pontos importantes

3. **Final do dia:**
   - `/cortex:summarize` para obter resumo do progresso
   - `/cortex:scan-todos` para compilar pontos de continuidade
   - `/cortex:export-tasks` para exportar suas tarefas atuais
   - Não precisas finalizar a sessão - ela será retomada automaticamente

## Ferramentas MCP Disponíveis

- `start_session`: Inicia uma nova sessão de trabalho com objetivo e contexto
- `end_session`: Finaliza uma sessão atual 
- `record_message`: Regista mensagem (pergunta ou resposta) na sessão
- `get_context`: Recupera contexto relevante para o modelo
- `scan_markers`: Analisa código em busca de TODOs, FIXMEs e cria relatório
- `create_task`: Cria tarefa em hierarquia de 4 níveis
- `update_task_status`: Actualiza estado, progresso e relação hierárquica
- `list_tasks`: Lista tarefas filtradas por nível, estado ou sessão
- `export_tasks_markdown`: Exporta tarefas para formato Markdown
- `import_tasks_markdown`: Importa tarefas de arquivo Markdown
- `detect_context`: Detecta automaticamente o contexto de trabalho
- `save_state`: Guarda um snapshot do estado atual
- `load_state`: Recupera um estado previamente guardado
- `summarize_conversation`: Gera resumo automático da sessão

## Contribuições

Contribuições são bem-vindas! Vê o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Licença

MIT

---

*Última atualização: 09-07-2024 12:35*
