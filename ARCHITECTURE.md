# Arquitetura do CORTEX

*Última atualização:* 09-07-2024

Este documento descreve a arquitetura técnica do CORTEX, um sistema MCP (Model Context Protocol) para gestão de contexto e tarefas no ambiente Cursor.

## Principais Componentes

O CORTEX adota uma arquitetura modular e leve, focada em simplicidade e responsividade:

1. **MCP Server** - Interface com o Cursor via stdio
2. **Core Engine** - Lógica de negócio e gestão de estado
3. **SQLite Store** - Armazenamento persistente local
4. **Markdown Sync** - Sistema de sincronização bidirecional SQLite-Markdown
5. **CLI** - Interface de linha de comando para administração

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
                                                  │
                                                  ▼
                                     ┌─────────────────────────┐     I/O       ┌──────────────┐
                                     │    Markdown Sync        │◄─────────────►│ .md Files    │
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

### 4. Fluxo Híbrido SQLite + Markdown

1. Utilizador executa comando de exportação (`/cortex:export-tasks`)
2. Sistema converte tarefas do SQLite para formato Markdown
3. Utilizador edita arquivo Markdown manualmente
4. Sistema importa alterações de volta para SQLite (`/cortex:import-tasks`) ou sincroniza automaticamente (`/cortex:sync-tasks`)
5. Sistema detecta conflitos e oferece estratégias de resolução quando necessário

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
  - `markdown_tools.py` - Ferramentas para exportação/importação Markdown

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
  - `markdown_sync.py` - Modelo para rastreamento de sincronização Markdown
- `dao/` - Objetos de acesso a dados
  - `session_dao.py`
  - `task_dao.py`
  - `context_dao.py`
  - `markdown_sync_dao.py` - DAO para operações de sincronização

### Markdown Sync (`cortex.markdown`)

Gerencia a sincronização bidirecional entre SQLite e arquivos Markdown:

- `exporter.py` - Exportação de tarefas para Markdown
- `importer.py` - Importação e parsing de Markdown para tarefas
- `diff.py` - Detecção de diferenças entre SQLite e Markdown
- `conflict.py` - Resolução de conflitos de sincronização
- `formatter.py` - Formatação da saída Markdown

### CLI (`cortex.cli`)

Interface de linha de comando para administração:

- `main.py` - Ponto de entrada e comandos principais
- `server_cmd.py` - Comandos relacionados ao servidor
- `project_cmd.py` - Gestão de projetos
- `task_cmd.py` - Gestão de tarefas
- `markdown_cmd.py` - Comandos para exportação/importação Markdown
- `setup_cmd.py` - Configuração inicial

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

## Abordagem Híbrida SQLite + Markdown

### Fundamentos da Arquitetura

A abordagem híbrida SQLite + Markdown é implementada como um subsistema que oferece:

1. **Persistência Dual**:
   - SQLite como armazenamento primário e confiável
   - Markdown como interface amigável para visualização e edição humana

2. **Sincronização Bidirecional**:
   - Rastreamento de mudanças através de hashes de conteúdo
   - Detecção e resolução de conflitos

3. **Modelo de Dados Específico**:
   - Tabela `markdown_sync` para rastrear estado de sincronização
   - Mapeamento entre estrutura hierárquica em SQLite e níveis de cabeçalho em Markdown

### Fluxo de Operações

1. **Exportação (SQLite → Markdown)**:
   ```
   SQLite DB → TaskExporter → MarkdownFormatter → Arquivo .md
   ```

2. **Importação (Markdown → SQLite)**:
   ```
   Arquivo .md → MarkdownParser → TaskImporter → SQLite DB
   ```

3. **Sincronização**:
   ```
   DiffGenerator → ConflictDetector → ConflictResolver → Sincronização
   ```

### Mecanismo de Resolução de Conflitos

O sistema utiliza uma estratégia de resolução de conflitos em três níveis:

1. **Automática**: Quando as mudanças não se sobrepõem
2. **Baseada em Regras**: Aplicação de heurísticas para resolver conflitos simples
3. **Manual**: Solicitação de intervenção do usuário para casos complexos

## Considerações Técnicas

### Performance

- SQLite com Write-Ahead Logging (WAL) para otimizar concorrência
- Cache LRU para contextos frequentemente acessados
- Operações em background para não bloquear interface
- Parsing incremental para arquivos Markdown grandes

### Segurança

- Armazenamento local para dados sensíveis
- Filtragem de credenciais em logs
- Validação de conteúdo Markdown importado

### Extensibilidade

- Arquitetura de plugins para componentes opcionais
- Hooks para personalização de comportamentos
- API interna estável para adição de recursos 
- Formato Markdown extensível para metadados adicionais 