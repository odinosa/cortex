#!/usr/bin/env python3
"""
CORTEX Database - Gerenciamento do banco de dados SQLite.

Este módulo gerencia conexões e esquema do banco de dados.
"""
import os
import sqlite3
import time
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
import logging

logger = logging.getLogger("cortex.storage")

# Diretório base para dados do CORTEX
CORTEX_DATA_DIR = os.path.expanduser("~/.cortex/data")
CORTEX_DB_PATH = os.path.join(CORTEX_DATA_DIR, "cortex.db")

# Garantir que o diretório de dados existe
os.makedirs(CORTEX_DATA_DIR, exist_ok=True)


def get_db_path() -> str:
    """
    Retorna o caminho para o banco de dados SQLite.
    
    Returns:
        Caminho absoluto para o arquivo do banco de dados
    """
    return CORTEX_DB_PATH


def get_connection() -> sqlite3.Connection:
    """
    Obtém uma conexão com o banco de dados SQLite.
    
    Returns:
        Conexão SQLite configurada
    """
    conn = sqlite3.connect(get_db_path(), isolation_level=None)
    conn.row_factory = sqlite3.Row
    
    # Habilitar foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Habilitar WAL para melhor performance
    conn.execute("PRAGMA journal_mode = WAL")
    
    return conn


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Executa uma consulta SELECT e retorna os resultados.
    
    Args:
        query: Consulta SQL
        params: Parâmetros para a consulta
        
    Returns:
        Lista de dicionários com os resultados
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()


def execute_update(query: str, params: tuple = ()) -> int:
    """
    Executa uma consulta de atualização (INSERT, UPDATE, DELETE).
    
    Args:
        query: Consulta SQL
        params: Parâmetros para a consulta
        
    Returns:
        ID do último registro inserido ou número de linhas afetadas
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params)
        
        # Para INSERT, retorna o último ID
        if query.strip().upper().startswith("INSERT"):
            return cursor.lastrowid
        
        # Para UPDATE/DELETE, retorna o número de linhas afetadas
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()


def execute_script(script: str) -> None:
    """
    Executa um script SQL (múltiplas consultas).
    
    Args:
        script: Script SQL com múltiplas consultas
    """
    conn = get_connection()
    
    try:
        conn.executescript(script)
    finally:
        conn.close()


def init_db() -> None:
    """
    Inicializa o banco de dados com o esquema inicial.
    """
    logger.info("Inicializando banco de dados SQLite")
    
    # Criar tabelas apenas se não existirem
    schema_script = """
    -- Tabela de projetos
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        workspace_path TEXT UNIQUE,
        description TEXT,
        jira_project_key TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN NOT NULL DEFAULT 1
    );
    
    -- Tabela de sessões
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        title TEXT NOT NULL,
        objective TEXT,
        start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        summary TEXT,
        next_session_context TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    
    -- Tabela de mensagens
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        role TEXT NOT NULL, -- 'user', 'assistant', 'system', 'summary'
        content TEXT NOT NULL,
        token_count INTEGER,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    );
    
    -- Tabela de tarefas
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        parent_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        level TEXT NOT NULL, -- 'phase', 'stage', 'task', 'activity'
        status TEXT NOT NULL, -- 'not_started', 'in_progress', 'blocked', 'completed'
        progress INTEGER NOT NULL DEFAULT 0, -- 0-100
        jira_id TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        estimated_hours REAL,
        actual_hours REAL,
        order_index INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (parent_id) REFERENCES tasks(id)
    );
    
    -- Tabela de relações entre tarefas
    CREATE TABLE IF NOT EXISTS task_relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_task_id INTEGER NOT NULL,
        target_task_id INTEGER NOT NULL,
        relation_type TEXT NOT NULL, -- 'blocks', 'depends_on', 'related_to', 'duplicates'
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_task_id) REFERENCES tasks(id),
        FOREIGN KEY (target_task_id) REFERENCES tasks(id)
    );
    
    -- Tabela de marcadores
    CREATE TABLE IF NOT EXISTS markers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        task_id INTEGER,
        marker_type TEXT NOT NULL, -- 'TODO', 'FIXME', 'NOTE'
        content TEXT NOT NULL,
        file_path TEXT NOT NULL,
        line_number INTEGER NOT NULL,
        context TEXT,
        detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (task_id) REFERENCES tasks(id)
    );
    
    -- Tabela de contextos
    CREATE TABLE IF NOT EXISTS contexts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        task_id INTEGER,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (task_id) REFERENCES tasks(id)
    );
    
    -- Tabela de regras
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        condition TEXT NOT NULL, -- JSON condition
        action TEXT NOT NULL, -- JSON action
        priority INTEGER NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    
    -- Índices para performance
    CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_id);
    CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
    CREATE INDEX IF NOT EXISTS idx_markers_project ON markers(project_id);
    CREATE INDEX IF NOT EXISTS idx_markers_task ON markers(task_id);
    CREATE INDEX IF NOT EXISTS idx_contexts_project ON contexts(project_id);
    CREATE INDEX IF NOT EXISTS idx_contexts_task ON contexts(task_id);
    """
    
    execute_script(schema_script)
    logger.info("Esquema do banco de dados inicializado")


def backup_db(backup_path: Optional[str] = None) -> str:
    """
    Cria um backup do banco de dados.
    
    Args:
        backup_path: Caminho opcional para o arquivo de backup
        
    Returns:
        Caminho absoluto para o arquivo de backup
    """
    if backup_path is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.expanduser("~/.cortex/backups")
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"cortex_backup_{timestamp}.db")
    
    # Conexão com banco de dados atual
    source_conn = get_connection()
    
    # Conexão com o arquivo de backup
    dest_conn = sqlite3.connect(backup_path)
    
    # Fazer backup
    source_conn.backup(dest_conn)
    
    # Fechar conexões
    source_conn.close()
    dest_conn.close()
    
    logger.info(f"Backup do banco de dados criado em {backup_path}")
    return backup_path


def restore_db(backup_path: str) -> bool:
    """
    Restaura o banco de dados a partir de um backup.
    
    Args:
        backup_path: Caminho para o arquivo de backup
        
    Returns:
        True se a restauração for bem-sucedida, False caso contrário
    """
    if not os.path.exists(backup_path):
        logger.error(f"Arquivo de backup não encontrado: {backup_path}")
        return False
    
    # Criar backup do banco atual antes da restauração
    current_backup = backup_db()
    
    try:
        # Conexão com o arquivo de backup
        source_conn = sqlite3.connect(backup_path)
        
        # Conexão com banco de dados atual
        dest_conn = get_connection()
        
        # Fazer restauração
        source_conn.backup(dest_conn)
        
        # Fechar conexões
        source_conn.close()
        dest_conn.close()
        
        logger.info(f"Banco de dados restaurado a partir de {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao restaurar banco de dados: {str(e)}")
        logger.info(f"Backup realizado em: {current_backup}")
        return False 