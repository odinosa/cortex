# Guia de Início Rápido do CORTEX

*Última atualização:* 07-07-2024

Este guia mostra como instalar, configurar e começar a usar o CORTEX com o Cursor.

## Instalação

### Requisitos
- Python 3.10 ou superior
- Cursor instalado
- MacOS (testado em Apple Silicon M3)

### Passos

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/odinosa/cortex.git
   cd cortex
   ```

2. **Criar ambiente virtual e instalar**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. **Inicializar banco de dados**
   ```bash
   python -m cortex.cli init
   ```

4. **Configurar integração com o Cursor**
   ```bash
   python -m cortex.cli setup-cursor
   ```
   
5. **Reiniciar o Cursor**
   Feche e abra novamente o Cursor para carregar a configuração MCP.

## Uso Básico

### Iniciar o Servidor MCP

Para usar o CORTEX, o servidor MCP precisa estar em execução:

```bash
# Iniciar em primeiro plano
python -m cortex.cli serve

# Iniciar em background
python -m cortex.cli serve &
```

### Criar um Projeto

Antes de usar as funcionalidades principais, crie um projeto:

```bash
python -m cortex.cli create-project "Meu Projeto" --desc "Descrição do projeto"
```

### Verificar Status

Para verificar o status atual do sistema:

```bash
python -m cortex.cli status
```

## Comandos no Cursor

Depois de configurado, você pode usar os seguintes comandos diretamente no chat do Cursor:

### Sessões

- **Iniciar sessão**
  ```
  /cortex:start "Título da Sessão" "Objetivo principal"
  ```

- **Finalizar sessão**
  ```
  /cortex:end "Resumo do que foi feito"
  ```

- **Retomar sessão anterior**
  ```
  /cortex:resume last
  ```

### Tarefas

- **Criar tarefa**
  ```
  /cortex:task "Implementar funcionalidade X"
  ```

- **Atualizar status de tarefa**
  ```
  /cortex:task-status 3 completed
  ```

- **Listar tarefas**
  ```
  /cortex:list-tasks
  ```

### Marcadores

- **Escanear marcadores**
  ```
  /cortex:scan-markers
  ```

### Contexto

- **Ver contexto atual**
  ```
  /cortex:context
  ```

## Exemplo de Fluxo de Trabalho

Um fluxo de trabalho típico usando o CORTEX:

1. **Iniciar o dia:**
   ```
   /cortex:start "Implementação de API" "Criar endpoints CRUD"
   ```

2. **Criar tarefas para a sessão:**
   ```
   /cortex:task "Definir modelos de dados"
   /cortex:task "Implementar endpoint GET"
   /cortex:task "Implementar endpoint POST"
   ```

3. **Durante o desenvolvimento:**
   - Trabalhe normalmente com o Cursor AI
   - Use `// TODO: ` nos comentários para marcar pontos de continuidade

4. **Verificar progresso:**
   ```
   /cortex:scan-markers
   /cortex:list-tasks
   ```

5. **Finalizar tarefas concluídas:**
   ```
   /cortex:task-status 1 completed
   ```

6. **Finalizar a sessão:**
   ```
   /cortex:end "Implementei endpoints GET e POST. Pendente: PUT e DELETE"
   ```

## Dicas e Truques

- **Usar com o Cursor LLM**: O CORTEX funciona melhor com modelos como o Claude 3 Opus ou GPT-4o, que têm melhor compreensão de contexto.

- **Marcadores de Continuidade**: Use comentários formatados como `// TODO: fazer algo` ou `// FIXME: corrigir isso` para que o CORTEX possa escaneá-los automaticamente.

- **Tarefas Hierárquicas**: Ao criar tarefas complexas, use a hierarquia de 4 níveis:
  ```
  /cortex:task "Implementar API" --level phase
  /cortex:task "Modelagem de Dados" --level stage --parent 1
  /cortex:task "Criar modelo de usuário" --level task --parent 2
  /cortex:task "Adicionar validação de senha" --level activity --parent 3
  ```

## Troubleshooting

### Problemas Comuns

- **Ferramentas não aparecem no Cursor**
  
  Verifique se o servidor está rodando:
  ```bash
  python -m cortex.cli status
  ```

  Se necessário, reinicie o Cursor ou force reconfiguração:
  ```bash
  python -m cortex.cli setup-cursor --force
  ```

- **Erro ao iniciar sessão**
  
  Verifique se você criou um projeto:
  ```bash
  python -m cortex.cli list-projects
  ```

## Próximos Passos

- Explore mais comandos com `python -m cortex.cli --help`
- Consulte a documentação completa em `README.md`
- Leia sobre o modelo de dados em `DATA_MODEL.md` 
- Configure regras contextuais avançadas 