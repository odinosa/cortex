# Exemplo: Desenvolvendo uma API REST com CORTEX

Este documento demonstra um fluxo de trabalho prático usando o CORTEX para gerenciar o desenvolvimento de uma API REST.

## 1. Iniciar o Projeto

Depois de configurar o CORTEX e o Cursor, abra o diretório do seu projeto e inicie uma nova sessão de trabalho:

```
/cortex:start "API REST FastAPI" "Desenvolver API REST de gerenciamento de usuários"
```

## 2. Estruturar as Tarefas do Projeto

Crie a hierarquia de tarefas usando o sistema de 4 níveis do CORTEX:

```
/cortex:task "Desenvolvimento da API" --level phase
```

Esta é a fase principal. Agora adicione etapas dentro desta fase:

```
/cortex:task "Configuração do Projeto" --level stage --parent 1
/cortex:task "Implementação de Modelos" --level stage --parent 1
/cortex:task "Implementação de Rotas" --level stage --parent 1
/cortex:task "Autenticação e Segurança" --level stage --parent 1
/cortex:task "Testes e Documentação" --level stage --parent 1
```

Adicione tarefas detalhadas para cada etapa:

```
# Tarefas para Configuração do Projeto
/cortex:task "Configurar estrutura do projeto FastAPI" --level task --parent 2
/cortex:task "Configurar banco de dados SQLAlchemy" --level task --parent 2
/cortex:task "Configurar sistema de migrations" --level task --parent 2

# Tarefas para Implementação de Modelos
/cortex:task "Implementar modelo de usuário" --level task --parent 3
/cortex:task "Implementar modelo de perfil" --level task --parent 3
/cortex:task "Implementar relacionamentos entre modelos" --level task --parent 3

# Continue para as outras etapas...
```

Para algumas tarefas mais complexas, adicione atividades específicas:

```
/cortex:task "Implementar validação de email" --level activity --parent 10
/cortex:task "Implementar hash de senha" --level activity --parent 10
```

## 3. Visualizar a Estrutura de Tarefas

Exporte as tarefas para Markdown para obter uma visão geral:

```
/cortex:export-tasks "plano-api-rest.md"
```

Conteúdo do arquivo gerado (exemplo):

```markdown
# Projeto: API REST FastAPI
*Atualizado: 09-07-2024*

## Fase: Desenvolvimento da API
- **Status:** not_started
- **Progresso:** 0%
- **Descrição:** Fase principal de desenvolvimento da API REST

### Etapa: Configuração do Projeto
- **Status:** not_started
- **Progresso:** 0%

#### Tarefa: Configurar estrutura do projeto FastAPI [ID:task_4]
- **Status:** not_started
- **Progresso:** 0%

#### Tarefa: Configurar banco de dados SQLAlchemy [ID:task_5]
- **Status:** not_started
- **Progresso:** 0%

#### Tarefa: Configurar sistema de migrations [ID:task_6]
- **Status:** not_started
- **Progresso:** 0%

### Etapa: Implementação de Modelos
- **Status:** not_started
- **Progresso:** 0%

...
```

## 4. Iniciar o Desenvolvimento

Comece a trabalhar nas tarefas, atualizando seu status conforme progride:

```
/cortex:task-status 4 in_progress --progress 20
```

Durante o desenvolvimento, adicione marcadores no código:

```python
# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # TODO: Adicionar validação de formato de email
    # TODO: Implementar relacionamento com perfil
```

## 5. Escanear e Vincular Marcadores

Escaneie o código em busca de marcadores:

```
/cortex:scan-markers
```

Vincule os marcadores encontrados às tarefas correspondentes:

```
/cortex:link-marker 1 10  # Vincula o marcador de validação de email à tarefa correspondente
/cortex:link-marker 2 12  # Vincula o marcador de relacionamento à tarefa correspondente
```

## 6. Colaboração via Markdown

Exporte as tarefas atualizadas para compartilhar com a equipe:

```
/cortex:export-tasks "plano-api-rest.md" --status all
```

Um membro da equipe pode editar o arquivo Markdown para adicionar detalhes e estimativas:

```markdown
#### Tarefa: Implementar modelo de usuário [ID:task_10]
- **Status:** in_progress
- **Progresso:** 60%
- **Estimativa:** 4 horas
- **Descrição:** Implementar o modelo SQLAlchemy para usuários com validações básicas
- **Responsável:** Alice

##### Atividade: Implementar validação de email [ID:task_15]
- **Status:** not_started
- **Progresso:** 0%
- **Estimativa:** 1 hora
- **Descrição:** Usar Pydantic ou validators do SQLAlchemy para validar formato de email
- **Responsável:** Bob
```

Importe as alterações de volta para o CORTEX:

```
/cortex:import-tasks "plano-api-rest.md"
```

## 7. Guardar e Restaurar Estado

No final do dia, salve o estado atual:

```
/cortex:save-state "api-dia-1"
```

Na próxima sessão, restaure o estado:

```
/cortex:resume <session_id>
/cortex:load-state "api-dia-1"
```

## 8. Analisar Progresso

Para obter um resumo do progresso atual:

```
/cortex:summarize
```

Saída (exemplo):
```
Resumo da Sessão "API REST FastAPI"
Duração: 8 horas
Progresso: 35% completo

Tarefas concluídas hoje:
- Configurar estrutura do projeto FastAPI ✓
- Configurar banco de dados SQLAlchemy ✓

Tarefas em andamento:
- Implementar modelo de usuário (60%)
- Implementar sistema de migrations (30%)

Próximos passos:
- Finalizar modelo de usuário
- Implementar validação de email
- Iniciar modelo de perfil

TODOs identificados: 5
```

## 9. Automação com Sincronização Contínua

Para manter a sincronização entre SQLite e Markdown durante todo o projeto:

```bash
# Configure sincronização automática
echo '#!/bin/bash
while true; do
  python -m cortex.cli sync-tasks "plano-api-rest.md" --auto-resolve=merge
  sleep 600  # A cada 10 minutos
done' > sync-api-tasks.sh

chmod +x sync-api-tasks.sh
./sync-api-tasks.sh &
```

## 10. Conectar com Sistema de Tickets

Se sua equipe usa Jira, configure a integração:

```bash
python -m cortex.cli config set jira_url "https://sua-empresa.atlassian.net"
python -m cortex.cli config set jira_project "API"
python -m cortex.cli config set jira_token "<seu-token>"
```

Sincronize tarefas específicas:

```
/cortex:sync-jira --task 10
```

## Conclusão

Este exemplo demonstra como o CORTEX pode ser integrado ao fluxo de trabalho de desenvolvimento de uma API REST, oferecendo:

1. Estruturação hierárquica de tarefas
2. Rastreamento de TODOs no código
3. Colaboração com outros membros da equipe via Markdown
4. Persistência de contexto entre sessões
5. Análise de progresso
6. Integração com sistemas externos 