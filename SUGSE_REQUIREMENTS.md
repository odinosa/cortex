# Sistema Unificado de Gestão de Sessões e Estado (SUGSE)
## Documento de Requisitos

**Data de criação:** 27-04-2025  
**Versão:** 1.1  
**Última atualização:** 28-04-2025  
**Autor:** Sistema Claude

## 1. Introdução

### 1.1 Propósito
Este documento especifica os requisitos do Sistema Unificado de Gestão de Sessões e Estado (SUGSE), um sistema projetado para gerenciar sessões de trabalho e manter estado entre sessões no desenvolvimento de software. Originalmente concebido para o projeto DeepCripto, o SUGSE é aplicável ao desenvolvimento de qualquer tipo de código e projetos.

### 1.2 Âmbito
O SUGSE será responsável por:
- Criar, recuperar e finalizar sessões de trabalho
- Persistir e recuperar o estado entre sessões de desenvolvimento
- Fornecer uma API simples para integração com diversos projetos
- Permitir o rastreamento de alterações e resultados entre sessões
- Adaptar comportamentos com base em contextos de desenvolvimento

## 2. Requisitos Funcionais

### 2.1 Gestão de Sessões

#### RF1.1: Criação de Sessões
O sistema DEVE permitir a criação de novas sessões de trabalho.
- Cada sessão DEVE ter um identificador único
- Cada sessão DEVE registar a data e hora de início
- Cada sessão DEVE armazenar metadados como utilizador e objetivo

#### RF1.2: Recuperação de Sessões
O sistema DEVE permitir recuperar sessões anteriores.
- DEVE ser possível listar todas as sessões existentes
- DEVE ser possível filtrar sessões por data ou objetivo
- DEVE ser possível retomar uma sessão anterior

#### RF1.3: Finalização de Sessões
O sistema DEVE permitir finalizar sessões adequadamente.
- DEVE registar a data e hora de finalização
- DEVE registar um sumário de atividades realizadas
- DEVE garantir que todo o estado relevante seja persistido

### 2.2 Gestão de Estado

#### RF2.1: Persistência de Estado
O sistema DEVE persistir o estado do desenvolvimento.
- DEVE armazenar parâmetros e configurações do projeto
- DEVE armazenar resultados intermediários e finais
- DEVE suportar diversos tipos de dados e estruturas

#### RF2.2: Recuperação de Estado
O sistema DEVE permitir recuperar estados anteriores.
- DEVE ser possível recuperar o último estado de um projeto
- DEVE ser possível recuperar estados específicos por ID ou timestamp

#### RF2.3: Versionamento Básico
O sistema DEVE implementar versionamento básico de estado.
- DEVE manter histórico de versões importantes
- DEVE permitir reverter para estados anteriores quando necessário

### 2.3 Interface

#### RF3.1: API REST
O sistema DEVE fornecer uma API REST para acesso às funcionalidades.
- Endpoints para gestão de sessões
- Endpoints para gestão de estado
- Autenticação básica

#### RF3.2: Interface de Linha de Comando
O sistema DEVE fornecer uma CLI para operações básicas.
- Criar/listar/recuperar sessões
- Consultar estados
- Executar operações em batch

### 2.4 Gestão de Contexto

#### RF4.1: Detecção de Contexto
O sistema DEVE ser capaz de detectar contextos de trabalho.
- DEVE analisar conteúdo de sessões ativas
- DEVE identificar palavras-chave configuráveis
- DEVE reconhecer padrões de atividade

#### RF4.2: Gestão de Regras Contextuais
O sistema DEVE suportar regras baseadas em contexto.
- DEVE permitir criar, editar e desativar regras
- DEVE permitir associar regras a contextos específicos
- DEVE suportar relações entre regras, incluindo pesos de relevância

#### RF4.3: Aplicação Contextual
O sistema DEVE adaptar seu comportamento baseado no contexto.
- DEVE pré-carregar regras relacionadas ao contexto atual
- DEVE registar o uso de regras e contextos
- DEVE fornecer estatísticas de utilização por contexto

### 2.5 Interface Contextual

#### RF5.1: API para Gestão de Contexto
O sistema DEVE fornecer endpoints específicos para gestão de contexto.
- Endpoints para CRUD de contextos
- Endpoints para CRUD de regras
- Endpoints para relações entre regras

#### RF5.2: CLI para Operações Contextuais
O sistema DEVE fornecer comandos para gestão de contexto.
- Comandos para criar/listar/testar contextos
- Comandos para definir relações entre regras
- Comandos para visualizar estatísticas

### 2.6 Sistema de Marcadores de Continuidade

#### RF6.1: Definição de Marcadores
O sistema DEVE suportar marcadores de continuidade no código.
- DEVE permitir definir categorias de marcadores padrão
- DEVE reconhecer formatos padronizados (ex. [STATUS:INCOMPLETE])
- DEVE permitir configurar formatos personalizados

