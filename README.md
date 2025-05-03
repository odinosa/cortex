# CORTEX

> Memória de contexto para o Cursor via Model Context Protocol.

![Status: Early Development](https://img.shields.io/badge/status-early_development-orange)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)

## Visão Geral

O CORTEX funciona como o "cérebro" do teu ambiente de desenvolvimento Cursor, permitindo:

- Guardar e restaurar sessões de desenvolvimento
- Manter contexto estruturado de conversas com modelos LLM
- Rastrear automaticamente tarefas, TODOs e FIXMEs do código
- Resumir progressos e fornecer contexto relevante a cada nova interação

Tudo através do [Model Context Protocol (MCP)](https://cursor.sh/docs/mcp) - implementando ferramentas nativas que qualquer LLM pode utilizar para guardar e recuperar estado.

## Quickstart

```bash
# 1. Clone o repositório
git clone https://github.com/odinosa/cortex.git
cd cortex

# 2. Inicia o PostgreSQL local (requer Docker)
docker-compose up -d db

# 3. Configura o ambiente Python
python -m venv .venv
source .venv/bin/activate
pip install -e .

# 4. Executa as migrações
python -m cortex.cli migrate

# 5. Inicia o servidor MCP (modo daemon)
python -m cortex.cli serve
```

## Integração com Cursor

1. Cria/edita `~/.cursor/mcp.json` com:
```json
{
  "tools": [
    {
      "id": "cortex",
      "stdio": {
        "command": ["python", "-m", "cortex.mcp.server"]
      },
      "tools": ["start_session", "end_session", "record_message", "get_context", "scan_markers"]
    }
  ]
}
```

2. Reinicia o Cursor

3. Verifica que o CORTEX está ativo abrindo o console do Cursor (`Cmd+Shift+P > Toggle Developer Console`) e procurando por `[MCP] Registered cortex tools`.

## Ferramentas MCP Disponíveis

- `start_session`: Inicia uma nova sessão de trabalho com objetivo e contexto
- `end_session`: Finaliza uma sessão atual 
- `record_message`: Regista mensagem (pergunta ou resposta) na sessão
- `get_context`: Recupera contexto relevante para o modelo
- `scan_markers`: Analisa código em busca de TODOs, FIXMEs e cria relatório

## Contribuições

Contribuições são bem-vindas! Vê o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Licença

MIT

---

*Última atualização: 03-05-2025 23:22*
