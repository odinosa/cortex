# Modelo de Dados do CORTEX

*Última atualização:* 05-05-2025

Este documento descreve o modelo de dados do CORTEX, implementado em SQLite.

## Esquema SQLite

O CORTEX utiliza SQLite como solução de armazenamento por sua simplicidade, robustez e ausência de requisitos de servidor, o que o torna ideal para uso pessoal.

### Visão Geral das Tabelas

```
+---------------+     +----------------+     +---------------+
| projects      |<--->| sessions       |<--->| messages      |
+---------------+     +----------------+     +---------------+
       |                     |
       |                     |
       v                     v
+---------------+     +----------------+     +---------------+
| tasks         |<--->| markers        |<--->| code_analysis |
+---------------+     +----------------+     +---------------+
       |                     |                      |
       |                     |                      |
       v                     v                      v
+---------------+     +----------------+     +---------------+
| task_relations|<--->| markdown_sync  |<--->| suggestions   |
+---------------+     +----------------+     +---------------+
       |                     |                      |
       |                     |                      |
       v                     v                      v
+---------------+     +----------------+     +---------------+
| productivity  |<--->| automation_rules|<--->| system_metrics|
+---------------+     +----------------+     +---------------+
```

## Definições das Tabelas

### `projects`

Armazena informações sobre os projetos detectados e suas configurações.

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    workspace_path TEXT UNIQUE,
    description TEXT,
    jira_project_key TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN NOT NULL DEFAULT 1
);
```

### `sessions`

Armazena sessões de trabalho com início, fim e objetivos.

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    title TEXT NOT NULL,
    objective TEXT,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    summary TEXT,
    next_session_context TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### `messages`

Armazena as mensagens trocadas durante uma sessão.

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL, -- 'user', 'assistant', 'system', 'summary'
    content TEXT NOT NULL,
    token_count INTEGER,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### `tasks`

Armazena tarefas em hierarquia de 4 níveis.

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    parent_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    level TEXT NOT NULL, -- 'phase', 'stage', 'task', 'activity'
    status TEXT NOT NULL, -- 'not_started', 'in_progress', 'blocked', 'completed'
    progress INTEGER NOT NULL DEFAULT 0, -- 0-100
    jira_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    estimated_hours REAL,
    actual_hours REAL,
    order_index INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (parent_id) REFERENCES tasks(id)
);
```

### `task_relations`

Define relações entre tarefas além da hierarquia principal.

```sql
CREATE TABLE task_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_task_id INTEGER NOT NULL,
    target_task_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL, -- 'blocks', 'depends_on', 'related_to', 'duplicates'
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_task_id) REFERENCES tasks(id),
    FOREIGN KEY (target_task_id) REFERENCES tasks(id)
);
```

### `markers`

Armazena marcadores de continuidade extraídos dos arquivos.

```sql
CREATE TABLE markers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    task_id INTEGER,
    marker_type TEXT NOT NULL, -- 'TODO', 'FIXME', 'NOTE'
    content TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    context TEXT,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### `markdown_sync`

Armazena informações de sincronização entre SQLite e arquivos Markdown.

```sql
CREATE TABLE markdown_sync (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT NOT NULL, -- Hash do conteúdo do arquivo para detecção de mudanças
    last_sync_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sync_status TEXT NOT NULL, -- 'in_sync', 'sqlite_ahead', 'markdown_ahead', 'conflict'
    last_error TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE(project_id, file_path)
);
```

### `contexts`

Armazena contextos para diferentes projetos ou tarefas.

```sql
CREATE TABLE contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    task_id INTEGER,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### `rules`

Armazena regras a serem aplicadas em diferentes contextos.

```sql
CREATE TABLE rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    condition TEXT NOT NULL, -- JSON condition
    action TEXT NOT NULL, -- JSON action
    priority INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### `automation_rules`

Armazena regras para automação baseada em eventos e condições.

```sql
CREATE TABLE automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    trigger_event TEXT NOT NULL, -- 'task_created', 'marker_detected', 'session_started', etc.
    condition TEXT NOT NULL, -- JSON condition
    action TEXT NOT NULL, -- JSON action
    priority INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_triggered_at TIMESTAMP,
    trigger_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### `code_analysis`