#### RF6.2: Extração de Marcadores
O sistema DEVE ser capaz de extrair marcadores dos arquivos do projeto.
- DEVE analisar arquivos modificados em um período configurável
- DEVE extrair o contexto em torno do marcador
- DEVE associar o marcador com a sessão atual

#### RF6.3: Relatórios de Continuidade
O sistema DEVE gerar relatórios sobre os marcadores encontrados.
- DEVE agrupar marcadores por categoria
- DEVE permitir formatação para diferentes formatos (Markdown, JSON)
- DEVE associar os relatórios às sessões de trabalho

### 2.7 Integração Cursor AI

#### RF7.1: Registo de Passos de Conversação
O sistema DEVE permitir gravar cada passo de diálogo (mensagem do utilizador ou do modelo) numa entidade `conversation_step`.
- DEVE armazenar `session_id`, `role`, `content` e contagem de tokens
- DEVE suportar gravação em batch para optimizar latência

#### RF7.2: Recuperação de Contexto
O sistema DEVE disponibilizar endpoint para obter os últimos *N* passos ou um resumo.
- DEVE permitir filtrar por `role` e intervalo de tempo
- DEVE retornar resumo automático quando excedido limite de tokens

#### RF7.3: Resumo Automático
O sistema DEVE gerar automaticamente resumos quando o limite configurável de tokens ou passos for excedido.
- DEVE utilizar modelo extractive por defeito, com opção abstractive
- DEVE persistir o resumo como um `conversation_step` de tipo `summary`

#### RF7.4: Extensão Cursor Bridge
O sistema DEVE fornecer documentação e exemplos para a extensão Cursor AI consumir a API.
- Deve suportar autenticação via token
- Deve fornecer SDK minimamente acoplado em TypeScript (opc.)

## 3. Requisitos Não-Funcionais

### 3.1 Desempenho

#### RNF1.1: Tempo de Resposta
- A API DEVE responder em menos de 500ms para operações comuns
- A recuperação de uma sessão completa NÃO DEVE exceder 3 segundos

#### RNF1.2: Latência de Passos de Conversação
- A gravação de um `conversation_step` DEVE processar em <150 ms na média
- A recuperação dos últimos 20 passos DEVE processar em <300 ms

### 3.2 Segurança

#### RNF2.1: Autenticação e Autorização
- Todas as operações DEVEM ser autenticadas
- Senhas DEVEM ser armazenadas com hash seguro

#### RNF2.2: Proteção de Dados
- Dados sensíveis DEVEM ser tratados com segurança
- Comunicações DEVEM ser encriptadas (TLS)

### 3.3 Confiabilidade

#### RNF3.1: Backup e Recuperação
- Backups completos DEVEM ser realizados diariamente
- O sistema DEVE ser capaz de recuperar dados após falhas

### 3.4 Manutenibilidade

#### RNF4.1: Modularidade
- O sistema DEVE seguir arquitetura modular
- Componentes DEVEM ser testáveis isoladamente

#### RNF4.2: Testabilidade
- Cobertura de testes unitários DEVE ser de no mínimo 70%

#### RNF4.3: Documentação
- Todo código DEVE ser documentado seguindo padrões da linguagem
- API DEVE ter documentação clara

## 4. Restrições Tecnológicas

### 4.1 Linguagens e Frameworks
- Backend DEVE ser implementado em Python 3.10 ou superior
- DEVE utilizar FastAPI para API REST
- DEVE utilizar SQLAlchemy para ORM

### 4.2 Armazenamento
- DEVE utilizar PostgreSQL como banco de dados principal

### 4.3 Implantação
- DEVE ser containerizado com Docker para desenvolvimento
- DEVE ser executável como aplicação standalone

## 5. Critérios de Aceitação

### 5.1 Gestão de Sessões
- DEVE ser possível criar, recuperar e finalizar sessões
- DEVE persistir corretamente todos os metadados de sessão

### 5.2 Gestão de Estado
- DEVE persistir e recuperar corretamente estados
- DEVE manter versionamento básico

### 5.3 Integração
- DEVE fornecer mecanismos de integração com diversos projetos
- DEVE ter integração específica com o projeto DeepCripto
- DEVE ser capaz de migrar dados existentes

## 6. Histórico de Alterações

### Versão 1.0 (27-04-2025)
- Versão inicial do documento

### Versão 1.1 (28-04-2025)
- Atualização do escopo para refletir aplicabilidade a qualquer tipo de desenvolvimento de software
- Remoção de referências específicas a algoritmos de trading
- Adição de suporte para diversos tipos de projetos além do DeepCripto 

### Versão 1.2 (27-04-2025)
- Adição de requisitos para o sistema de marcadores de continuidade 