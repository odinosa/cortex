# Guia de Contribuição para o CORTEX

*Última atualização:* 09-07-2024

Este documento descreve como podes contribuir para o desenvolvimento do CORTEX.

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.10 ou superior
- Git
- macOS (recomendado para consistência com o ambiente principal)

### Passos de Configuração

1. **Fork e Clone do Repositório**:
   ```bash
   git clone https://github.com/SEU_USERNAME/cortex.git
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

3. **Executar Testes Locais**:
   ```bash
   # Executar todos os testes
   pytest
   
   # Verificar formatação
   black cortex tests
   isort cortex tests
   
   # Verificar tipagem
   mypy cortex
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

## Convenções de Código

### Estilo de Código

- Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/) para Python
- Use tipagem estática com `mypy`
- Formatação automática com `black` (88 caracteres por linha)
- Importações organizadas com `isort`

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

### Convenções de Commits

Seguimos um formato semelhante ao [Conventional Commits](https://www.conventionalcommits.org/):

- `feature: descrição da nova funcionalidade`
- `fix: descrição da correção de bug`
- `docs: atualização na documentação`
- `refactor: melhoria no código sem alteração de comportamento`
- `test: adição ou modificação de testes`
- `chore: alterações em ferramentas, configuração, etc.`

## Processo de Revisão

Seu código será revisado por pelo menos um mantenedor do projeto. Para acelerar o processo:

1. Certifique-se de que todos os testes estão passando
2. Siga as convenções de código e documentação
3. Mantenha o escopo da sua contribuição focado e compreensível
4. Responda a comentários de forma oportuna

## Relatando Bugs e Solicitando Funcionalidades

- Use o sistema de issues do GitHub
- Forneça detalhes completos para bugs (passos para reproduzir, ambiente, etc.)
- Para solicitações de funcionalidades, explique o caso de uso e os benefícios

## Notas Adicionais

### Sistema de Banco de Dados

Ao modificar o esquema do banco de dados:
1. Atualize `DATA_MODEL.md`
2. Adicione migrações na pasta `cortex/storage/migrations/`
3. Atualize os testes relacionados

### Abordagem Híbrida SQLite + Markdown

Ao trabalhar com a funcionalidade de sincronização SQLite-Markdown:
1. Teste rigorosamente casos de borda e conflitos
2. Documente claramente qualquer mudança no formato ou comportamento

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto. 