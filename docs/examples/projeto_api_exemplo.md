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

Alternativamente, use o dashboard para visualização rápida:

```
/cortex:dashboard
```

Isso mostrará uma visão geral do progresso do projeto diretamente no terminal:

```
╭───────────────────────────────────────────────────────────╮
│                 API REST FastAPI Dashboard                 │
├───────────────────────────────────────────────────────────┤
│ Progresso Geral: [████████░░░░░░░░░░░░░░░░░░░░] 32%       │
│                                                           │
│ Por Nível:                                                │
│ ├─ Fases:     [██████████░░░░░░░░░░░░░░] 40%              │
│ ├─ Etapas:    [████████░░░░░░░░░░░░░░░░] 35%              │
│ ├─ Tarefas:   [██████░░░░░░░░░░░░░░░░░░] 25%              │
│ └─ Atividades:[████░░░░░░░░░░░░░░░░░░░░] 20%              │
│                                                           │
│ TODOs Pendentes: 8  │  Marcadores Não Vinculados: 3       │
│                                                           │
│ Próximas Tarefas Sugeridas:                               │
│ 1. Implementar validação de email                         │
│ 2. Configurar sistema de migrations                       │
│ 3. Implementar hash de senha                              │
╰───────────────────────────────────────────────────────────╯
```

## 4. Configurar Automações

Configure automações para auxiliar no fluxo de trabalho:

```
# Criar automação para gerar tarefas a partir de TODOs no código
/cortex:automate create "todo-tarefas" --event "marker_detected" --condition "marker.type == 'TODO'" --action "create_task" --params "title=Resolver {marker.content},level=activity"

# Configurar notificação para tarefas bloqueadas
/cortex:automate create "notificacao-bloqueio" --event "task_updated" --condition "task.status == 'blocked'" --action "notify" --params "message=Atenção: Tarefa {task.title} está bloqueada"

# Configurar otimização de banco durante ociosidade
/cortex:automate create "otimizacao" --event "system_idle" --condition "system.cpu_usage < 15" --action "optimize_database"
```

## 5. Iniciar o Desenvolvimento

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

## 6. Analisar o Código

Analise o código para identificar problemas e oportunidades de melhoria:

```
# Analisar complexidade do código
/cortex:analyze complexity ./app

# Detectar padrões e anti-padrões
/cortex:analyze patterns ./app

# Verificar duplicações
/cortex:analyze duplication ./app
```

Exemplo de saída da análise de complexidade:

```
Análise de Complexidade Concluída
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Arquivos Analisados: 12
Funções/Métodos: 28
Complexidade Média: 5.7

Componentes de Alta Complexidade:
- app/auth/jwt.py:verify_token (Complexidade: 14) ⚠️
- app/routes/users.py:create_user (Complexidade: 11)
- app/database.py:get_db_session (Complexidade: 8)

Sugestões de Refatoração:
1. Dividir função verify_token em funções menores
2. Simplificar validações em create_user
3. Extrair lógica de tratamento de erros em get_db_session
```

## 7. Obter Sugestões Inteligentes

Obtenha sugestões baseadas na análise de código e no estado atual do projeto:

```
# Obter sugestões gerais
/cortex:suggest

# Obter sugestões específicas para refatoração
/cortex:suggest refactoring --path ./app/auth/jwt.py
```

Exemplo de sugestões:

```
Sugestões para o Projeto
━━━━━━━━━━━━━━━━━━━━━━━━

1. Refatoração: Dividir função verify_token
   Impacto: Alto | Esforço: Médio
   Descrição: Extrair validação de payload para função separada

2. Nova Tarefa: Adicionar testes para modelos
   Impacto: Alto | Esforço: Baixo
   Descrição: Os modelos User e Profile não possuem testes

3. Processo: Configurar automação para testes
   Impacto: Médio | Esforço: Baixo
   Descrição: Adicionar automação para rodar testes em idle
```

## 8. Escanear e Vincular Marcadores

Escaneie o código em busca de marcadores:

```
/cortex:scan-markers
```

A automação configurada anteriormente criará tarefas automaticamente para os TODOs encontrados, mas você também pode vincular manualmente:

