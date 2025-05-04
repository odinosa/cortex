# Guia de Utilização do CORTEX

*Última atualização:* 05-05-2025

Este guia fornece instruções completas para instalar, configurar e utilizar o CORTEX no seu fluxo de trabalho de desenvolvimento.

## Índice

- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Passos de Instalação](#passos-de-instalação)
- [Primeiros Passos](#primeiros-passos)
  - [Integração com Cursor](#integração-com-cursor)
  - [Iniciar uma Sessão](#iniciar-uma-sessão)
- [Fluxo de Trabalho Diário](#fluxo-de-trabalho-diário)
  - [1. Início do Dia](#1-início-do-dia)
  - [2. Durante o Desenvolvimento](#2-durante-o-desenvolvimento)
  - [3. Planejamento e Revisão](#3-planejamento-e-revisão)
  - [4. Final do Dia](#4-final-do-dia)
- [Gestão de Tarefas](#gestão-de-tarefas)
  - [Comandos de Tarefas](#comandos-de-tarefas)
- [Sistema Flexível de Gestão de Tarefas](#sistema-flexível-de-gestão-de-tarefas)
  - [Benefícios Principais](#benefícios-principais)
  - [Exportação para Formato Visual](#exportação-para-formato-visual)
  - [Edição Manual Visual](#edição-manual-visual)
  - [Importação e Sincronização](#importação-e-sincronização)
  - [Caso de Uso: Planejamento Colaborativo](#caso-de-uso-planejamento-colaborativo)
- [Automação Inteligente](#automação-inteligente)
  - [Regras e Ações](#regras-e-ações)
  - [Eventos e Triggers](#eventos-e-triggers)
  - [Exemplos de Automação](#exemplos-de-automação)
- [Análise de Código](#análise-de-código)
  - [Análise de Complexidade](#análise-de-complexidade)
  - [Detecção de Padrões](#detecção-de-padrões)
  - [Sugestões de Refatoração](#sugestões-de-refatoração)
- [Métricas e Produtividade](#métricas-e-produtividade)
  - [Dashboard](#dashboard)
  - [Relatórios de Produtividade](#relatórios-de-produtividade)
  - [Insights Automáticos](#insights-automáticos)
- [Contexto e Estado](#contexto-e-estado)
- [Monitoramento e Otimização](#monitoramento-e-otimização)
  - [Modo Econômico](#modo-econômico)
  - [Otimização Automática](#otimização-automática)
- [Backup e Restauração](#backup-e-restauração)
  - [Backup Manual da Base de Dados](#backup-manual-da-base-de-dados)
  - [Restauração da Base de Dados](#restauração-da-base-de-dados)
  - [Backup Automático](#backup-automático)
  - [Backup Incremental](#backup-incremental)
  - [Sincronização Remota](#sincronização-remota)
  - [Resolução de Problemas de Corrupção](#resolução-de-problemas-de-corrupção)
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
- Veja seu dashboard para uma visão geral rápida: `/cortex:dashboard`

### 2. Durante o Desenvolvimento

- Trabalhe normalmente com o Cursor AI
- Use `/cortex:task` para criar novas tarefas conforme necessário
- Atualize o status com `/cortex:task-status`
- Use `/cortex:export-tasks` para visualizar suas tarefas quando precisar de uma visão geral
- Peça sugestões de próximas tarefas com `/cortex:suggest`

### 3. Planejamento e Revisão

- Exporte tarefas para um formato visual com `/cortex:export-tasks`
- Edite o arquivo gerado em seu editor preferido
- Importe as alterações de volta com `/cortex:import-tasks`
- Ou use `/cortex:sync-tasks` para sincronização automática
- Analise código com `/cortex:analyze` para obter insights sobre melhorias

### 4. Final do Dia

- Use `/cortex:summarize` para obter um resumo do progresso
- Use `/cortex:scan-markers` para identificar TODOs e FIXMEs
- Verifique métricas de produtividade com `/cortex:metrics`
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

## Sistema Flexível de Gestão de Tarefas

O CORTEX oferece um sistema flexível que permite gerir suas tarefas de múltiplas formas, adaptando-se ao seu fluxo de trabalho.

### Benefícios Principais

- **Edição onde preferir:** Use comandos rápidos ou edição visual, conforme sua preferência
- **Colaboração simplificada:** Compartilhe facilmente o plano com a equipe
- **Visualização hierárquica:** Veja claramente a estrutura do projeto
- **Personalização:** Adicione informações extras como estimativas, responsáveis e descrições

### Exportação para Formato Visual

Exporte suas tarefas para um formato visual e editável:

```
/cortex:export-tasks "caminho/para/tarefas.md"
```

Com filtros:
```
/cortex:export-tasks "tarefas.md" --status in_progress,not_started --level phase,stage
```

### Edição Manual Visual

O formato gerado segue uma estrutura hierárquica que você pode editar em qualquer editor:

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

Para importar alterações visuais de volta ao sistema:

```
/cortex:import-tasks "caminho/para/tarefas.md"
```

Para sincronização bidirecional automática:

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

## Automação Inteligente

O CORTEX oferece um poderoso sistema de automação que permite configurar regras baseadas em eventos e condições, reduzindo trabalho manual repetitivo.

### Regras e Ações

Para criar uma nova regra de automação:
```
/cortex:automate create "nome-da-regra" --event "evento" --condition "condição" --action "ação"
```

Para listar regras existentes:
```
/cortex:automate list
```

Para ativar/desativar uma regra:
```
/cortex:automate toggle <rule_id>
```

### Eventos e Triggers

O CORTEX pode reagir a diversos eventos:

- `task_created`: Quando uma nova tarefa é criada
- `task_updated`: Quando uma tarefa é atualizada
- `marker_detected`: Quando um marcador (TODO, FIXME) é detectado
- `session_started`: Quando uma sessão é iniciada
- `system_idle`: Quando o sistema está ocioso
- `scheduled_time`: Em momentos específicos (formato cron)

### Exemplos de Automação

**Exemplo 1: Criar tarefas a partir de TODOs**
```
/cortex:automate create "todo-tarefas" --event "marker_detected" --condition "marker.type == 'TODO'" --action "create_task" --params "title=TODO: {marker.content},level=activity"
```

**Exemplo 2: Notificar sobre tarefas bloqueadas**
```
/cortex:automate create "blocked-notification" --event "task_updated" --condition "task.status == 'blocked'" --action "notify" --params "message=Tarefa {task.title} está bloqueada"
```

**Exemplo 3: Otimização automática de banco de dados**
```
/cortex:automate create "db-optimize" --event "system_idle" --condition "system.cpu_usage < 10" --action "optimize_database"
```

## Análise de Código

O CORTEX oferece ferramentas avançadas para análise de código e identificação de melhorias.

### Análise de Complexidade

Para analisar a complexidade do código:
```
/cortex:analyze complexity "caminho/para/diretório" [--file-type py,js]
```

Para ver arquivos mais complexos:
```
/cortex:analyze list-complexity --min-score 70
```

### Detecção de Padrões

Para detectar padrões e anti-padrões:
```
/cortex:analyze patterns "caminho/para/diretório" [--pattern-type "anti-pattern"]
```

Para encontrar código duplicado:
```
/cortex:analyze duplication "caminho/para/diretório" [--min-lines 5]
```

### Sugestões de Refatoração

Para obter sugestões baseadas em análise de código:
```
/cortex:suggest refactoring [--path "caminho/para/arquivo"]
```

Para priorizar sugestões por impacto:
```
/cortex:suggest list --sort-by impact
```

Para aplicar uma sugestão:
```
/cortex:suggest apply <suggestion_id>
```

## Métricas e Produtividade

O CORTEX rastreia e analisa métricas de produtividade para fornecer insights sobre seu fluxo de trabalho.

### Dashboard

Para visualizar o dashboard principal:
```
/cortex:dashboard
```

Para um dashboard específico de um projeto:
```
/cortex:dashboard --project <project_id>
```

### Relatórios de Produtividade

Para gerar relatório de tarefas completas:
```
/cortex:metrics completion-rate [--timeframe "7days"]
```

Para analisar tempo gasto por tarefa:
```
/cortex:metrics task-time
```

Para identificar períodos mais produtivos:
```
/cortex:metrics productive-hours
```

### Insights Automáticos

O CORTEX gera insights baseados nos seus padrões de trabalho:
```
/cortex:insights [--type productivity,workflow]
```

Para receber sugestões de melhoria no fluxo de trabalho:
```
/cortex:insights workflow-suggestions
```

## Marcadores e Análise de Código

O CORTEX ajuda a rastrear pontos de continuidade no seu código e analisar a qualidade geral.

### Escaneando Marcadores

Para escanear marcadores no código:
```
/cortex:scan-markers [--path "caminho/para/diretório"]
```

Para gerar relatório de TODOs:
```
/cortex:todo-report
```

Para associar um marcador a uma tarefa:
```
/cortex:link-marker <marker_id> <task_id>
```

### Análise Avançada

Para analisar a qualidade geral do código:
```
/cortex:analyze quality "caminho/para/diretório"
```

Para encontrar métodos muito longos:
```
/cortex:analyze long-methods [--max-lines 30]
```

## Monitoramento e Otimização

O CORTEX monitora o sistema e otimiza seu próprio funcionamento para garantir performance ideal.

### Modo Econômico

Para ativar/desativar o modo econômico:
```
/cortex:system eco-mode [on|off|auto]
```

Para verificar o status do sistema:
```
/cortex:system status
```

### Otimização Automática

Para otimizar o banco de dados manualmente:
```
/cortex:system optimize-db
```

Para limpar dados temporários:
```
/cortex:system cleanup
```

Para ver o histórico de uso de recursos:
```
/cortex:system resources [--days 7]
```

## Backup e Restauração

O CORTEX armazena todos os seus dados em um banco SQLite local. É recomendável fazer backups periódicos para evitar perda de dados.

### Backup Manual da Base de Dados

Para criar uma cópia de segurança do banco de dados:

```bash
# Localização padrão do banco de dados
# Por padrão em ~/.cortex/cortex.db
python -m cortex.cli backup --output ~/backups/cortex_backup_$(date +%Y%m%d).db
```

Ou manualmente usando ferramentas SQLite:

```bash
# Certifique-se que o servidor CORTEX não está em execução
sqlite3 ~/.cortex/cortex.db ".backup '~/backups/cortex_backup.db'"
```

### Restauração da Base de Dados

Para restaurar a partir de um backup:

```bash
# Certifique-se que o servidor CORTEX não está em execução
python -m cortex.cli restore --input ~/backups/cortex_backup.db
```

Ou manualmente:

```bash
# Pare o servidor CORTEX
mv ~/.cortex/cortex.db ~/.cortex/cortex.db.old
cp ~/backups/cortex_backup.db ~/.cortex/cortex.db
```

### Backup Automático

O CORTEX pode ser configurado para criar backups automáticos:

```bash
# Configurar backup diário
python -m cortex.cli config set backups.enabled true
python -m cortex.cli config set backups.interval daily
python -m cortex.cli config set backups.retention 7
```

Os backups automáticos são armazenados em `~/.cortex/backups/` por padrão.

### Backup Incremental

O CORTEX suporta backup incremental para economia de espaço:

```bash
# Configurar backup incremental
python -m cortex.cli config set backups.type incremental
```

O backup incremental rastreia alterações desde o último backup completo e armazena apenas as diferenças, economizando espaço e tempo.

### Sincronização Remota

Para configurar sincronização com servidor remoto via SSH:

```bash
# Configurar servidor remoto
python -m cortex.cli remote setup --host usuario@servidor --path /path/to/backup
python -m cortex.cli remote test-connection

# Ativar sincronização automática
python -m cortex.cli config set sync.remote.enabled true
python -m cortex.cli config set sync.remote.interval daily
```

Para sincronizar manualmente:
```bash
python -m cortex.cli remote sync
```

### Resolução de Problemas de Corrupção

Se você encontrar erros de corrupção de banco de dados:

1. Pare o servidor CORTEX:
   ```bash
   python -m cortex.cli stop
   ```

2. Tente reparar o banco de dados:
   ```bash
   sqlite3 ~/.cortex/cortex.db "PRAGMA integrity_check;"
   ```

3. Se a verificação falhar, restaure a partir do backup mais recente:
   ```bash
   python -m cortex.cli restore --auto-latest
   ```

4. Em caso de problemas persistentes, exporte as tarefas para Markdown antes de tentar qualquer reparo:
   ```bash
   python -m cortex.cli export-all-tasks ~/cortex_tasks_backup/
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

### Configurações de Automação

Para ajustar a frequência de análise de código:
```bash
python -m cortex.cli config set analysis.frequency hourly
```

Para configurar o cache adaptativo:
```bash
python -m cortex.cli config set cache.max_size 100MB
python -m cortex.cli config set cache.strategy adaptive
```

Para ajustar limites de uso de recursos:
```bash
python -m cortex.cli config set system.max_cpu_percent 30
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

### Erro de Importação 

Se a importação falhar:

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

### Problemas com Análise de Código

Se a análise de código falhar:

1. Verifique permissões de acesso aos arquivos
2. Verifique configurações de excludes: `/cortex:config get analysis.excludes`
3. Tente analisar um arquivo específico: `/cortex:analyze "caminho/para/arquivo.py"`
4. Verifique recursos do sistema: `/cortex:system status`

### Problemas de Performance

Se o sistema estiver lento:

1. Verifique métricas do sistema: `/cortex:system resources`
2. Otimize o banco de dados: `/cortex:system optimize-db`
3. Ajuste configurações de cache: `/cortex:config set cache.strategy lru`
4. Desative temporariamente automações pesadas: `/cortex:automate pause-all`

## Exemplos Práticos

### Exemplo 1: Iniciar um Novo Projeto

```
/cortex:start "Projeto XYZ" "Implementar sistema de autenticação"
/cortex:task "Implementação de Autenticação" --level phase
/cortex:task "Configurar Backend" --level stage --parent 1
/cortex:task "Implementar rotas de API" --level task --parent 2
/cortex:export-tasks "projeto-xyz.md"
```

### Exemplo 2: Fluxo com Edição Visual

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

Para projetos com edição frequente do formato visual:

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

### Exemplo 4: Automação de Tarefas Repetitivas

```
# 1. Criar regra para transformar TODOs em tarefas
/cortex:automate create "todo-tarefas" --event "marker_detected" --condition "marker.type == 'TODO'" --action "create_task" --params "title=TODO: {marker.content},level=activity"

# 2. Ativar escaneamento periódico
/cortex:automate create "scan-periodico" --event "scheduled_time" --condition "true" --action "scan_markers" --params "schedule=0 * * * *"

# 3. Verificar tarefas criadas automaticamente
/cortex:list-tasks --filter "title:TODO:"
```

### Exemplo 5: Análise e Melhoria de Código

```
# 1. Analisar complexidade do código
/cortex:analyze complexity "./src"

# 2. Verificar arquivos mais complexos
/cortex:analyze list-complexity --min-score 70

# 3. Obter sugestões de refatoração
/cortex:suggest refactoring --path "./src/arquivo_complexo.py"

# 4. Aplicar uma sugestão específica
/cortex:suggest apply 123
```

### Exemplo 6: Otimização em Momentos Ociosos

```bash
# Configurar otimização automática durante tempo ocioso
/cortex:automate create "optimize-idle" --event "system_idle" --condition "system.cpu_usage < 15 && system.is_on_power" --action "optimize_database"

# Configurar limpeza de cache antiga
/cortex:automate create "clean-cache" --event "system_idle" --condition "cache.size > 50MB" --action "clean_cache" --params "older_than=7days"
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

### Sistema Flexível de Gestão de Tarefas
```
/cortex:export-tasks "caminho/para/arquivo.md" [filtros]
/cortex:import-tasks "caminho/para/arquivo.md"
/cortex:sync-tasks "caminho/para/arquivo.md"
/cortex:diff-tasks "caminho/para/arquivo.md"
```

### Automação Inteligente
```
/cortex:automate create "nome-da-regra" --event "evento" --condition "condição" --action "ação"
/cortex:automate list [--status active]
/cortex:automate toggle <rule_id>
/cortex:automate delete <rule_id>
```

### Análise de Código
```
/cortex:analyze [complexity|patterns|duplication] "caminho"
/cortex:suggest [refactoring|tasks]
/cortex:suggest apply <suggestion_id>
```

### Métricas e Dashboard
```
/cortex:dashboard [--project <project_id>]
/cortex:metrics [completion-rate|task-time|productive-hours]
/cortex:insights [--type <tipo>]
```

### Marcadores
```
/cortex:scan-markers [--path "caminho"]
/cortex:link-marker <marker_id> <task_id>
/cortex:todo-report
```

### Sistema e Otimização
```
/cortex:system [status|optimize-db|cleanup|eco-mode]
/cortex:system resources [--days <dias>]
```

### Contexto e Estado
```
/cortex:context [filtro]
/cortex:save-state "nome_do_snapshot"
/cortex:load-state "nome_do_snapshot"
```

### Backup e Sincronização
```
/cortex:backup [--incremental]
/cortex:remote [setup|sync|test-connection]
```

### Ajuda
```
/cortex:help [comando]
``` 