# CORTEX

> Memória de contexto para o Cursor via Model Context Protocol (MCP).

![Status: Early Development](https://img.shields.io/badge/status-early_development-orange)
![Python: 3.12+](https://img.shields.io/badge/python-3.12+-blue)
![PostgreSQL: 14+](https://img.shields.io/badge/postgresql-14+-blue)

## Visão Geral

O CORTEX funciona como o "cérebro" do teu ambiente de desenvolvimento Cursor, permitindo:

- Guardar e restaurar sessões de desenvolvimento completas
- Manter contexto estruturado de conversas com modelos LLM entre sessões
- Rastrear automaticamente tarefas, TODOs e FIXMEs do código
- Resumir progressos e fornecer contexto relevante a cada nova interação
- Gerir hierarquias de tarefas com propagação de estado
- Detectar automaticamente contextos de trabalho e aplicar regras apropriadas

Tudo através do [Model Context Protocol (MCP)](https://docs.cursor.com/context/model-context-protocol) - implementando ferramentas nativas que qualquer LLM pode utilizar para guardar e recuperar estado.

## Principais Benefícios

- **Continuidade:** Nunca perca o fio condutor do seu desenvolvimento
- **Estrutura:** Organização clara do trabalho e progresso
- **Rastreabilidade:** Histórico completo de decisões e alterações
- **Adaptabilidade:** Sistema contextual ajusta regras automaticamente
- **Gerenciamento:** Controle hierárquico de tarefas (Fase → Etapa → Tarefa → Actividade)
- **Simplicidade:** Comandos directamente no chat do Cursor

## Quickstart

```bash
# 1. Clone o repositório
git clone https://github.com/odinosa/cortex.git
cd cortex

# 2. Inicia o PostgreSQL local (requer Docker)
docker-compose up -d db

# 3. Configura o ambiente Python
python -m venv .venv
source .venv/bin/activate
pip install -e .

# 4. Executa as migrações
python -m cortex.cli migrate

# 5. Inicia o servidor MCP (modo daemon)
python -m cortex.cli serve
```

## Integração com Cursor

1. Cria/edita `~/.cursor/mcp.json` com:
```json
{
  "tools": [
    {
      "id": "cortex",
      "stdio": {
        "command": ["python", "-m", "cortex.mcp.server"]
      },
      "tools": ["start_session", "end_session", "record_message", "get_context", "scan_markers", "create_task", "update_task_status", "list_tasks", "detect_context", "save_state", "load_state"]
    }
  ]
}
```

2. Reinicia o Cursor

3. Verifica que o CORTEX está ativo abrindo o console do Cursor (`Cmd+Shift+P > Toggle Developer Console`) e procurando por `[MCP] Registered cortex tools`.

## Comandos Disponíveis no Chat

Usa estes comandos directamente no chat do Cursor:

```
/cortex:start "Nome da Sessão" "Objetivo principal"
/cortex:list-sessions
/cortex:resume <session_id>
/cortex:task "Nova tarefa"
/cortex:task-status <task_id> "done"
/cortex:list-tasks [filtro]
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
- `detect_context`: Detecta automaticamente o contexto de trabalho
- `save_state`: Guarda um snapshot do estado atual
- `load_state`: Recupera um estado previamente guardado
- `summarize_conversation`: Gera resumo automático da sessão

## Contribuições

Contribuições são bem-vindas! Vê o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Licença

MIT

---

*Última atualização: 04-06-2024 17:45*
