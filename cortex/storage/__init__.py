"""
CORTEX Storage - Gestão de persistência de dados.

Este subpacote contém a implementação do armazenamento de dados.
"""

from cortex.storage.database import (
    init_db,
    get_connection,
    execute_query,
    execute_update,
    execute_script,
    backup_db,
    restore_db,
)

__all__ = [
    "init_db",
    "get_connection",
    "execute_query",
    "execute_update",
    "execute_script",
    "backup_db",
    "restore_db",
] 