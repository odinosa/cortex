# Guia de Utilização do CORTEX

*Última atualização:* 09-07-2024

Este guia fornece instruções completas para instalar, configurar e utilizar o CORTEX no seu fluxo de trabalho de desenvolvimento.

## Índice

- [Instalação](#instalação)
- [Primeiros Passos](#primeiros-passos)
- [Integração com Cursor](#integração-com-cursor)
- [Fluxo de Trabalho Diário](#fluxo-de-trabalho-diário)
- [Gestão de Tarefas](#gestão-de-tarefas)
- [Abordagem Híbrida SQLite + Markdown](#abordagem-híbrida-sqlite--markdown)
- [Análise de Código](#análise-de-código)
- [Contexto e Estado](#contexto-e-estado)
- [Configuração Avançada](#configuração-avançada)
- [Solução de Problemas](#solução-de-problemas)
- [Exemplos Práticos](#exemplos-práticos)

## Instalação

### Pré-requisitos

- macOS (Apple Silicon ou Intel)
- Python 3.10 ou superior
- Cursor IDE instalado
- Acesso a Terminal

### Passos de Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/odinosa/cortex.git
   cd cortex
   ```

2. **Configure o ambiente Python**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Inicialize o banco de dados**:
   ```bash
   python -m cortex.cli init
   ```

4. **Inicie o servidor MCP**:
   ```bash
   # Em um terminal dedicado ou como daemon
   python -m cortex.cli serve
   
   # Ou em background
   python -m cortex.cli serve &
   ```

5. **Configure o Cursor**:
   ```bash
   python -m cortex.cli setup-cursor
   ```

6. **Verifique a instalação**:
   ```bash
   python -m cortex.cli status
   ```

## Primeiros Passos

### Integração com Cursor

O CORTEX integra-se ao Cursor através do [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), que permite que o Cursor acesse ferramentas externas através de um formato padronizado.

A configuração do MCP é realizada automaticamente quando você executa o comando `setup-cursor`, que configura o arquivo `~/.cursor/mcp.json`:

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

### Iniciar uma Sessão

Para começar a usar o CORTEX, inicie uma nova sessão diretamente no chat do Cursor:

```
/cortex:start "Projeto XYZ" "Implementar sistema de autenticação"
```

Ou retome uma sessão existente:

```
/cortex:list-sessions
/cortex:resume <session_id>
```

## Fluxo de Trabalho Diário

O CORTEX é projetado para se integrar naturalmente ao seu fluxo de trabalho de desenvolvimento:

### 1. Início do Dia

- Abra o Cursor e seu projeto
- Use `/cortex:resume` para continuar uma sessão anterior ou `/cortex:start` para iniciar uma nova

### 2. Durante o Desenvolvimento

- Trabalhe normalmente com o Cursor AI
- Use `/cortex:task` para criar novas tarefas conforme necessário
- Atualize o status com `/cortex:task-status`
- Use `/cortex:export-tasks` para visualizar suas tarefas em Markdown quando precisar de uma visão geral

### 3. Planejamento e Revisão

- Exporte tarefas para Markdown com `/cortex:export-tasks`
- Edite manualmente o arquivo Markdown em seu editor preferido
- Importe as alterações de volta para o SQLite com `/cortex:import-tasks`
- Ou use `/cortex:sync-tasks` para sincronização bidirecional automática

### 4. Final do Dia

- Use `/cortex:summarize` para obter um resumo do progresso
- Use `/cortex:scan-markers` para identificar TODOs e FIXMEs
- Opcionalmente, use `/cortex:save-state` para criar um snapshot importante

## Gestão de Tarefas

O CORTEX oferece um sistema hierárquico de gestão de tarefas em 4 níveis:

1. **Fase**: Maior nível de organização (ex: "MVP Backend")
2. **Etapa**: Agrupamento lógico de tarefas (ex: "Implementação de Modelos")
3. **Tarefa**: Unidade de trabalho (ex: "Criar modelo de usuário")
4. **Atividade**: Passo específico (ex: "Adicionar validação de email")

### Comandos de Tarefas

Para criar uma nova tarefa:
```
/cortex:task "Nova tarefa" --level task --parent <parent_id>
```

Para atualizar o status de uma tarefa:
```
/cortex:task-status <task_id> <status> --progress <0-100>
```
Estados disponíveis: `not_started`, `in_progress`, `blocked`, `completed`

Para listar tarefas:
```
/cortex:list-tasks [--status in_progress] [--level task]
```

## Abordagem Híbrida SQLite + Markdown

O CORTEX implementa uma abordagem híbrida inovadora que combina o armazenamento estruturado do SQLite com a flexibilidade dos arquivos Markdown.

### Exportação para Markdown

Exporte tarefas para um arquivo Markdown:

```
/cortex:export-tasks "caminho/para/tarefas.md"
```

Com filtros:
```
/cortex:export-tasks "tarefas.md" --status in_progress,not_started --level phase,stage
```

### Edição Manual em Markdown

O arquivo Markdown gerado segue uma estrutura hierárquica que você pode editar manualmente:

```markdown
# Projeto: Nome do Projeto
*Atualizado: DATA_HORA*

## Fase: Nome da Fase
- **Status:** Estado
- **Progresso:** X%
- **Descrição:** Descrição detalhada da fase

### Etapa: Nome da Etapa
- **Status:** Estado
- **Progresso:** X% 
- **Descrição:** Descrição da etapa

#### Tarefa: Nome da Tarefa [ID:task_123]
- **Status:** Estado
- **Progresso:** X%
- **Estimativa:** Y horas
- **Descrição:** Descrição da tarefa

##### Atividade: Nome da Atividade [ID:task_456]
- **Status:** Estado
- **Progresso:** X%
- **Descrição:** Descrição da atividade
```

### Importação e Sincronização

Para importar alterações do Markdown para o SQLite:

```
/cortex:import-tasks "caminho/para/tarefas.md"
```

Para sincronização bidirecional (comparando SQLite e Markdown):

```
/cortex:sync-tasks "caminho/para/tarefas.md"
```

Para visualizar diferenças antes de sincronizar:

```
/cortex:diff-tasks "caminho/para/tarefas.md"
```

### Caso de Uso: Planejamento Colaborativo

```
# 1. Exporte tarefas atuais
/cortex:export-tasks "planejamento-sprint.md"

# 2. Compartilhe o arquivo com a equipe
# 3. Cada membro adiciona ou edita tarefas no arquivo

# 4. Importe as alterações
/cortex:import-tasks "planejamento-sprint.md"

# 5. Verifique as atualizações
/cortex:list-tasks --level phase
```

## Análise de Código

O CORTEX ajuda a rastrear pontos de continuidade no seu código.

### Escaneando Marcadores

Para escanear marcadores no código:
```
/cortex:scan-markers
```

Para gerar relatório de TODOs:
```
/cortex:todo-report
```

Para associar um marcador a uma tarefa:
```
/cortex:link-marker <marker_id> <task_id>
```

## Contexto e Estado

### Gerenciando Contexto

Para obter o contexto atual:
```
/cortex:context
```

### Salvando e Carregando Estados

Para salvar um snapshot do estado:
```
/cortex:save-state "nome-do-snapshot"
```

Para carregar um snapshot:
```
/cortex:load-state "nome-do-snapshot"
```

## Configuração Avançada

### Configurações Personalizadas

Para listar configurações:
```bash
python -m cortex.cli config list
```

Para atualizar uma configuração:
```bash
python -m cortex.cli config set marcador_path /caminho/personalizado
```

## Solução de Problemas

### Servidor MCP não responde

Verifique o status do servidor:
```bash
python -m cortex.cli status
```

Reinicie o servidor:
```bash
python -m cortex.cli restart
```

### Cursor não reconhece comandos

Verifique a configuração do MCP:
```bash
cat ~/.cursor/mcp.json
```

Reconfigure se necessário:
```bash
python -m cortex.cli setup-cursor
```

### Erro de Importação de Markdown

Se a importação de Markdown falhar:

1. Verifique o formato do arquivo (deve seguir a estrutura de níveis e atributos)
2. Verifique se há conflitos: `/cortex:diff-tasks "tarefas.md"`
3. Tente resolver manualmente ou use a opção de força:
   ```
   /cortex:import-tasks "tarefas.md" --force=sqlite
   ```
   (ou `--force=markdown` para priorizar o conteúdo do arquivo)

### Logs de Depuração

O CORTEX registra logs detalhados em `~/.cortex/logs/mcp.log`. Para habilitar logs de depuração:

```bash
python -m cortex.cli config set log_level debug
```

## Exemplos Práticos

### Exemplo 1: Iniciar um Novo Projeto

```
/cortex:start "Projeto XYZ" "Implementar sistema de autenticação"
/cortex:task "Implementação de Autenticação" --level phase
/cortex:task "Configurar Backend" --level stage --parent 1
/cortex:task "Implementar rotas de API" --level task --parent 2
/cortex:export-tasks "projeto-xyz.md"
```

### Exemplo 2: Fluxo Híbrido SQLite + Markdown

```
# 1. Exporte tarefas atuais
/cortex:export-tasks "tarefas-atual.md"

# 2. Edite o arquivo em seu editor preferido
# ... edição manual ...

# 3. Importe as alterações
/cortex:import-tasks "tarefas-atual.md"

# 4. Verifique as atualizações
/cortex:list-tasks
```

### Exemplo 3: Manter Sincronização Contínua

Para projetos com edição frequente do arquivo Markdown:

```bash
# Crie um script de sincronização automática
echo '#!/bin/bash
while true; do
  python -m cortex.cli sync-tasks "tarefas.md" --auto-resolve=merge
  sleep 300  # Sincronizar a cada 5 minutos
done' > sync-tasks.sh

chmod +x sync-tasks.sh
./sync-tasks.sh &
```

## Resumo dos Comandos

### Gestão de Sessões
```
/cortex:start "Nome da Sessão" "Objetivo principal"
/cortex:end
/cortex:list-sessions [filtro]
/cortex:resume <session_id>
```

### Tarefas e Progresso
```
/cortex:task "Nova tarefa" --parent <parent_id> --level <level>
/cortex:task-status <task_id> <status> [--progress <0-100>]
/cortex:list-tasks [filtro]
```

### Sistema Híbrido SQLite + Markdown
```
/cortex:export-tasks "caminho/para/arquivo.md" [filtros]
/cortex:import-tasks "caminho/para/arquivo.md"
/cortex:sync-tasks "caminho/para/arquivo.md"
/cortex:diff-tasks "caminho/para/arquivo.md"
```

### Marcadores
```
/cortex:scan-markers
/cortex:link-marker <marker_id> <task_id>
/cortex:todo-report
```

### Contexto e Estado
```
/cortex:context [filtro]
/cortex:save-state "nome_do_snapshot"
/cortex:load-state "nome_do_snapshot"
```

### Resumos
```
/cortex:summarize
```

### Ajuda
```
/cortex:help [comando]
``` 