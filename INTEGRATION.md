# Integração com Cursor

*Última atualização:* 09-07-2024

Este documento descreve como o CORTEX se integra ao ambiente de desenvolvimento Cursor através do Model Context Protocol (MCP).

## Sobre o MCP

O [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) é um protocolo que permite que Modelos de Linguagem de Grande Escala (LLMs) no Cursor acessem ferramentas externas através de um formato padronizado. O CORTEX implementa o MCP para:

1. Receber e processar comandos do Cursor
2. Fornecer informações de contexto para o modelo
3. Manter estado entre sessões
4. Interagir com o sistema de arquivos local

## Setup MCP

A integração com o Cursor requer uma configuração no arquivo `~/.cursor/mcp.json`:

```json
{
  "tools": {
    "cortex": {
      "command": "python -m cortex.mcp",
      "env": {},
      "enabled": true
    }
  }
}
```

O comando `cortex.cli setup-cursor` configura automaticamente este arquivo.

### Permissões

O CORTEX requer acesso a:

- Sistema de arquivos (para ler/gravar arquivos de projeto)
- SQLite (para armazenar dados de sessão e tarefas)
- Porta stdio (para comunicação com o Cursor)

## Comandos Disponíveis

Os seguintes comandos podem ser usados diretamente no chat do Cursor:

### Gestão de Sessões

```
/cortex:start "Nome da Sessão" "Objetivo principal"
```
Inicia uma nova sessão de trabalho. A sessão é vinculada ao projeto atual.

```
/cortex:end
```
Finaliza a sessão atual e gera um resumo.

```
/cortex:list-sessions [filtro]
```
Lista as sessões disponíveis, opcionalmente filtrando por nome.

```
/cortex:resume <session_id>
```
Retoma uma sessão anterior, carregando seu contexto.

### Contexto e Estado

```
/cortex:context [filtro]
```
Obtém o contexto atual da sessão.

```
/cortex:save-state "nome_do_snapshot"
```
Salva um snapshot do estado atual.

```
/cortex:load-state "nome_do_snapshot"
```
Carrega um estado previamente salvo.

### Tarefas e Progresso

```
/cortex:task "Nova tarefa" --parent <parent_id> --level <level>
```
Cria uma nova tarefa na hierarquia.

```
/cortex:task-status <task_id> <status> [--progress <0-100>]
```
Atualiza o status e o progresso de uma tarefa.

```
/cortex:list-tasks [filtro]
```
Lista as tarefas do projeto, opcionalmente com filtro.

### Sistema Híbrido SQLite + Markdown

```
/cortex:export-tasks "caminho/para/arquivo.md" [filtros]
```
Exporta tarefas do SQLite para um arquivo Markdown, aplicando filtros opcionais como nível, status, etc.

```
/cortex:import-tasks "caminho/para/arquivo.md"
```
Importa tarefas de um arquivo Markdown para o SQLite, criando ou atualizando conforme necessário.

```
/cortex:sync-tasks "caminho/para/arquivo.md"
```
Sincroniza automaticamente as tarefas entre SQLite e Markdown, detectando e resolvendo conflitos.

```
/cortex:diff-tasks "caminho/para/arquivo.md"
```
Mostra diferenças entre as tarefas no SQLite e no arquivo Markdown, sem realizar alterações.

### Marcadores

```
/cortex:scan-markers
```
Escaneia o projeto em busca de TODOs, FIXMEs e outros marcadores.

```
/cortex:link-marker <marker_id> <task_id>
```
Associa um marcador a uma tarefa.

```
/cortex:todo-report
```
Gera um relatório dos TODOs e FIXMEs encontrados.

### Resumos

```
/cortex:summarize
```
Gera um resumo da sessão atual.

### Ajuda

```
/cortex:help [comando]
```
Mostra ajuda geral ou sobre um comando específico.

## Ferramentas MCP

Internamente, o CORTEX implementa as seguintes ferramentas MCP que são expostas ao Cursor:

### Ferramentas de Sessão

- `start_session`: Inicia uma nova sessão com título e objetivo
- `end_session`: Finaliza uma sessão atual
- `list_sessions`: Lista sessões existentes
- `resume_session`: Retoma uma sessão existente
- `record_message`: Registra uma mensagem na sessão atual

