#!/bin/bash
# CORTEX Bootstrap Script
# Configura ambiente de desenvolvimento completo

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PYTHON_MIN_VERSION="3.12.0"
PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
VENV_DIR="${PROJECT_ROOT}/.venv"

# Funções auxiliares
log_info() {
  echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
  exit 1
}

check_python_version() {
  local python_cmd=$1
  local python_version=$($python_cmd -c "import sys; print('.'.join(map(str, sys.version_info[:3])))")
  
  log_info "Verificando versão do Python: $python_version"
  
  if ! command -v python3 &> /dev/null; then
    log_error "Python 3 não encontrado. Por favor, instale o Python $PYTHON_MIN_VERSION ou superior."
  fi
  
  if [ "$(printf '%s\n' "$PYTHON_MIN_VERSION" "$python_version" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]; then
    log_error "Versão do Python ($python_version) é menor que a requerida ($PYTHON_MIN_VERSION). Por favor, atualize o Python."
  fi
  
  log_success "Versão do Python OK: $python_version"
}

create_venv() {
  if [ -d "$VENV_DIR" ]; then
    log_info "Ambiente virtual já existe em: $VENV_DIR"
    read -p "Deseja recriá-lo? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      log_info "Removendo ambiente virtual existente..."
      rm -rf "$VENV_DIR"
    else
      log_info "Mantendo ambiente virtual existente."
      return
    fi
  fi
  
  log_info "Criando ambiente virtual Python em: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
  log_success "Ambiente virtual criado com sucesso!"
}

install_dependencies() {
  log_info "Instalando dependências do projeto..."
  
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip setuptools wheel
  
  # Instalação em modo de desenvolvimento com extras
  pip install -e ".[dev]"
  
  log_success "Dependências instaladas com sucesso!"
}

setup_pre_commit() {
  log_info "Configurando pre-commit hooks..."
  
  if [ ! -f "$PROJECT_ROOT/.git/hooks/pre-commit" ]; then
    source "$VENV_DIR/bin/activate"
    pre-commit install
    log_success "Pre-commit hooks configurados com sucesso!"
  else
    log_info "Pre-commit hooks já configurados."
  fi
}

check_postgresql() {
  log_info "Verificando disponibilidade do PostgreSQL..."
  
  if ! command -v docker &> /dev/null; then
    log_warning "Docker não encontrado, não será possível verificar o PostgreSQL automaticamente."
    log_warning "Certifique-se de que o PostgreSQL 14+ está instalado e acessível na porta 5433."
    return
  fi
  
  if ! docker ps | grep -q "postgres"; then
    log_info "PostgreSQL não detectado em execução. Iniciando via Docker..."
    
    if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
      cd "$PROJECT_ROOT" && docker-compose up -d db
      log_success "PostgreSQL iniciado via docker-compose!"
    else
      log_warning "Arquivo docker-compose.yml não encontrado."
      log_warning "Certifique-se de que o PostgreSQL 14+ está instalado e acessível na porta 5433."
    fi
  else
    log_success "PostgreSQL detectado em execução!"
  fi
}

create_basic_structure() {
  log_info "Criando estrutura básica de diretórios..."
  
  mkdir -p "$PROJECT_ROOT/cortex/core"
  mkdir -p "$PROJECT_ROOT/cortex/mcp/tools"
  mkdir -p "$PROJECT_ROOT/cortex/cli"
  mkdir -p "$PROJECT_ROOT/tests"
  
  # Criar __init__.py básicos
  touch "$PROJECT_ROOT/cortex/__init__.py"
  touch "$PROJECT_ROOT/cortex/core/__init__.py"
  touch "$PROJECT_ROOT/cortex/mcp/__init__.py"
  touch "$PROJECT_ROOT/cortex/mcp/tools/__init__.py"
  touch "$PROJECT_ROOT/cortex/cli/__init__.py"
  touch "$PROJECT_ROOT/tests/__init__.py"
  
  log_success "Estrutura básica criada!"
}

execute_migrations() {
  log_info "Verificando migrações do banco de dados..."
  
  if [ -d "$PROJECT_ROOT/alembic" ]; then
    source "$VENV_DIR/bin/activate"
    
    if command -v alembic &> /dev/null; then
      log_info "Executando migrações..."
      cd "$PROJECT_ROOT" && alembic upgrade head
      log_success "Migrações aplicadas com sucesso!"
    else
      log_warning "Alembic não encontrado no ambiente virtual. Pulando migrações."
    fi
  else
    log_warning "Diretório alembic não encontrado. Pulando migrações."
    log_info "Execute 'alembic init alembic' para inicializar quando estiver pronto."
  fi
}

# Execução principal
main() {
  echo -e "\n${CYAN}======== CORTEX - BOOTSTRAP ========${NC}\n"
  
  check_python_version "python3"
  create_venv
  install_dependencies
  setup_pre_commit
  create_basic_structure
  check_postgresql
  execute_migrations
  
  echo -e "\n${GREEN}========= SETUP CONCLUÍDO ==========${NC}\n"
  echo -e "Para iniciar o desenvolvimento:"
  echo -e "  1. ${YELLOW}source ${VENV_DIR}/bin/activate${NC}"
  echo -e "  2. ${YELLOW}cd ${PROJECT_ROOT}${NC}"
  echo -e "  3. ${YELLOW}python -m cortex.cli serve --dev${NC}"
  echo -e "\nBom desenvolvimento! 🚀\n"
}

main 