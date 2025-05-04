# CORTEX

> Assistente Inteligente de Contexto para Cursor via Model Context Protocol (MCP)

![Status: Em Desenvolvimento](https://img.shields.io/badge/status-em_desenvolvimento-orange)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![SQLite: 3.x](https://img.shields.io/badge/sqlite-3.x-blue)
![CI](https://img.shields.io/github/actions/workflow/status/odinosa/cortex/ci.yml?branch=main&label=CI)
![Test Coverage](https://img.shields.io/codecov/c/github/odinosa/cortex?token=XXXXXXXX)
![Licença: MIT](https://img.shields.io/badge/license-MIT-green)

## Visão Geral

O CORTEX é um assistente inteligente de contexto para o ambiente de desenvolvimento Cursor, que permite:

- **Manter contexto estruturado** entre sessões de desenvolvimento
- **Gerir hierarquias de tarefas** em 4 níveis (Fase → Etapa → Tarefa → Atividade)
- **Automatizar fluxos de trabalho** com base em eventos e condições
- **Analisar código e oferecer sugestões** para refatoração e melhorias
- **Monitorar produtividade** e fornecer insights sobre padrões de trabalho
- **Guardar e restaurar sessões** de desenvolvimento com facilidade
- **Editar tarefas de forma flexível** através de comandos ou visualmente
- **Extrair marcadores (TODOs, FIXMEs)** do código e vinculá-los a tarefas
- **Aplicar regras e templates** conforme o contexto do projeto
- **Otimizar performance** com cache adaptativo e monitoramento de recursos

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
- **Automação:** Redução de tarefas repetitivas com automação inteligente
- **Flexibilidade:** Escolha como gerir tarefas - comandos rápidos ou edição visual
- **Rastreabilidade:** Histórico completo de decisões e alterações
- **Adaptabilidade:** Sistema contextual ajusta regras automaticamente
- **Simplicidade:** Comandos diretamente no chat do Cursor
- **Eficiência:** Otimização automática para máxima performance
- **Insights:** Análises e métricas sobre seu código e produtividade

## Sistema Inteligente e Adaptativo

O CORTEX vai além da gestão de tarefas tradicional ao oferecer:

### Automação Inteligente

- **Regras Automáticas:** Configure ações automáticas baseadas em eventos e condições
- **Detecção de Padrões:** Identifica TODOs, FIXMEs e padrões de código automaticamente
- **Integrações:** Sincronização com sistemas externos via SSH

### Análise e Sugestões

- **Análise de Código:** Detecta complexidade, duplicações e anti-padrões
- **Sugestões Proativas:** Recomendações para refatoração e melhorias
- **Priorização Inteligente:** Tarefas sugeridas com base em impacto e esforço

### Monitoramento e Otimização

- **Dashboard em Terminal:** Visualização rápida do progresso e métricas
- **Métricas de Produtividade:** Análise de tempo, eficiência e padrões de trabalho
- **Modo Econômico:** Reduz operações em background quando em bateria

## Sistema Flexível de Gestão de Tarefas

Uma das principais inovações do CORTEX é o seu sistema de gestão de tarefas que oferece:

- **Múltiplas formas de interação:** Utilize comandos rápidos durante o desenvolvimento ou edição visual para planejamento
- **Colaboração sem complicações:** Compartilhe facilmente o plano de tarefas com outros membros da equipe
- **Versionamento simplificado:** Compatibilidade com Git e outras ferramentas de controle de versão
- **Visualização hierárquica:** Veja claramente a estrutura e relações entre as tarefas

Tecnicamente, isto é implementado através de uma combinação de armazenamento estruturado (SQLite) e formato visual editável (Markdown), mas o que importa é a flexibilidade que isto proporciona no seu fluxo de trabalho.

## Comandos Principais

```
/cortex:start "Nome da Sessão" "Objetivo principal"
/cortex:task "Nova tarefa" --level task --parent <id>
/cortex:export-tasks "caminho/para/arquivo.md"
/cortex:import-tasks "caminho/para/arquivo.md"
/cortex:scan-markers
/cortex:analyze "caminho/para/diretório"
/cortex:suggest
/cortex:dashboard
/cortex:automate "nome-da-regra"
/cortex:help
```

Consulte o [Guia de Utilização](USAGE_GUIDE.md) para a lista completa de comandos.

## Perguntas Frequentes

**P: Como funciona a integração com o Cursor?**
R: O CORTEX utiliza o Model Context Protocol (MCP) para fornecer ferramentas que o Cursor pode utilizar. Quando configurado, o Cursor chamará estas ferramentas para guardar e restaurar contexto de desenvolvimento.

**P: Como é garantida a segurança dos dados?**
R: Todos os dados são armazenados localmente em SQLite, e o sistema funciona inteiramente no teu Macbook, sem enviar dados para serviços externos (exceto quando explicitamente configurado para sincronização SSH).

**P: Como escolher entre as diferentes formas de gerir tarefas?**
R: Use comandos para operações rápidas durante o desenvolvimento e edição visual para planejamento mais detalhado ou quando precisar visualizar a estrutura completa de tarefas.

**P: Como o sistema se adapta aos recursos do meu MacBook?**
R: O CORTEX monitora o uso de CPU, memória e bateria, ajustando automaticamente suas operações em background. Em modo bateria, ele reduz processamento pesado para economizar energia.

**P: Como a automação inteligente pode ajudar-me?**
R: O sistema pode criar tarefas automaticamente a partir de marcadores de código, sugerir refatorações baseadas em análise de código, e otimizar o banco de dados durante períodos de ociosidade, entre muitas outras ações configuráveis.

## Contribuições

Contribuições são bem-vindas! Vê o [CONTRIBUTING.md](docs/CONTRIBUTING.md) para detalhes.

---

*Última atualização: 05-05-2025*