### Ferramentas de Contexto

- `get_context`: Obtém o contexto da sessão atual
- `save_state`: Salva um snapshot do estado atual
- `load_state`: Carrega um snapshot existente
- `detect_context`: Detecta automaticamente o contexto do projeto

### Ferramentas de Tarefas

- `create_task`: Cria uma nova tarefa
- `update_task_status`: Atualiza o status de uma tarefa
- `list_tasks`: Lista tarefas com filtros
- `task_details`: Obtém detalhes de uma tarefa específica
- `set_task_relations`: Define relações entre tarefas

### Ferramentas SQLite + Markdown

- `export_tasks_markdown`: Exporta tarefas do SQLite para Markdown
- `import_tasks_markdown`: Importa tarefas de Markdown para SQLite
- `sync_tasks`: Sincroniza tarefas entre SQLite e Markdown
- `diff_tasks`: Compara tarefas entre SQLite e Markdown
- `resolve_conflicts`: Resolve conflitos de sincronização

### Ferramentas de Marcadores

- `scan_markers`: Escaneia o projeto em busca de marcadores
- `link_marker_to_task`: Associa um marcador a uma tarefa
- `generate_todo_report`: Gera um relatório de TODOs e FIXMEs

### Ferramentas de Resumo

- `summarize_conversation`: Gera um resumo da sessão atual
- `generate_next_steps`: Sugere próximos passos com base no contexto

## Fluxo de Trabalho Típico

1. **Início do Dia**
   - Abra o Cursor e seu projeto
   - Use `/cortex:resume` para continuar uma sessão ou `/cortex:start` para iniciar uma nova

2. **Durante o Desenvolvimento**
   - Trabalhe normalmente com o Cursor AI
   - Use `/cortex:task` para criar novas tarefas conforme necessário
   - Atualize o status com `/cortex:task-status`
   - Use `/cortex:export-tasks` para visualizar suas tarefas em Markdown quando precisar de uma visão geral

3. **Planejamento e Revisão**
   - Exporte tarefas para Markdown com `/cortex:export-tasks`
   - Edite manualmente o arquivo Markdown em seu editor preferido
   - Importe as alterações de volta para o SQLite com `/cortex:import-tasks`
   - Ou use `/cortex:sync-tasks` para sincronização bidirecional automática

4. **Final do Dia**
   - Use `/cortex:summarize` para obter um resumo do progresso
   - Use `/cortex:scan-markers` para identificar TODOs e FIXMEs
   - Opcionalmente, use `/cortex:save-state` para criar um snapshot importante

## Implementação da Comunicação MCP

A comunicação entre o Cursor e o CORTEX segue o seguinte fluxo:

1. O Cursor envia um objeto JSON através de stdin
2. O servidor MCP do CORTEX processa o comando
3. O CORTEX envia uma resposta JSON através de stdout
4. O Cursor apresenta o resultado ao usuário

Exemplo de solicitação MCP:

```json
{
  "name": "cortex.create_task",
  "arguments": {
    "title": "Implementar sincronização SQLite-Markdown",
    "level": "task",
    "parent_id": 42
  }
}
```

Exemplo de resposta MCP:

```json
{
  "result": {
    "task_id": 123,
    "title": "Implementar sincronização SQLite-Markdown",
    "level": "task",
    "status": "not_started"
  }
}
```

## Depuração

O CORTEX registra logs detalhados em `~/.cortex/logs/mcp.log`. Para habilitar logs de depuração:

```bash
python -m cortex.cli config set log_level debug
```

## Resolução de Problemas

- **O Cursor não reconhece os comandos CORTEX**: Verifique se o servidor MCP está em execução e se `~/.cursor/mcp.json` está configurado corretamente.
- **O servidor MCP não inicia**: Verifique o log em `~/.cortex/logs/mcp.log` para detalhes do erro.
- **Problemas de sincronização Markdown**: Verifique se o arquivo Markdown segue o formato esperado. Use `/cortex:diff-tasks` para investigar discrepâncias.