# Arquitetura do CORTEX

*Última atualização:* 05-05-2025

Este documento descreve a arquitetura técnica do CORTEX, um sistema MCP (Model Context Protocol) para gestão de contexto e tarefas no ambiente Cursor.

## Principais Componentes

O CORTEX adota uma arquitetura modular e leve, focada em simplicidade e responsividade:

1. **MCP Server** - Interface com o Cursor via stdio
2. **Core Engine** - Lógica de negócio e gestão de estado
3. **SQLite Store** - Armazenamento persistente local
4. **Markdown Sync** - Sistema de sincronização bidirecional SQLite-Markdown
5. **CLI** - Interface de linha de comando para administração
6. **Automation System** - Motor de automação e regras inteligentes
7. **Analysis Engine** - Sistema de análise de código e sugestões
8. **LLM Integration** - Assistente proativo e geração de insights

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
                                                  │
                                                  │
                                                  ▼
┌─────────────────┐                 ┌─────────────────────────┐                ┌──────────────┐
│  Analysis       │◄───────────────►│    Automation System    │◄───────────────│  LLM         │
│  Engine         │                 │                         │                │  Integration  │
└─────────────────┘                 └─────────────────────────┘                └──────────────┘
                                                  │
                                                  │
                                                  ▼
                                     ┌─────────────────────────┐
                                     │    System Monitor       │
                                     └─────────────────────────┘