Armazena resultados de análise do código-fonte.

```sql
CREATE TABLE code_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    analysis_type TEXT NOT NULL, -- 'complexity', 'pattern', 'metrics'
    analysis_data TEXT NOT NULL, -- JSON data
    score REAL, -- Normalized score (0-100)
    analyzed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### `suggestions`

Armazena sugestões geradas pelo sistema ou LLM.

```sql
CREATE TABLE suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    task_id INTEGER,
    session_id INTEGER,
    suggestion_type TEXT NOT NULL, -- 'task', 'refactoring', 'optimization'
    content TEXT NOT NULL,
    context TEXT,
    impact_score INTEGER NOT NULL DEFAULT 50, -- 0-100
    effort_score INTEGER NOT NULL DEFAULT 50, -- 0-100
    is_applied BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    applied_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### `productivity`

Armazena métricas de produtividade para análise.

```sql
CREATE TABLE productivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    session_id INTEGER,
    task_id INTEGER,
    metric_type TEXT NOT NULL, -- 'task_completion', 'focus_time', 'efficiency'
    value REAL NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT, -- JSON additional data
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### `system_metrics`

Armazena métricas do sistema para otimização.

```sql
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_usage REAL NOT NULL,
    memory_usage REAL NOT NULL,
    disk_usage REAL NOT NULL,
    battery_level REAL,
    is_on_battery BOOLEAN,
    db_size INTEGER NOT NULL, -- bytes
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### `cache_entries`

Gerencia o cache inteligente do sistema.

```sql
CREATE TABLE cache_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT UNIQUE NOT NULL,
    cache_value TEXT NOT NULL,
    use_count INTEGER NOT NULL DEFAULT 1,
    last_used_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

## Índices

```sql
-- Índices para performance
CREATE INDEX idx_sessions_project ON sessions(project_id);
CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_parent ON tasks(parent_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_markers_project ON markers(project_id);
CREATE INDEX idx_markers_task ON markers(task_id);
CREATE INDEX idx_contexts_project ON contexts(project_id);
CREATE INDEX idx_contexts_task ON contexts(task_id);
CREATE INDEX idx_markdown_sync_project ON markdown_sync(project_id);
CREATE INDEX idx_markdown_sync_filepath ON markdown_sync(file_path);

-- Índices adicionais para tarefas
CREATE INDEX idx_tasks_level ON tasks(level);
CREATE INDEX idx_tasks_progress ON tasks(progress);
CREATE INDEX idx_tasks_created ON tasks(created_at);
CREATE INDEX idx_tasks_updated ON tasks(updated_at);
CREATE INDEX idx_tasks_completed ON tasks(completed_at);
CREATE INDEX idx_tasks_level_status ON tasks(level, status);
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);

-- Índices adicionais para sincronização Markdown
CREATE INDEX idx_markdown_sync_status ON markdown_sync(sync_status);
CREATE INDEX idx_markdown_sync_last_sync ON markdown_sync(last_sync_time);
CREATE INDEX idx_markdown_sync_project_status ON markdown_sync(project_id, sync_status);

-- Índices para novas tabelas
CREATE INDEX idx_automation_rules_project ON automation_rules(project_id);
CREATE INDEX idx_automation_rules_event ON automation_rules(trigger_event);
CREATE INDEX idx_automation_rules_active ON automation_rules(is_active);

CREATE INDEX idx_code_analysis_project ON code_analysis(project_id);
CREATE INDEX idx_code_analysis_file ON code_analysis(file_path);
CREATE INDEX idx_code_analysis_type ON code_analysis(analysis_type);

CREATE INDEX idx_suggestions_project ON suggestions(project_id);
CREATE INDEX idx_suggestions_task ON suggestions(task_id);
CREATE INDEX idx_suggestions_session ON suggestions(session_id);
CREATE INDEX idx_suggestions_type ON suggestions(suggestion_type);
CREATE INDEX idx_suggestions_applied ON suggestions(is_applied);

CREATE INDEX idx_productivity_project ON productivity(project_id);
CREATE INDEX idx_productivity_session ON productivity(session_id);
CREATE INDEX idx_productivity_task ON productivity(task_id);
CREATE INDEX idx_productivity_type ON productivity(metric_type);
CREATE INDEX idx_productivity_recorded ON productivity(recorded_at);

