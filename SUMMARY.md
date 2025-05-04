# Resumo do Projeto CORTEX

*Última atualização:* 09-07-2024

Este documento fornece uma visão resumida do projeto CORTEX, sua arquitetura, funcionalidades e evolução.

## O Que é o CORTEX?

O CORTEX é um assistente de contexto para o ambiente de desenvolvimento Cursor, que implementa o Model Context Protocol (MCP) para fornecer ferramentas de gestão de contexto, sessões e tarefas. O sistema permite manter um histórico estruturado de sessões de desenvolvimento, gerenciar tarefas em níveis hierárquicos e aplicar regras contextuais.

## Principais Funcionalidades

- **Gestão de Sessões**: Capacidade de iniciar, pausar e retomar sessões de desenvolvimento, mantendo contexto completo
- **Gestão Hierárquica de Tarefas**: Organização em 4 níveis (Fase > Etapa > Tarefa > Atividade) com relações e dependências
- **Abordagem Híbrida SQLite + Markdown**: Sistema de sincronização bidirecional para edição flexível de tarefas
- **Detecção de Contexto**: Identificação automática do contexto de trabalho com base no projeto e conteúdo
- **Marcadores de Continuidade**: Extração e rastreamento de TODOs, FIXMEs e outros marcadores do código
- **Regras Contextuais**: Aplicação de comportamentos específicos baseados no contexto detectado
- **Integração com Cursor**: Implementação completa do protocolo MCP para interação fluida
- **Exportação Flexível**: Capacidade de exportar tarefas e contexto para Markdown e formatos estruturados

## Decisões Arquiteturais

1. **SQLite como Armazenamento Principal**: Escolhido por sua simplicidade, robustez e ausência de requisitos de servidor
2. **Abordagem Híbrida com Markdown**: Combina o melhor dos dois mundos - armazenamento estruturado em SQLite e edição amigável em Markdown
3. **Servidor MCP Leve**: Implementação eficiente do protocolo MCP via stdio
4. **CLI Extensível**: Interface de linha de comando para administração simples
5. **Design Modular**: Componentes isolados para facilitar manutenção e extensão

## Abordagem Híbrida SQLite + Markdown

Uma das principais inovações do CORTEX é sua abordagem híbrida para gestão de tarefas, combinando:

- **SQLite para Armazenamento Estruturado**:
  - Consultas rápidas e eficientes
  - Integridade referencial e relacional
  - Suporte a transações ACID

- **Markdown para Interação Humana**:
  - Visualização e edição amigável
  - Facilidade de compartilhamento
  - Integração com ferramentas de versionamento (Git)

- **Sincronização Bidirecional**:
  - Exportação de tarefas para arquivos Markdown
  - Importação de alterações feitas manualmente
  - Detecção e resolução de conflitos

Esta abordagem facilita tanto o gerenciamento programático (via APIs e comandos) quanto a interação humana direta através de edição de arquivos Markdown, proporcionando a flexibilidade ideal para diferentes necessidades.

## Evolução Planejada

O desenvolvimento do CORTEX segue um modelo iterativo, com as seguintes fases:

1. **MVP (1.0)**: Gestão básica de sessões e contexto
2. **Gestão de Tarefas (2.0)**: Sistema hierárquico de tarefas
3. **Abordagem Híbrida SQLite + Markdown (2.5)**: Sincronização bidirecional para edição flexível
4. **Análise de Código (3.0)**: Extração e gestão de marcadores
5. **Motor Contextual (4.0)**: Detecção de contexto e aplicação de regras
6. **Integração Externa (5.0)**: Conectores para sistemas externos (Jira)
7. **Extensões Avançadas (6.0)**: Ferramentas adicionais para análise e visualização

## Comparação com Alternativas

| Característica | CORTEX | SUGSE | Cursor Nativo | Jira |
|----------------|--------|-------|---------------|------|
| Integração com Cursor | ✅ | ⚠️ Parcial | ✅ | ❌ |
| Persistência de Sessões | ✅ | ✅ | ❌ | ❌ |
| Hierarquia de Tarefas | ✅ | ✅ | ❌ | ✅ |
| Sincronização SQLite ↔ Markdown | ✅ | ❌ | ❌ | ❌ |
| Marcadores de Código | ✅ | ✅ | ❌ | ❌ |
| Gestão de Contexto | ✅ | ⚠️ Básica | ❌ | ❌ |
| Uso Exclusivamente Local | ✅ | ✅ | ✅ | ❌ |
| Integração Jira | ⚠️ Planejada | ❌ | ❌ | ✅ |

## Conclusão

O CORTEX representa um avanço significativo na gestão de contexto para desenvolvimento em Cursor, com foco em:

- **Continuidade**: Manutenção do contexto entre sessões de desenvolvimento
- **Flexibilidade**: Abordagem híbrida SQLite + Markdown para gerenciamento de tarefas
- **Estrutura**: Organização hierárquica de tarefas e contextos
- **Automação**: Detecção e aplicação de regras contextuais
- **Simplicidade**: Interface direta via chat do Cursor e comandos MCP

A abordagem híbrida para gestão de tarefas é especialmente valiosa, pois permite aproveitar o melhor de dois mundos: a estrutura e integridade do SQLite com a flexibilidade e legibilidade do Markdown, proporcionando uma experiência de desenvolvimento mais fluida e produtiva.

## Visão Geral

O CORTEX é um sistema de gestão de contexto para o Cursor, implementado utilizando o Model Context Protocol (MCP). Ele resolve o problema de "amnésia" entre sessões de desenvolvimento, permitindo persistir e restaurar contexto, gerir tarefas hierárquicas e aplicar regras contextuais.

## Componentes Principais

1. **Sistema MCP**: Interface com o Cursor via Model Context Protocol
2. **Gestão de Sessões**: Persistência de conversas e contexto entre sessões
3. **Gestão de Tarefas**: Sistema hierárquico de 4 níveis (Fase > Etapa > Tarefa > Atividade)
4. **Marcadores de Continuidade**: Extração e rastreamento de TODOs/FIXMEs no código
5. **Motor Contextual**: Detecção e aplicação de regras conforme contexto

## Destaques da Arquitetura

- **Modularidade**: Componentes bem separados para fácil manutenção
- **Simplicidade**: SQLite local para persistência sem requisitos de servidor
- **Leveza**: Foco em baixa latência e consumo mínimo de recursos
- **Integração MCP**: Comunicação direta com o Cursor via stdio

## Estrutura de Arquivos

```
cortex/
├── cli/             # Interface de linha de comando
├── core/            # Lógica de negócios principal
├── mcp/             # Implementação do Model Context Protocol
│   └── tools/       # Ferramentas MCP
└── storage/         # Persistência de dados
    ├── models/      # Modelos de dados
    └── dao/         # Data Access Objects
```

## Plano de Implementação

O desenvolvimento segue uma abordagem iterativa com foco em entrega de valor:

1. **Fase 1**: Sistema MCP básico com persistência de sessões (2 semanas)
2. **Fase 2**: Gestão de tarefas hierárquicas (2 semanas) 
3. **Fase 3**: Análise de código e marcadores (2 semanas)
4. **Fase 4**: Motor contextual e regras (2 semanas)
5. **Fase 5**: Integrações e polimento (2 semanas)

## Casos de Uso Principais

1. **Continuidade entre Sessões**: Restaurar contexto completo ao retomar um projeto
2. **Estruturação de Trabalho**: Organizar tarefas em hierarquia clara
3. **Rastreamento de Progresso**: Visualizar avanço e pendências
4. **Marcação de Pontos de Continuidade**: Capturar TODOs e FIXMEs no código
5. **Adaptação Contextual**: Aplicar regras específicas conforme o contexto

## Fluxo de Trabalho do Utilizador

1. Iniciar o servidor MCP do CORTEX
2. Trabalhar no Cursor com comandos `/cortex:...`
3. Usar marcadores no código (`TODO`, `FIXME`)
4. Finalizar sessão com resumo do progresso
5. Retomar trabalho posteriormente com contexto completo

## Documentação

- `README.md`: Visão geral e início rápido
- `ARCHITECTURE.md`: Detalhes da arquitetura do sistema
- `DATA_MODEL.md`: Esquema de dados e relações
- `PROJECT_PLAN.md`: Plano de implementação faseado
- `INTEGRATION.md`: Integração com o Cursor
- `QUICKSTART.md`: Guia rápido de uso

## Desenvolvimento

O desenvolvimento do CORTEX segue a filosofia de "dogfooding" - utilizar o próprio sistema durante seu desenvolvimento, permitindo iterações rápidas baseadas na experiência real de uso.

## Ferramentas MCP

O CORTEX fornece as seguintes ferramentas MCP ao Cursor:

- `start_session`: Inicia uma sessão de trabalho
- `end_session`: Finaliza uma sessão 
- `record_message`: Registra mensagens na sessão atual
- `get_context`: Obtém contexto para o modelo
- `create_task`: Cria tarefas hierárquicas
- `update_task_status`: Atualiza o estado de tarefas
- `list_tasks`: Lista tarefas com filtros
- `scan_markers`: Analisa código para marcadores
- `detect_context`: Detecta o contexto atual
- `add_context`: Adiciona contexto personalizado
- `apply_rule`: Aplica regras baseadas em contexto

## Próximos Passos Sugeridos

1. Iniciar com a implementação do servidor MCP básico
2. Testar integração com o Cursor
3. Desenvolver funcionalidades do core em ordem de prioridade
4. Refinar a UX com base no uso real 