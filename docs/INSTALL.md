# Guia de Instalação do CORTEX

*Última actualização:* 04-06-2024 18:15

Este guia apresenta os passos necessários para instalar e configurar o CORTEX, o sistema MCP (Model Context Protocol) para o Cursor.

## Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL 14 ou superior (ou Docker para execução em contêiner)
- Git
- Cursor (versão mais recente)

## Instalação Rápida

### 1. Clone o Repositório

```bash
git clone https://github.com/odinosa/cortex.git
cd cortex
```

### 2. Execute o Script de Bootstrap

O script de bootstrap automatiza toda a configuração inicial:

```bash
./scripts/bootstrap.sh
```

Este script irá:
- Verificar os pré-requisitos
- Criar um ambiente virtual Python
- Instalar todas as dependências
- Configurar o PostgreSQL (via Docker se disponível)
- Criar a estrutura inicial de diretórios
- Executar as migrações do banco de dados

## Instalação Manual

Se preferir uma instalação passo a passo:

### 1. Configurar o Ambiente Python

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Linux/macOS:
source .venv/bin/activate
# No Windows:
# .venv\Scripts\activate

# Instalar dependências
pip install -e ".[dev]"
```

### 2. Configurar o PostgreSQL

Opção 1: Usar Docker (recomendado para desenvolvimento)
```bash
# Iniciar PostgreSQL
docker-compose up -d db
```

Opção 2: Usar PostgreSQL local existente
```bash
# Criar banco de dados
createdb cortex_db -U seu_usuario

# Configurar variável de ambiente
export DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost:5432/cortex_db"
```

### 3. Executar Migrações

```bash
python -m cortex.cli migrate
```

## Integração com o Cursor

1. Crie ou edite o ficheiro `~/.cursor/mcp.json` com o seguinte conteúdo:

```json
{
  "tools": [
    {
      "id": "cortex",
      "stdio": {
        "command": ["python", "-m", "cortex.mcp.server"]
      },
      "tools": ["start_session", "end_session", "record_message", "get_context", "scan_markers", "create_task", "update_task_status", "list_tasks", "detect_context", "save_state", "load_state"]
    }
  ]
}
```

2. Certifique-se de que o caminho para o Python está correto e aponta para o ambiente virtual onde o CORTEX está instalado:

```json
"command": ["/caminho/completo/para/.venv/bin/python", "-m", "cortex.mcp.server"]
```

3. Reinicie o Cursor para carregar a nova configuração MCP.

4. Verifique que o CORTEX está ativo abrindo o console do Cursor (`Cmd+Shift+P > Toggle Developer Console`) e procurando por `[MCP] Registered cortex tools`.

## Iniciar o Servidor

```bash
# Inicie o servidor MCP (modo daemon)
python -m cortex.cli serve --daemon

# Para ver logs e execução em primeiro plano
python -m cortex.cli serve

# Para modo de desenvolvimento
python -m cortex.cli serve --dev
```

## Verificação da Instalação

Para verificar se tudo está funcionando corretamente:

1. Abra o Cursor e inicie um chat com o AI.
2. Digite o comando `/cortex:start "Minha Primeira Sessão" "Testar instalação do CORTEX"`
3. Verifique se a sessão foi criada com sucesso.

## Configuração Avançada

### Variáveis de Ambiente

- `DATABASE_URL`: URL de conexão com o PostgreSQL
- `DATABASE_POOL_SIZE`: Tamanho do pool de conexões (padrão: 10)
- `DATABASE_MAX_OVERFLOW`: Limite de overflow do pool (padrão: 20)
- `DATABASE_POOL_TIMEOUT`: Timeout do pool em segundos (padrão: 30)
- `DATABASE_ECHO`: Ativar logs SQL (true/false, padrão: false)
- `LOG_LEVEL`: Nível de logging (INFO, DEBUG, WARNING, ERROR)
- `CORTEX_ENV`: Ambiente (development, production)

### Configuração de Redis (Opcional)

Para habilitar cache com Redis:

```bash
# No arquivo .env ou exportar manualmente
export REDIS_URL="redis://localhost:6379/0"
```

### Métricas com Prometheus (Opcional)

Para habilitar métricas:

```bash
# Iniciar com todos os serviços (incluindo Prometheus e Grafana)
docker-compose --profile full up -d
```

Acesse o dashboard do Grafana em http://localhost:3000 (admin/cortex).

## Solução de Problemas

### Erro de Conexão com o PostgreSQL

Verifique:
- Se o PostgreSQL está em execução: `docker ps` ou `pg_isready`
- Se a URL de conexão está correta
- Se o Docker está em execução (se estiver usando o contêiner)

### Ferramentas MCP não Aparecem no Cursor

Verifique:
- Se o arquivo `~/.cursor/mcp.json` está correto
- Se o servidor CORTEX está em execução: `ps aux | grep cortex`
- Se há erros no console do Cursor (Cmd+Shift+P > Toggle Developer Console)
- Se o caminho do Python no `mcp.json` está correto

### Problemas com as Migrações

Tente:
```bash
# Resetar o banco de dados
docker-compose down -v
docker-compose up -d db

# Recriar as migrações
alembic revision --autogenerate -m "reset"
alembic upgrade head
```

## Recursos Adicionais

- [Documentação do Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
- [Estrutura do Projeto CORTEX](../README.md)
- [Estratégia do Projeto](../STRATEGY.md)
- [Roadmap](../ROADMAP.md) 