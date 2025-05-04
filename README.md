# CORTEX

> Assistente de Contexto para Cursor via Model Context Protocol (MCP)

![Status: Em Desenvolvimento](https://img.shields.io/badge/status-em_desenvolvimento-orange)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![SQLite: 3.x](https://img.shields.io/badge/sqlite-3.x-blue)

## Visão Geral

O CORTEX é um assistente de contexto para o ambiente de desenvolvimento Cursor, que permite:

- **Manter contexto estruturado** entre sessões de desenvolvimento
- **Gerir hierarquias de tarefas** em 4 níveis (Fase → Etapa → Tarefa → Atividade)
- **Guardar e restaurar sessões** de desenvolvimento com facilidade
- **Sincronizar tarefas entre SQLite e Markdown** para edição flexível
- **Extrair marcadores (TODOs, FIXMEs)** do código e vinculá-los a tarefas
- **Aplicar regras e templates** conforme o contexto do projeto

O CORTEX implementa o [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) para fornecer ferramentas que qualquer LLM no Cursor pode utilizar para manter e recuperar estado.

## Documentação

- [Guia de Utilização](USAGE_GUIDE.md) - Instruções completas de instalação e uso
- [Arquitetura](ARCHITECTURE.md) - Detalhes técnicos da implementação
- [Modelo de Dados](DATA_MODEL.md) - Esquema de banco de dados e relações

## Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/odinosa/cortex.git
cd cortex

# Configura o ambiente Python
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Inicializa o banco de dados e inicia o servidor
python -m cortex.cli init
python -m cortex.cli serve &

# Configura o Cursor
python -m cortex.cli setup-cursor
```

Consulte o [Guia de Utilização](USAGE_GUIDE.md) para instruções mais detalhadas.

## Principais Benefícios

- **Continuidade:** Nunca perca o fio condutor do seu desenvolvimento
- **Estrutura:** Organização clara do trabalho e progresso
- **Flexibilidade:** Edite tarefas tanto via comandos quanto via Markdown
- **Rastreabilidade:** Histórico completo de decisões e alterações
- **Adaptabilidade:** Sistema contextual ajusta regras automaticamente
- **Simplicidade:** Comandos diretamente no chat do Cursor

## Abordagem Híbrida SQLite + Markdown

Uma das principais inovações do CORTEX é a combinação do melhor de dois mundos:

- **SQLite** para armazenamento estruturado, consultas rápidas e integridade de dados
- **Markdown** para visualização amigável, edição manual e compartilhamento fácil

Esta abordagem permite:
- Edição por diversos meios (comandos, API, arquivos Markdown)
- Compatibilidade com ferramentas de versionamento como Git
- Exportação para compartilhamento simples com outros membros da equipe

## Comandos Principais

```
/cortex:start "Nome da Sessão" "Objetivo principal"
/cortex:task "Nova tarefa" --level task --parent <id>
/cortex:export-tasks "caminho/para/arquivo.md"
/cortex:import-tasks "caminho/para/arquivo.md"
/cortex:scan-markers
/cortex:help
```

Consulte o [Guia de Utilização](USAGE_GUIDE.md) para a lista completa de comandos.

## Perguntas Frequentes

**P: Como funciona a integração com o Cursor?**
R: O CORTEX utiliza o Model Context Protocol (MCP) para fornecer ferramentas que o Cursor pode utilizar. Quando configurado, o Cursor chamará estas ferramentas para guardar e restaurar contexto de desenvolvimento.

**P: Como é garantida a segurança dos dados?**
R: Todos os dados são armazenados localmente em SQLite, e o sistema funciona inteiramente no teu Macbook, sem enviar dados para serviços externos (exceto quando explicitamente configurado para integração com Jira).

**P: Como escolher entre editar no SQLite ou no Markdown?**
R: Use comandos para operações rápidas durante o desenvolvimento e edição de Markdown para planejamento mais detalhado ou quando precisar visualizar a estrutura completa de tarefas.

## Contribuições

Contribuições são bem-vindas! Vê o [CONTRIBUTING.md](docs/CONTRIBUTING.md) para detalhes.

## Licença

MIT

---

*Última atualização: 09-07-2024*
