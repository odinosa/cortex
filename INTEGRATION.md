# Integração com Cursor

*Última atualização:* 07-07-2024

Este documento descreve como o CORTEX se integra com o Cursor utilizando o Model Context Protocol (MCP).

## Model Context Protocol (MCP)

O MCP é uma especificação para permitir que modelos LLM acessem e modifiquem um contexto compartilhado. O Cursor implementa o MCP para permitir que ferramentas externas, como o CORTEX, gerenciem contexto para o LLM.

### Conceitos Chave do MCP

1. **Ferramentas MCP**: Funções que podem ser chamadas pelo LLM
2. **Protocolo de Comunicação**: Formato de mensagens trocadas via stdio
3. **Servidor MCP**: Processo que recebe e processa chamadas de ferramentas

## Setup MCP

### Configuração do Arquivo MCP

O CORTEX utiliza a configuração MCP para registrar suas ferramentas no Cursor. A instalação cria/modifica o arquivo `~/.cursor/mcp.json`:

```json
{
  "tools": [
    {
      "id": "cortex",
      "stdio": {
        "command": ["python", "-m", "cortex.mcp.server"]
      },
      "tools": [
        "start_session",
        "end_session", 
        "record_message",
        "get_context",
        "create_task",
        "update_task_status",
        "list_tasks",
        "scan_markers",
        "detect_context",
        "add_context",
        "apply_rule"
      ]
    }
  ]
}
```

Esta configuração:
- Define o CORTEX como uma ferramenta MCP com ID "cortex"
- Usa o servidor Python como ponto de entrada
- Registra as ferramentas disponíveis no Cursor

### Instalação Automática

O comando CLI do CORTEX configura automaticamente a integração:

```bash
python -m cortex.cli setup-cursor
```

Este comando:
1. Verifica se o Cursor está instalado
2. Cria/atualiza o arquivo MCP
3. Configura a inicialização automática (opcional)

## Comandos Disponíveis

O CORTEX disponibiliza dois tipos de interação:

1. **Comandos de Chat**: Digitados diretamente no Cursor
2. **Ferramentas MCP**: Invocadas pelo LLM via `<function_call>`

### Comandos de Chat

Os comandos de chat são prefixados com `/cortex:` e podem ser usados pelo usuário:

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/cortex:start` | Inicia uma nova sessão | `/cortex:start "Implementação Auth" "Implementar sistema de login"` |
| `/cortex:end` | Finaliza a sessão atual | `/cortex:end "Completo até validação de tokens"` |
| `/cortex:resume` | Retoma uma sessão anterior | `/cortex:resume 42` ou `/cortex:resume last` |
| `/cortex:task` | Cria uma nova tarefa | `/cortex:task "Implementar validação de email"` |
| `/cortex:task-status` | Atualiza status da tarefa | `/cortex:task-status 123 completed` |
| `/cortex:list-tasks` | Lista tarefas do projeto | `/cortex:list-tasks pending` |
| `/cortex:scan-markers` | Escaneia marcadores | `/cortex:scan-markers` |
| `/cortex:context` | Mostra contexto atual | `/cortex:context` |
| `/cortex:help` | Lista comandos disponíveis | `/cortex:help` |

### Parser de Comandos

O CORTEX implementa um parser de comandos que:
1. Captura mensagens do usuário começando com `/cortex:`
2. Analisa argumentos e formato
3. Redireciona para a função apropriada
4. Retorna resultado para o chat

## Ferramentas MCP

As ferramentas MCP são funções que podem ser chamadas pelo modelo LLM:

| Ferramenta | Descrição | Parâmetros |
|------------|-----------|------------|
| `start_session` | Inicia sessão | `title`, `objective` |
| `end_session` | Finaliza sessão | `summary`, `next_session_notes` |
| `record_message` | Registra mensagem | `role`, `content` |
| `get_context` | Obtém contexto atual | `max_messages`, `include_system` |
| `create_task` | Cria tarefa | `title`, `description`, `level`, `parent_id` |
| `update_task_status` | Atualiza tarefa | `task_id`, `status`, `progress` |
| `list_tasks` | Lista tarefas | `status`, `level`, `limit` |
| `scan_markers` | Escaneia marcadores | `directories`, `file_types` |
| `detect_context` | Detecta contexto atual | - |
| `add_context` | Adiciona contexto | `name`, `content` |
| `apply_rule` | Aplica regra | `rule_name` |

### Exemplo de Chamada MCP

O LLM pode chamar ferramentas MCP usando:

```
<function_call>
<invoke name="create_task">
<parameter name="title">Implementar validação de email</parameter>
<parameter name="level">task</parameter>
<parameter name="parent_id">42</parameter>
</invoke>
</function_call>
```

O servidor MCP processará esta chamada e retornará:

```
<function_result>
{"task_id": 123, "status": "created", "message": "Tarefa criada com sucesso"}
</function_result>
```

## Fluxo de Integração

### Inicialização

1. O CORTEX inicia automaticamente quando o Cursor é aberto
2. O servidor MCP registra suas ferramentas
3. O CORTEX detecta o workspace atual e carrega o projeto correspondente

### Durante Sessão

1. O usuário pode iniciar uma sessão via comando `/cortex:start`
2. O CORTEX monitora mensagens trocadas e as salva
3. O modelo LLM pode chamar ferramentas MCP conforme necessário
4. Tarefas e contextos são gerenciados via comandos ou ferramentas

### Finalização

1. O usuário fecha a sessão via `/cortex:end`
2. O CORTEX salva o estado final, resumo e tarefas concluídas
3. O CORTEX prepara contexto para a próxima sessão

## Configuração Avançada

### Inicialização Automática

O CORTEX pode ser configurado para iniciar automaticamente com o Cursor:

```bash
# Habilitar inicialização automática
python -m cortex.cli setup-autostart

# Desabilitar inicialização automática
python -m cortex.cli disable-autostart
```

### Customização de Ferramentas

Você pode personalizar quais ferramentas estão disponíveis no Cursor:

```bash
# Listar ferramentas disponíveis
python -m cortex.cli list-tools

# Habilitar/desabilitar ferramenta específica
python -m cortex.cli toggle-tool scan_markers
```

## Troubleshooting

### Verificar Integração

Para verificar se a integração está funcionando:

```bash
# Testar integração MCP
python -m cortex.cli test-mcp

# Verificar status do servidor
python -m cortex.cli status
```

### Problemas Comuns

1. **Servidor não inicia**:
   - Verificar logs em `~/.cortex/logs/server.log`
   - Confirmar que Python 3.10+ está instalado

2. **Ferramentas não aparecem no Cursor**:
   - Reiniciar o Cursor após instalar o CORTEX
   - Verificar se `~/.cursor/mcp.json` está correto

3. **Erros MCP no Console**:
   - Abrir console do Cursor (Cmd+Shift+P > Toggle Developer Console)
   - Procurar erros relacionados ao MCP