```
/cortex:link-marker 1 10  # Vincula o marcador de validação de email à tarefa correspondente
/cortex:link-marker 2 12  # Vincula o marcador de relacionamento à tarefa correspondente
```

## 9. Monitorar Produtividade

Acompanhe métricas de produtividade para otimizar seu fluxo de trabalho:

```
# Ver métricas de conclusão de tarefas
/cortex:metrics completion-rate

# Analisar tempo gasto por tarefa
/cortex:metrics task-time

# Identificar horários mais produtivos
/cortex:metrics productive-hours
```

Exemplo de visualização de períodos produtivos:

```
Análise de Períodos Produtivos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Horários mais produtivos (tarefas/hora):
09:00-11:00: ████████████ (2.4)
14:00-16:00: █████████ (1.8)
20:00-22:00: ██████ (1.2)

Dias mais produtivos:
Terça: ████████████ (12 tarefas)
Quinta: █████████ (9 tarefas)
Segunda: ████████ (8 tarefas)

Recomendação: Concentrar tarefas complexas entre 9-11h
```

## 10. Colaboração via Markdown

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

## 11. Otimizar o Sistema

Monitore e otimize o sistema durante o desenvolvimento:

```
# Verificar status do sistema
/cortex:system status

# Ativar modo econômico em bateria
/cortex:system eco-mode auto

# Otimizar manualmente o banco de dados
/cortex:system optimize-db
```

Exemplo de saída de status do sistema:

```
Status do Sistema CORTEX
━━━━━━━━━━━━━━━━━━━━━━

CPU: 12% | Memória: 145MB | Disco: 78MB
Bateria: 65% (modo econômico: ativado)
Tamanho do Banco: 6.2MB (última otimização: há 3 horas)
Cache: 24MB (hit ratio: 87%)

Recomendações:
- Limpar cache antigo (>7 dias): Economizaria 8MB
- Executar VACUUM no banco: Potencial redução de 15%
```

## 12. Backup e Sincronização

Configure backup incremental e sincronização:

```bash
# Configurar backup incremental
python -m cortex.cli config set backups.type incremental
python -m cortex.cli config set backups.interval daily

# Configurar sincronização remota
python -m cortex.cli remote setup --host usuario@servidor --path /backups/api-project
```

Execute backup manual:

```
/cortex:backup --incremental
```

## 13. Guardar e Restaurar Estado

No final do dia, salve o estado atual:

```
/cortex:save-state "api-dia-1"
```

Na próxima sessão, restaure o estado:

```
/cortex:resume <session_id>
/cortex:load-state "api-dia-1"
```

## 14. Analisar Progresso

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
Complexidade média do código: 4.8
Sugestões pendentes: 3

Insights:
- Seu ritmo está 15% acima da média
- Período mais produtivo foi entre 9-11h
- Concentre-se em refatorações amanhã
```

## 15. Utilizar Insights Automatizados

Obtenha insights sobre seu fluxo de trabalho:

```
/cortex:insights workflow-suggestions
```

Exemplo de saída:

```
Insights de Fluxo de Trabalho
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Com base em seus padrões de trabalho:

1. Você resolve 30% mais tarefas quando trabalha em blocos de 90 minutos
2. Tarefas de implementação são mais eficientes quando feitas pela manhã
3. Documentação e testes são mais eficientes à tarde
4. Você frequentemente subestima tarefas de autenticação (43% mais longas)

Sugestões:
- Agende blocos de implementação para 9-11h
- Reserve períodos de 30min para revisão de código após o almoço
- Adicione 40% no tempo estimado para tarefas de autenticação
```

## Conclusão

Este exemplo demonstra como o CORTEX pode ser integrado ao fluxo de trabalho de desenvolvimento de uma API REST, oferecendo:

1. Estruturação hierárquica de tarefas
2. Automação inteligente baseada em eventos
3. Análise avançada de código
4. Sugestões contextuais para melhorias
5. Monitoramento de produtividade com insights
6. Otimização de sistema e recursos
7. Rastreamento de TODOs no código
8. Colaboração com outros membros da equipe via Markdown
9. Persistência de contexto entre sessões
10. Backup incremental e sincronização remota 