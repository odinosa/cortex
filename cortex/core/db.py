"""
Configuração de conexão com o banco de dados e sessão SQLAlchemy.
"""

import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

import structlog

logger = structlog.get_logger()

# Base Model declarativa do SQLAlchemy
Base = declarative_base()

# Configuração de URLs de conexão
DEFAULT_DATABASE_URL = "postgresql://cortex:cortexpass@localhost:5433/cortex"
TEST_DATABASE_URL = "sqlite:///:memory:"

# Variáveis de configuração de database
db_url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
db_pool_size = int(os.environ.get("DATABASE_POOL_SIZE", "10"))
db_max_overflow = int(os.environ.get("DATABASE_MAX_OVERFLOW", "20"))
db_pool_timeout = int(os.environ.get("DATABASE_POOL_TIMEOUT", "30"))
db_echo = os.environ.get("DATABASE_ECHO", "false").lower() == "true"


# Ativar suporte a FOREIGN KEY no SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if db_url.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Engine do SQLAlchemy
engine = create_engine(
    db_url,
    echo=db_echo,
    pool_size=db_pool_size if not db_url.startswith("sqlite") else None,
    max_overflow=db_max_overflow if not db_url.startswith("sqlite") else None,
    pool_timeout=db_pool_timeout if not db_url.startswith("sqlite") else None,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    poolclass=QueuePool if not db_url.startswith("sqlite") else None,
)

# Factory de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager para obter uma sessão de banco de dados.
    
    Yields:
        Session: Sessão SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error("Erro na transação do banco de dados", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


def get_engine() -> Engine:
    """
    Retorna o engine atual do SQLAlchemy.
    
    Returns:
        Engine: Engine SQLAlchemy.
    """
    return engine


def create_tables() -> None:
    """
    Cria todas as tabelas definidas nos modelos.
    Útil para testes e ambientes de desenvolvimento.
    """
    Base.metadata.create_all(bind=engine)


def init_db() -> None:
    """
    Inicializa o banco de dados se necessário.
    """
    # Importar modelos aqui para tê-los disponíveis para criação de tabelas
    import cortex.core.models.session
    import cortex.core.models.message
    import cortex.core.models.task
    import cortex.core.models.state
    import cortex.core.models.marker
    
    logger.info("Inicializando banco de dados")
    create_tables()
    logger.info("Banco de dados inicializado")


def use_test_db() -> None:
    """
    Configura o banco de dados para testes (SQLite em memória).
    """
    global engine, SessionLocal, db_url
    db_url = TEST_DATABASE_URL
    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    create_tables()
    logger.info("Banco de dados de teste configurado", db_url=db_url) 