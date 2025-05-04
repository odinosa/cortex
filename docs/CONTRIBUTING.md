# Guia de Contribuição para o CORTEX

*Última atualização:* 05-05-2025

Este documento descreve como podes contribuir para o desenvolvimento do CORTEX.

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.10 ou superior
- Git
- macOS (recomendado para consistência com o ambiente principal)

### Passos de Configuração

1. **Fork e Clone do Repositório**:
   ```bash
   git clone https://github.com/odinosa/cortex.git
   cd cortex
   ```

2. **Configuração do Ambiente Virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instalação em Modo de Desenvolvimento**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Inicialização do Banco de Dados**:
   ```bash
   python -m cortex.cli init
   ```

5. **Configuração para Dogfooding**:
   ```bash
   # Iniciar servidor CORTEX para usar durante o desenvolvimento
   python -m cortex.cli serve &
   python -m cortex.cli setup-cursor
   
   # Criar sessão para trabalhar no CORTEX
   python -m cortex.cli start "Desenvolvimento CORTEX" "Contribuir com o CORTEX"
   ```

## Fluxo de Desenvolvimento

### Ramos e Convenções

- `main`: Ramo principal, sempre estável
- `develop`: Ramo de desenvolvimento ativo
- `feature/nome-da-feature`: Para novas funcionalidades
- `bugfix/nome-do-bug`: Para correções de bugs
- `docs/nome-da-documentacao`: Para atualizações de documentação

### Processo de Contribuição

1. **Criar um Ramo para sua Contribuição**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/sua-funcionalidade
   ```

2. **Desenvolver sua Contribuição**:
   - Siga as convenções de código do projeto
   - Adicione testes para novas funcionalidades
   - Atualize a documentação conforme necessário
   - Use o CORTEX para gerenciar suas tarefas (dogfooding)

3. **Executar Testes Locais**:
   ```bash
   # Executar todos os testes
   pytest
   
   # Verificar formatação
   black cortex tests
   isort cortex tests
   
   # Verificar tipagem
   mypy cortex
   
   # Analisar qualidade de código
   python -m cortex.cli analyze ./cortex
   ```

4. **Submeter sua Contribuição**:
   ```bash
   git add .
   git commit -m "feature: adiciona funcionalidade XYZ"
   git push origin feature/sua-funcionalidade
   ```

5. **Criar um Pull Request**:
   - Abra um PR do seu ramo para o ramo `develop`
   - Descreva claramente o propósito e as alterações realizadas
   - Referencie quaisquer issues relacionadas
   - Inclua métricas de impacto se disponíveis

## Convenções de Código

### Estilo de Código

- Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/) para Python
- Use tipagem estática com `mypy`
- Formatação automática com `black` (88 caracteres por linha)
- Importações organizadas com `isort`
- Complexidade máxima por função: 15 (verificada pelo `radon`)

### Convenções de Nomenclatura

- **Classes**: `CamelCase`
- **Funções/Variáveis**: `snake_case`
- **Constantes**: `UPPERCASE`
- **Módulos**: `snake_case`
- **Diretórios**: `snake_case`

### Documentação

- Docstrings para todas as classes, funções e métodos
- Comentários para código complexo ou não óbvio
- Manter documentação de usuário atualizada em arquivos Markdown
- Documentar novas ferramentas MCP no formato padrão

### Convenções de Commits

Seguimos um formato semelhante ao [Conventional Commits](https://www.conventionalcommits.org/):

- `feature: descrição da nova funcionalidade`
- `fix: descrição da correção de bug`
- `docs: atualização na documentação`
- `refactor: melhoria no código sem alteração de comportamento`
- `test: adição ou modificação de testes`
- `chore: alterações em ferramentas, configuração, etc.`

## Trabalhando com Componentes Específicos

### Sistema de Automação

Ao contribuir para o sistema de automação:
1. Documente a trigger, condições e ações claramente
2. Adicione testes abrangentes para diferentes cenários
3. Considere impacto na performance e recursos
4. Use o formato JSON padronizado para condições e ações

### Análise de Código

Ao contribuir para o motor de análise:
1. Utilize bibliotecas estabelecidas (radon, bandit, etc.) quando possível
2. Calibre cuidadosamente pontuações e limites
3. Adicione testes com casos reais e sintéticos
4. Documente claramente métricas e interpretações

### Métricas e Dashboard

Ao contribuir para o sistema de métricas:
1. Otimize consultas SQL para performance
2. Considere o impacto na usabilidade do terminal
3. Teste em diferentes tamanhos de terminal
4. Documente algoritmos de cálculo de métricas

### Integrações com LLM

Ao contribuir para integrações LLM:
1. Mantenha prompts e contextos no formato padronizado
2. Documente o propósito e formato esperado de saída
3. Considere casos de falha e recuperação
4. Adicione testes com mock respostas

## Processo de Revisão

Seu código será revisado por pelo menos um mantenedor do projeto. Para acelerar o processo:

1. Certifique-se de que todos os testes estão passando
2. Siga as convenções de código e documentação
3. Mantenha o escopo da sua contribuição focado e compreensível
4. Responda a comentários de forma oportuna
5. Inclua análise de código e métricas quando relevante

## Relatando Bugs e Solicitando Funcionalidades

- Use o sistema de issues do GitHub
- Forneça detalhes completos para bugs (passos para reproduzir, ambiente, etc.)
- Para solicitações de funcionalidades, explique o caso de uso e os benefícios
- Inclua logs de sistema ou métricas quando disponíveis

## Notas Adicionais

### Sistema de Banco de Dados

Ao modificar o esquema do banco de dados:
1. Atualize `DATA_MODEL.md`
2. Adicione migrações na pasta `cortex/storage/migrations/`
3. Atualize os testes relacionados
4. Considere impacto em performance para tabelas grandes

### Abordagem Híbrida SQLite + Markdown

Ao trabalhar com a funcionalidade de sincronização SQLite-Markdown:
1. Teste rigorosamente casos de borda e conflitos
2. Documente claramente qualquer mudança no formato ou comportamento
3. Considere a experiência de edição manual

### Cache Adaptativo

Ao trabalhar com o sistema de cache:
1. Documente a estratégia e política de expiração
2. Adicione métricas de eficácia (hit/miss ratio)
3. Considere o impacto em memória e performance

### Monitoramento de Sistema

Ao trabalhar com monitoramento de recursos:
1. Minimize o overhead de coleta de métricas
2. Considere o impacto em bateria e performance
3. Teste em diferentes configurações de hardware

## Dogfooding

Encorajamos fortemente o uso do CORTEX para gerenciar o desenvolvimento do próprio CORTEX. Isso proporciona:

1. Validação em tempo real das funcionalidades
2. Identificação de problemas de usabilidade
3. Insights para melhorias
4. Exemplo prático de uso

Para iniciar uma sessão de desenvolvimento CORTEX:

```bash
# No Cursor, após abrir o repositório
/cortex:start "Desenvolvimento CORTEX" "Trabalhar na funcionalidade XYZ"

# Criar tarefas para sua contribuição
/cortex:task "Implementar funcionalidade XYZ" --level task

# Ao final da sessão
/cortex:summarize
```

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto. 