CREATE INDEX idx_system_metrics_recorded ON system_metrics(recorded_at);
CREATE INDEX idx_system_metrics_battery ON system_metrics(is_on_battery);

CREATE INDEX idx_cache_entries_key ON cache_entries(cache_key);
CREATE INDEX idx_cache_entries_used ON cache_entries(last_used_at);
CREATE INDEX idx_cache_entries_expires ON cache_entries(expires_at);
```

## Relações

### Relações Hierárquicas

1. **Projeto > Sessão > Mensagem**:
   - Um projeto pode ter múltiplas sessões
   - Uma sessão contém múltiplas mensagens
   - Uma sessão pertence a um único projeto

2. **Projeto > Tarefa**:
   - Um projeto contém múltiplas tarefas
   - Uma tarefa pertence a um único projeto

3. **Tarefa > Sub-Tarefa**:
   - Uma tarefa pode ter múltiplas sub-tarefas
   - Uma tarefa pode ter uma tarefa pai
   - Hierarquia de 4 níveis: Fase > Etapa > Tarefa > Atividade

### Relações Adicionais

1. **Tarefa <-> Tarefa** (via `task_relations`):
   - Tarefas podem bloquear outras tarefas
   - Tarefas podem depender de outras tarefas
   - Tarefas podem estar relacionadas a outras tarefas
   - Tarefas podem duplicar outras tarefas

2. **Tarefa <-> Marcador**:
   - Uma tarefa pode ter múltiplos marcadores
   - Um marcador pode estar associado a uma tarefa

3. **Projeto <-> Markdown** (via `markdown_sync`):
   - Um projeto pode estar associado a múltiplos arquivos Markdown
   - Um arquivo Markdown está associado a um único projeto
   - Esta relação rastreia o estado de sincronização entre o banco de dados e os arquivos Markdown

4. **Projeto <-> Regras de Automação**:
   - Um projeto pode ter múltiplas regras de automação
   - Uma regra de automação está associada a um único projeto ou é global
   - As regras podem ser ativadas ou desativadas individualmente

5. **Projeto <-> Análise de Código**:
   - Um projeto contém múltiplos resultados de análise de código
   - Cada resultado de análise está associado a um arquivo específico
   - Resultados podem ser de diferentes tipos (complexidade, padrões, métricas)

6. **Projeto/Tarefa/Sessão <-> Sugestões**:
   - Sugestões podem estar associadas a um projeto, tarefa ou sessão
   - Uma sugestão tem um tipo que indica sua natureza (tarefa, refatoração, otimização)
   - Sugestões têm pontuações de impacto e esforço para priorização

7. **Projeto/Sessão/Tarefa <-> Produtividade**:
   - Métricas de produtividade podem estar associadas a projetos, sessões ou tarefas
   - As métricas são registradas ao longo do tempo para análise de tendências
   - Diferentes tipos de métricas capturam diferentes aspectos da produtividade

## Convenções de Dados

### Níveis de Tarefa

1. **Fase**: Maior nível de organização (ex: "MVP Backend")
2. **Etapa**: Agrupamento lógico de tarefas (ex: "Implementação de Modelos")
3. **Tarefa**: Unidade de trabalho (ex: "Criar modelo de usuário")
4. **Atividade**: Passo específico (ex: "Adicionar validação de email")

### Estados de Tarefa

- `not_started`: Ainda não iniciada
- `in_progress`: Em andamento
- `blocked`: Bloqueada por alguma dependência
- `completed`: Concluída

### Tipos de Marcadores

- `TODO`: Item a fazer
- `FIXME`: Problema que precisa ser corrigido
- `NOTE`: Informação importante

### Estados de Sincronização Markdown

- `in_sync`: Sistema interno e arquivo de visualização estão sincronizados
- `sqlite_ahead`: Alterações internas ainda não exportadas para visualização
- `markdown_ahead`: Alterações no arquivo de visualização ainda não importadas para o sistema
- `conflict`: Conflito entre alterações internas e no arquivo de visualização

### Tipos de Eventos para Automação

- `task_created`: Uma nova tarefa foi criada
- `task_updated`: Uma tarefa existente foi atualizada
- `task_completed`: Uma tarefa foi marcada como concluída
- `marker_detected`: Um novo marcador foi detectado no código
- `session_started`: Uma nova sessão foi iniciada
- `session_ended`: Uma sessão foi encerrada
- `system_idle`: O sistema está ocioso
- `system_low_resources`: O sistema está com poucos recursos
- `scheduled_time`: Evento agendado (cron-like)

### Tipos de Análise de Código

- `complexity`: Análise de complexidade ciclomática, cognitiva, etc.
- `pattern`: Detecção de padrões e anti-padrões
- `duplication`: Análise de código duplicado
- `metrics`: Métricas gerais (linhas de código, relação comentários/código, etc.)
- `quality`: Análise geral de qualidade e conformidade com padrões

### Tipos de Sugestões

- `task`: Sugestão de nova tarefa a ser criada
- `refactoring`: Sugestão de refatoração de código
- `optimization`: Sugestão de otimização de performance
- `documentation`: Sugestão relacionada a documentação
- `process`: Sugestão relacionada ao processo de trabalho

### Métricas de Produtividade

- `task_completion`: Taxa de conclusão de tarefas
- `focus_time`: Tempo focado em uma tarefa
- `efficiency`: Relação entre tempo estimado e real
- `velocity`: Tarefas completadas por unidade de tempo
- `quality`: Medidas relacionadas à qualidade do trabalho entregue

## Sistema Inteligente de Cache

O CORTEX implementa um sistema de cache adaptativo para melhorar a performance sem comprometer recursos:

### Principais Características do Cache

1. **Políticas de Expiração**:
   - Baseada em tempo: entradas expiram após um determinado período
   - Baseada em uso: itens pouco utilizados são descartados primeiro
   - Adaptativa: ajusta automaticamente com base nos padrões de uso

2. **Estratégias de Armazenamento**:
   - Em memória para performance (tamanho limitado)
   - Em SQLite para persistência (com limite configurável)

3. **Tipos de Dados Armazenados**:
   - Consultas frequentes
   - Resultados de análise
   - Contextos de trabalho
   - Configurações

4. **Monitoramento de Performance**:
   - Taxa de acertos/erros
   - Tempo médio de acesso
   - Economia de recursos estimada

### Implementação Técnica

A tabela `cache_entries` armazena os itens em cache com metadados que permitem ao sistema tomar decisões inteligentes sobre quais itens manter e quais descartar:

- `cache_key`: Identificador único da entrada
- `cache_value`: Valor armazenado (geralmente serializado como JSON)
- `use_count`: Contador de uso para identificar itens frequentemente acessados
- `last_used_at`: Timestamp do último acesso para política LRU
- `created_at`: Timestamp de criação
- `expires_at`: Timestamp de expiração (NULL para itens sem expiração definida)

## Sistema de Automação Baseado em Regras

O sistema de automação do CORTEX utiliza um mecanismo flexível baseado em regras que permite configurar comportamentos automáticos sem necessidade de programação:

### Estrutura de Regras

Cada regra é composta por:

1. **Trigger (Acionador)**: Especifica o evento que ativa a regra
2. **Condition (Condição)**: Expressão lógica que determina se a ação deve ser executada
3. **Action (Ação)**: Operação a ser realizada quando a condição é atendida

### Formato JSON de Condições

Condições são expressas em formato JSON que permite combinações lógicas complexas:

```json
{
  "operator": "and",
  "conditions": [
    {
      "field": "task.level",
      "op": "eq",
      "value": "activity"
    },
    {
      "field": "project.name",
      "op": "contains",
      "value": "CORTEX"
    },
    {
      "operator": "or",
      "conditions": [
        {
          "field": "marker.type",
          "op": "eq",
          "value": "TODO"
        },
        {
          "field": "marker.type",
          "op": "eq",
          "value": "FIXME"
        }
      ]
    }
  ]
}
```

### Formato JSON de Ações

Ações são expressas em formato JSON que especifica o tipo de ação e seus parâmetros:

```json
{
  "action": "create_task",
  "parameters": {
    "title": "Resolver {marker.content}",
    "level": "activity",
    "status": "not_started",
    "parent_id": "{task.id}",
    "description": "Gerado automaticamente a partir do marcador em {marker.file_path}:{marker.line_number}"
  }
}
```

### Exemplos de Regras Automáticas

1. **Criação de Tarefas a partir de Marcadores**:
   - Trigger: `marker_detected`
   - Condition: `marker.type == "TODO"`
   - Action: `create_task` com título e descrição baseados no marcador

2. **Notificação de Tarefas Bloqueadas**:
   - Trigger: `task_updated`
   - Condition: `task.status == "blocked" && task.level == "task"`
   - Action: `notify` com detalhes sobre a tarefa bloqueada

3. **Otimização de Banco de Dados**:
   - Trigger: `system_idle`
   - Condition: `system.cpu_usage < 10% && system.is_on_power`
   - Action: `optimize_database`

## Sistema de Análise e Sugestões

O CORTEX implementa um sistema de análise e sugestões que detecta padrões no código e no fluxo de trabalho:

### Análise de Código

O sistema analisa periodicamente o código-fonte e armazena os resultados na tabela `code_analysis`:

1. **Complexidade**:
   - Análise de complexidade ciclomática
   - Detecção de funções/métodos excessivamente complexos
   - Sugestões de refatoração

2. **Padrões e Anti-padrões**:
   - Detecção de práticas recomendadas
   - Identificação de anti-padrões comuns
   - Sugestões de melhoria

3. **Duplicação**:
   - Detecção de código duplicado ou similar
   - Sugestões para extração de funções/componentes comuns

### Sugestões Inteligentes

O sistema gera sugestões baseadas na análise de código e no histórico de trabalho:

1. **Tarefas Recomendadas**:
   - Baseadas em padrões de trabalho anterior
   - Priorizadas por impacto e esforço
   - Relacionadas ao contexto atual

2. **Refatorações Sugeridas**:
   - Baseadas em análise de código
   - Focadas em melhorias de qualidade
   - Com estimativas de esforço e impacto

### Integração com LLM

O sistema enriquece as sugestões usando o LLM:

1. **Geração de Descrições**:
   - Descrições detalhadas para tarefas
   - Explicações claras para refatorações

2. **Contextualização**:
   - Alinhamento com o projeto como um todo
   - Explicação do raciocínio por trás das sugestões

## Sistema de Métricas de Produtividade

O CORTEX coleta e analisa métricas de produtividade para fornecer insights sobre o fluxo de trabalho:

### Métricas Coletadas

1. **Tempo por Tarefa**:
   - Tempo total gasto em cada tarefa
   - Comparação entre tempo estimado e real
   - Distribuição de tempo entre diferentes níveis de tarefas

2. **Velocidade de Conclusão**:
   - Tarefas concluídas por dia/semana
   - Tendências ao longo do tempo
   - Comparação entre diferentes tipos de tarefas

3. **Padrões de Trabalho**:
   - Horários mais produtivos
   - Distribuição de atividade ao longo do dia
   - Identificação de períodos de foco prolongado

### Visualização e Análise

O sistema oferece visualizações claras das métricas:

1. **Dashboard em Terminal**:
   - Gráficos ASCII/Unicode para visualização rápida
   - Resumos diários/semanais
   - Indicadores de produtividade

2. **Tendências**:
   - Análise de tendências ao longo do tempo
   - Identificação de melhorias ou quedas na produtividade
   - Correlação com mudanças no fluxo de trabalho

### Insights Automáticos

O sistema gera insights baseados nas métricas coletadas:

1. **Recomendações de Fluxo de Trabalho**:
   - Sugestões para otimizar horários de trabalho
   - Recomendações sobre duração de sessões
   - Dicas para melhorar a produtividade

2. **Feedbacks Personalizados**:
   - Reconhecimento de conquistas
   - Alertas sobre possíveis problemas
   - Sugestões adaptadas ao perfil de trabalho

## Sistema de Monitoramento e Otimização

O CORTEX monitora o sistema e otimiza seu próprio funcionamento:

### Métricas Monitoradas

1. **Recursos do Sistema**:
   - Uso de CPU e memória
   - Espaço em disco
   - Nível de bateria e estado de energia

2. **Performance do Banco de Dados**:
   - Tamanho do banco
   - Tempo de consultas
   - Fragmentação

### Estratégias de Otimização

1. **Modo Econômico**:
   - Redução de operações em background quando na bateria
   - Adiamento de análises intensivas para períodos de ociosidade

2. **Manutenção Automática**:
   - VACUUM automático do SQLite
   - Limpeza de dados temporários
   - Otimização de índices

### Backup Incremental

O sistema implementa um mecanismo de backup incremental:

1. **Detecção de Alterações**:
   - Rastreamento de mudanças desde o último backup
   - Cálculo de diferenças

2. **Geração de Scripts**:
   - Criação de scripts SQL incrementais
   - Rotação de backups

3. **Sincronização Remota**:
   - Opção para sincronizar com servidor remoto via SSH
   - Verificação de integridade

## Exemplos de Consultas SQLite Comuns

### Listar Tarefas de um Projeto

```sql
SELECT id, title, level, status, progress 
FROM tasks 
WHERE project_id = ? 
ORDER BY level, order_index;
```

### Encontrar Marcadores Não Resolvidos

```sql
SELECT m.id, m.content, m.file_path, m.line_number, t.title as task_title
FROM markers m
LEFT JOIN tasks t ON m.task_id = t.id
WHERE m.project_id = ? AND m.resolved_at IS NULL;
```

### Obter Estado de Sincronização Markdown

```sql
SELECT file_path, sync_status, last_sync_time 
FROM markdown_sync 
WHERE project_id = ?;
```

### Rastrear Progresso de Tarefas

```sql
SELECT 
  level,
  COUNT(*) as total_tasks,
  SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
  AVG(progress) as avg_progress