```

## Fluxo de Dados

### 1. Fluxo de Comunicação MCP

1. O Cursor envia uma solicitação MCP via stdin com nome da ferramenta e argumentos
2. O MCP Server do CORTEX recebe e processa a solicitação
3. O Core Engine aplica a lógica de negócio necessária
4. As alterações são persistidas no SQLite Store quando aplicável
5. O resultado é enviado de volta para o Cursor via stdout
6. O Cursor apresenta a resposta ao utilizador

### 2. Detecção de Workspace

1. O CORTEX inicia quando o Cursor abre
2. O sistema detecta o arquivo de workspace aberto
3. Identifica e carrega o projeto associado ao workspace
4. Carrega contexto específico do projeto
5. Determina tarefas pendentes para o projeto atual

### 3. Gestão de Sessão

1. Utilizador inicia sessão via comando `/cortex:start`
2. Sistema carrega contexto e tarefas pendentes
3. Sessão registra interações e alterações durante o desenvolvimento
4. Ao finalizar, sistema atualiza estado das tarefas e cria contexto para próxima sessão

### 4. Fluxo Híbrido SQLite + Markdown

1. Utilizador executa comando de exportação (`/cortex:export-tasks`)
2. Sistema converte tarefas do SQLite para formato Markdown estruturado
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
  - `automation_tools.py` - Ferramentas de automação e inteligência

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
- `automation/` - Sistema de automação inteligente
  - `trigger.py` - Detecção de eventos e acionadores
  - `condition.py` - Avaliação de condições 
  - `action.py` - Execução de ações automatizadas
  - `event_bus.py` - Sistema de eventos e listeners

### Persistência (`cortex.storage`)

Gerencia armazenamento de dados:

- `database.py` - Interface com SQLite
- `cache.py` - Sistema de cache inteligente com política LRU e adaptativa
- `models/` - Definição dos modelos de dados
  - `session.py`
  - `task.py`
  - `context.py`
  - `marker.py`
  - `rule.py`
  - `markdown_sync.py` - Modelo para rastreamento de sincronização Markdown
  - `automation_rule.py` - Modelo para regras de automação
- `dao/` - Objetos de acesso a dados
  - `session_dao.py`
  - `task_dao.py`
  - `context_dao.py`
  - `markdown_sync_dao.py` - DAO para operações de sincronização
  - `automation_dao.py` - DAO para operações de automação

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
- `dashboard.py` - Dashboard em terminal para visualização de status
- `metrics.py` - Visualização de métricas e estatísticas

### Analysis Engine (`cortex.analysis`)

Sistema para análise de código e sugestões inteligentes:

- `analyzer.py` - Interface principal para análise
- `complexity.py` - Análise de complexidade de código
- `pattern_detector.py` - Detecção de padrões e anti-padrões
- `code_metrics.py` - Cálculo de métricas de código
- `suggestion.py` - Geração de sugestões de melhorias

### LLM Integration (`cortex.llm`)

Integração com modelos de linguagem para assistência proativa:

- `assistant.py` - Assistente inteligente
- `suggestion.py` - Geração de sugestões para tarefas
- `summarizer.py` - Geração de resumos automáticos
- `context_enhancer.py` - Enriquecimento de contexto

### System Monitor (`cortex.system`)

Monitoramento e otimização de recursos do sistema:

- `monitor.py` - Verificação de recursos do sistema
- `optimizer.py` - Otimização automática de recursos
- `backup.py` - Sistema de backup incremental
- `sync.py` - Sincronização com sistemas remotos (SSH)

### Plugins (`cortex.plugins`)

Sistema leve de plugins para extensibilidade:

- `loader.py` - Carregador de plugins
- `registry.py` - Registro e gerenciamento de plugins
- `api.py` - API para desenvolvimento de plugins

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

## Modelo de Concorrência

O CORTEX implementa um modelo de concorrência baseado em eventos que equilibra responsividade com simplicidade:

1. **MCP Server**:
   - Opera em um processo único dedicado
   - Utiliza um loop de eventos baseado em `asyncio` para I/O não-bloqueante
   - Comunicação stdio são geridas como streams assíncronos

2. **Operações de Longa Duração**:
   - Processamento de marcadores e scanning de arquivos grandes são executados em threads separadas
   - Sistema de filas para operações pesadas, evitando bloqueio da interface principal
   - Implementação de timeouts para operações potencialmente bloqueantes

3. **Acesso a SQLite**:
   - Conexões pooling para evitar contenção
   - Modo WAL (Write-Ahead Logging) habilitado por padrão
   - Transações explícitas para operações em lote

4. **Operações em Markdown**:
   - Parsing e escrita de arquivos Markdown em threads dedicadas
   - Sistema de notificação baseado em eventos para atualizações de UI

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

### Diagrama de Fluxo de Sincronização

```
┌────────────┐         ┌────────────┐        ┌────────────┐
│  SQLite DB │◄────────┤ Diff Engine├───────►│ Markdown   │
└─────┬──────┘         └────────────┘        └──────┬─────┘
      │                       ▲                     │
      │                       │                     │
      ▼                       │                     ▼
┌─────────────┐        ┌──────────────┐     ┌──────────────┐
│ DAO/Queries │        │Conflict Solver│     │ Parser/Writer│
└─────┬───────┘        └──────────────┘     └──────┬───────┘
      │                       ▲                    │
      │                       │                    │
      ▼                       │                    ▼
