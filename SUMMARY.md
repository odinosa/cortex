# Resumo do Projeto CORTEX

*Última atualização:* 07-07-2024

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