FROM tasks
WHERE project_id = ?
GROUP BY level;
```

### Consultar Regras de Automação Ativas

```sql
SELECT id, name, trigger_event, priority 
FROM automation_rules 
WHERE is_active = 1 AND (project_id = ? OR project_id IS NULL) 
ORDER BY priority DESC, trigger_event;
```

### Obter Sugestões Não Aplicadas

```sql
SELECT id, suggestion_type, content, impact_score, effort_score 
FROM suggestions 
WHERE project_id = ? AND is_applied = 0 
ORDER BY (impact_score - effort_score) DESC;
```

### Analisar Tendências de Produtividade

```sql
SELECT 
  DATE(recorded_at) as date,
  metric_type,
  AVG(value) as avg_value
FROM productivity
WHERE project_id = ? AND recorded_at >= DATE('now', '-30 days')
GROUP BY DATE(recorded_at), metric_type
ORDER BY DATE(recorded_at);
```

### Identificar Arquivos com Problemas

```sql
SELECT 
  file_path,
  MAX(CASE WHEN analysis_type = 'complexity' THEN score END) as complexity_score,
  MAX(CASE WHEN analysis_type = 'pattern' THEN score END) as pattern_score,
  MAX(CASE WHEN analysis_type = 'duplication' THEN score END) as duplication_score