┌─────────────┐               │              ┌────────────┐
│ Task Models │───────────────┴──────────────│   MD View  │
└─────────────┘                              └────────────┘
```

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
3. **Manual**: Solicitação de intervenção do utilizador para casos complexos

## Considerações Técnicas

### Performance

- SQLite com Write-Ahead Logging (WAL) para otimizar concorrência
- Cache LRU adaptativo para contextos e dados frequentemente acessados
- Operações em background para não bloquear interface
- Parsing incremental para arquivos Markdown grandes
- Sistema de monitoramento de recursos para otimização automática
- Modo econômico para execução em bateria

### Segurança

- Armazenamento local para dados sensíveis
- Filtragem de credenciais em logs
- Validação de conteúdo Markdown importado
- Comunicação segura via SSH para componentes remotos

### Extensibilidade

- Arquitetura de plugins para componentes opcionais
- Hooks para personalização de comportamentos
- API interna estável para adição de recursos 
- Formato Markdown extensível para metadados adicionais
- Sistema de automação baseado em triggers, condições e ações

## Mecanismos de Inteligência Automática

### Sistema de Automação

O CORTEX implementa um sistema de automação inteligente baseado no padrão evento-condição-ação:

1. **Eventos (Triggers)**: 
   - Criação de tarefas
   - Detecção de marcadores
   - Atualização de sessão
   - Alterações no código-fonte
   - Tempo programado (cronômetros)

2. **Condições**:
   - Expressões lógicas avaliando propriedades de objetos
   - Verificações de contexto (tipo de projeto, linguagem)
   - Estado atual do sistema

3. **Ações**:
   - Criação automática de tarefas
   - Atualização de status
   - Geração de relatórios
   - Notificações
   - Execução de comandos do sistema

O sistema utiliza um barramento de eventos central (`EventBus`) para distribuir eventos para os listeners apropriados, que então avaliam as condições e executam ações conforme necessário.

### Análise de Código

O motor de análise realiza:

1. **Varredura Periódica**:
   - Executada em segundo plano em intervalos configuráveis
   - Mais intensiva durante períodos de baixa utilização da CPU

2. **Detecção de Padrões**:
   - Práticas recomendadas
   - Anti-padrões comuns
   - Duplicação de código
   - Complexidade excessiva

3. **Sugestões Contextuais**:
   - Refatorações sugeridas baseadas no contexto
   - Priorização por impacto/esforço

### Integração com LLM

A integração com o LLM permite:

1. **Assistência Proativa**:
   - Sugestão de próximas tarefas
   - Geração de resumos de sessão
   - Melhoria de descrições de tarefas

2. **Análise de Produtividade**:
   - Identificação de padrões de trabalho eficientes
   - Sugestões para otimização do fluxo de trabalho
   - Análise de tendências e métricas

3. **Contexto Inteligente**:
   - Enriquecimento de contexto para o LLM
   - Priorização de informações relevantes

## Visualização e Métricas

### Dashboard no Terminal

O CORTEX inclui um dashboard em terminal para visualização rápida:

1. **Status de Projeto**:
   - Progresso de tarefas por nível
   - Bloqueiros ativos
   - Próximas tarefas recomendadas

2. **Métricas de Produtividade**:
   - Tempo gasto por tarefa
   - Velocidade de conclusão
   - Tendências ao longo do tempo

3. **Recursos do Sistema**:
   - Uso de CPU/memória
   - Tamanho do banco de dados
   - Estado de otimização

O dashboard usa caracteres ASCII/Unicode para visualização compatível com qualquer terminal, garantindo leveza e simplicidade.

## Relação com Comandos do Usuário

Os comandos que o utilizador invoca no Cursor (formato `/cortex:comando`) são mapeados para chamadas de ferramentas MCP internas:

| Comando do Usuário | Ferramenta MCP Interna | Componentes Envolvidos |
|--------------------|------------------------|------------------------|
| `/cortex:start`    | `start_session`        | MCP Server, Core Engine (session.py), SQLite Store |
| `/cortex:task`     | `create_task`          | MCP Server, Core Engine (task.py), SQLite Store |
| `/cortex:export-tasks` | `export_tasks_markdown` | MCP Server, Markdown Sync (exporter.py) |
| `/cortex:import-tasks` | `import_tasks_markdown` | MCP Server, Markdown Sync (importer.py) |
| `/cortex:scan-markers` | `scan_markers`      | MCP Server, Core Engine (markers.py) |
| `/cortex:analyze`  | `analyze_code`        | MCP Server, Analysis Engine (analyzer.py) |
| `/cortex:suggest`  | `suggest_next_tasks`  | MCP Server, LLM Integration (assistant.py) |
| `/cortex:dashboard` | `show_dashboard`     | MCP Server, CLI (dashboard.py) |
| `/cortex:automate` | `manage_automation`   | MCP Server, Core Engine (automation/) |

Cada comando é processado seguindo o mesmo fluxo básico através da arquitetura, com variações dependendo da operação específica. 