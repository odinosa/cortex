# Modelo de Dados do CORTEX

*Última atualização:* 07-07-2024

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
+---------------+     +----------------+
| tasks         |     | markers        |
+---------------+     +----------------+
       |
       |
       v
+---------------+
| task_relations|
+---------------+
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
- `NOTE`: Informação relevante

## Migrações

O CORTEX utiliza um sistema simples de migrações para criar e atualizar o banco de dados:

```python
def init_db():
    """Inicializa o banco de dados com o esquema inicial."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Criar tabelas
    cursor.executescript("""
        -- Tabela projects
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            -- campos...
        );
        
        -- Outras tabelas...
    """)
    
    conn.commit()
    conn.close()
```

## Evolução do Modelo

Este modelo é projetado para ser evolutivo:

1. **Fase 1**: Tabelas essenciais (projects, sessions, messages, tasks)
2. **Fase 2**: Relações de tarefas e marcadores
3. **Fase 3**: Contextos e regras avançadas 