FROM code_analysis
WHERE project_id = ? AND analyzed_at >= DATE('now', '-7 days')
GROUP BY file_path
HAVING complexity_score > 70 OR pattern_score > 70 OR duplication_score > 70
ORDER BY (COALESCE(complexity_score, 0) + COALESCE(pattern_score, 0) + COALESCE(duplication_score, 0)) DESC;
```

### Monitorar Performance do Sistema

```sql
SELECT 
  DATE(recorded_at) as date,
  AVG(cpu_usage) as avg_cpu,
  AVG(memory_usage) as avg_memory,
  MAX(db_size) as max_db_size
FROM system_metrics
WHERE recorded_at >= DATE('now', '-7 days')
GROUP BY DATE(recorded_at)
ORDER BY DATE(recorded_at);
```

## Evolução do Modelo

Este modelo é projetado para ser evolutivo, com um plano claro de expansão:

1. **Fase 1**: Tabelas essenciais (projects, sessions, messages, tasks)
2. **Fase 2**: Relações de tarefas e marcadores
3. **Fase 3**: Modelo completo incluindo contextos, regras e sincronização Markdown
4. **Fase 4**: Extensões para automação, análise e sugestões inteligentes
5. **Fase 5 (planejada)**: Machine learning para personalização avançada e previsão de padrões 