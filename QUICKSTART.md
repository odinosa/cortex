# Guia de Início Rápido do CORTEX

*Última atualização:* 09-07-2024

Este guia fornece instruções para instalar, configurar e começar a usar o CORTEX.

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

## Comandos Básicos

### Gestão de Sessões

Para iniciar uma nova sessão:
```
/cortex:start "Título da Sessão" "Objetivo principal"
```

Para listar sessões existentes:
```
/cortex:list-sessions
```

Para retomar uma sessão:
```
/cortex:resume <session_id>
```

### Gestão de Tarefas

Para criar uma nova tarefa:
```
/cortex:task "Implementar feature X" --level task --parent 3
```

Para listar tarefas:
```
/cortex:list-tasks [--status in_progress] [--level task]
```

Para atualizar status:
```
/cortex:task-status 5 in_progress --progress 75
```

## Gestão Híbrida SQLite + Markdown

O CORTEX oferece uma abordagem híbrida para gerenciar tarefas, permitindo que você alterne facilmente entre o banco de dados SQLite e arquivos Markdown.

### Exportação para Markdown

Para exportar suas tarefas para um arquivo Markdown:

```
/cortex:export-tasks "caminho/para/tarefas.md" 
```

Você pode filtrar as tarefas a serem exportadas:

```
/cortex:export-tasks "caminho/para/tarefas.md" --status in_progress,not_started --level phase,stage
```

### Edição Manual em Markdown

Após exportar, você pode editar o arquivo Markdown manualmente em qualquer editor:

1. Altere títulos, descrições, status ou progresso
2. Adicione novas tarefas (seguindo o formato existente)
3. Reorganize a hierarquia (mudando os níveis de cabeçalho)
4. Salve o arquivo

### Importação de Markdown para SQLite

Para importar as alterações feitas no arquivo Markdown:

```
/cortex:import-tasks "caminho/para/tarefas.md"
```

### Sincronização Bidirecional

Para sincronizar automaticamente (comparando SQLite e Markdown):

```
/cortex:sync-tasks "caminho/para/tarefas.md"
```

Se houver conflitos, o CORTEX fornecerá opções para resolvê-los.

### Visualização de Diferenças

Para ver as diferenças entre as tarefas no SQLite e no arquivo Markdown:

```
/cortex:diff-tasks "caminho/para/tarefas.md"
```

### Fluxo de Trabalho Recomendado

1. **Desenvolvimento Diário**:
   - Use comandos `/cortex:task` e `/cortex:task-status` para atualizações rápidas
   - Exporte para Markdown no final do dia: `/cortex:export-tasks "tarefas.md"`

2. **Planejamento e Revisão**:
   - Edite o arquivo Markdown para reorganizar e planejar
   - Importe de volta para SQLite: `/cortex:import-tasks "tarefas.md"`

3. **Colaboração**:
   - Compartilhe arquivo Markdown com colegas
   - Versione com Git para rastreamento de alterações
   - Sincronize atualizações: `/cortex:sync-tasks "tarefas.md"`

## Análise de Código

Para escanear marcadores no código:
```
/cortex:scan-markers
```

Para gerar relatório de TODOs:
```
/cortex:todo-report
```

## Contexto e Estado

Para obter o contexto atual:
```
/cortex:context
```

Para salvar um snapshot do estado:
```
/cortex:save-state "nome-do-snapshot"
```

Para carregar um snapshot:
```
/cortex:load-state "nome-do-snapshot"
```

## Configuração Personalizada

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

## Exemplos de Uso

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

## Próximos Passos

1. Explore a documentação completa para recursos avançados
2. Configure regras contextuais para seu fluxo de trabalho
3. Explore a integração de marcadores com tarefas
4. Considere contribuir com o desenvolvimento

Para mais informações, consulte a [documentação completa](README.md). 