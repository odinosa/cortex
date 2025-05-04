# Arquitetura do CORTEX

*Última atualização:* 07-07-2024

Este documento descreve a arquitetura técnica do CORTEX, um sistema MCP (Model Context Protocol) para gestão de contexto e tarefas no ambiente Cursor.

## Principais Componentes

O CORTEX adota uma arquitetura modular e leve, focada em simplicidade e responsividade:

1. **MCP Server** - Interface com o Cursor via stdio
2. **Core Engine** - Lógica de negócio e gestão de estado
3. **SQLite Store** - Armazenamento persistente local
4. **CLI** - Interface de linha de comando para administração

## Diagrama de Componentes

```
┌─────────────────┐     MCP stdio     ┌─────────────────────────┐
│    Cursor AI    │◄────────────────►│    CORTEX MCP Server    │
└─────────────────┘                  └───────────┬─────────────┘
                                                  │
                                                  │
                                                  ▼
┌─────────────────┐     CLI          ┌─────────────────────────┐     SQLite    ┌──────────────┐
│  Administração  │◄────────────────►│    CORTEX Core Engine   │◄─────────────►│  Database    │
└─────────────────┘                  └────────────┬────────────┘               └──────────────┘
                                                  │
                                                  │ [Opcional]
                                                  ▼
                                     ┌─────────────────────────┐     HTTPS     ┌──────────────┐
                                     │    Jira Connector       │◄─────────────►│  Jira API    │
                                     └─────────────────────────┘               └──────────────┘
```

## Fluxo de Dados

### 1. Fluxo Básico MCP

1. Cursor invoca ferramentas MCP do CORTEX via stdio
2. MCP Server recebe e processa comandos
3. Core Engine aplica lógica de negócio
4. SQLite Store persiste dados
5. Resultado retorna para o Cursor

### 2. Detecção de Workspace

1. CORTEX inicia quando o Cursor abre
2. Detecta arquivo de workspace aberto
3. Carrega contexto específico do projeto
4. Determina tarefas pendentes para o projeto

### 3. Gestão de Sessão

1. Utilizador inicia sessão via comando `/cortex:start`
2. Sistema carrega contexto e tarefas pendentes
3. Sessão registra interações e alterações
4. Ao finalizar, sistema atualiza estado das tarefas e cria contexto para próxima sessão

## Detalhamento dos Componentes

### MCP Server (`cortex.mcp`)

Responsável pela interface com o Cursor via Model Context Protocol:

- `server.py` - Loop principal de leitura/escrita stdio
- `protocol.py` - Serialização/deserialização de mensagens MCP
- `tools/` - Implementação das ferramentas MCP expostas
  - `session_tools.py` - Gestão de sessões
  - `task_tools.py` - Gestão de tarefas
  - `context_tools.py` - Gestão de contexto
  - `marker_tools.py` - Processamento de marcadores de continuidade

### Core Engine (`cortex.core`)

Contém a lógica principal do sistema:

- `engine.py` - Coordenação entre componentes
- `config.py` - Gestão de configuração
- `project.py` - Detecção e contexto de projetos
- `session.py` - Lógica de sessões de trabalho
- `task.py` - Gestão hierárquica de tarefas
- `context.py` - Gestão de contexto
- `markers.py` - Processamento de marcadores de continuidade
- `rules.py` - Aplicação de regras contextuais

### Persistência (`cortex.storage`)

Gerencia armazenamento de dados:

- `database.py` - Interface com SQLite
- `models/` - Definição dos modelos de dados
  - `session.py`
  - `task.py`
  - `context.py`
  - `marker.py`
  - `rule.py`
- `dao/` - Objetos de acesso a dados
  - `session_dao.py`
  - `task_dao.py`
  - `context_dao.py`

### CLI (`cortex.cli`)

Interface de linha de comando para administração:

- `main.py` - Ponto de entrada e comandos principais
- `server_cmd.py` - Comandos relacionados ao servidor
- `project_cmd.py` - Gestão de projetos
- `task_cmd.py` - Gestão de tarefas
- `setup_cmd.py` - Configuração inicial

### Integração Jira (Opcional)

Componente para sincronização bidirecional com Jira:

- `jira_connector.py` - Sincronização de tarefas
- `jira_mapper.py` - Mapeamento entre modelos CORTEX e Jira

## Inicialização do Sistema

1. O CORTEX inicia através de:
   - Startup automático configurado para o Cursor
   - Script `python -m cortex.cli serve`
   - Serviço do sistema operacional (opcional)

2. Na inicialização:
   - Verifica configuração e banco de dados
   - Abre conexão SQLite
   - Inicia servidor MCP
   - Monitora eventos do Cursor

3. Quando o Cursor abre um workspace:
   - Detecta projeto atual
   - Carrega configurações específicas
   - Prepara contexto e regras

## Considerações Técnicas

### Performance

- SQLite com Write-Ahead Logging (WAL) para otimizar concorrência
- Cache LRU para contextos frequentemente acessados
- Operações em background para não bloquear interface

### Segurança

- Armazenamento local para dados sensíveis
- Filtragem de credenciais em logs
- Integração segura com APIs externas

### Extensibilidade

- Arquitetura de plugins para componentes opcionais
- Hooks para personalização de comportamentos
- API interna estável para adição de recursos 