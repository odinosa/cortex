#!/usr/bin/env python3
"""
CORTEX Config - Gestão de configurações.

Este módulo gerencia as configurações do sistema.
"""
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("cortex.core.config")

# Diretórios e arquivos de configuração
CORTEX_HOME = os.path.expanduser("~/.cortex")
CORTEX_CONFIG_FILE = os.path.join(CORTEX_HOME, "config.json")
CURSOR_MCP_PATH = os.path.expanduser("~/.cursor/mcp.json")

# Configurações padrão
DEFAULT_CONFIG = {
    "version": "0.1.0",
    "log_level": "INFO",
    "data_dir": os.path.join(CORTEX_HOME, "data"),
    "auto_start": False,
    "http_enabled": False,
    "http_port": 8765,
    "jira": {
        "enabled": False,
        "url": "",
        "api_key": "",
    },
    "features": {
        "task_hierarchy": True,
        "context_detection": True,
        "marker_scanning": True,
    },
}


def ensure_config_dir() -> None:
    """
    Garante que o diretório de configuração existe.
    """
    os.makedirs(CORTEX_HOME, exist_ok=True)
    os.makedirs(os.path.join(CORTEX_HOME, "logs"), exist_ok=True)
    os.makedirs(os.path.join(CORTEX_HOME, "data"), exist_ok=True)
    os.makedirs(os.path.join(CORTEX_HOME, "backups"), exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Carrega a configuração do CORTEX.
    
    Returns:
        Dicionário com as configurações
    """
    ensure_config_dir()
    
    # Se não existe arquivo de configuração, cria com padrões
    if not os.path.exists(CORTEX_CONFIG_FILE):
        with open(CORTEX_CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG.copy()
    
    # Carrega configuração existente
    try:
        with open(CORTEX_CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        # Garantir que todas as chaves padrão existem
        updated = False
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
                updated = True
                
        # Se precisou adicionar chaves padrão, salva o arquivo atualizado
        if updated:
            save_config(config)
            
        return config
    except Exception as e:
        logger.error(f"Erro ao carregar configuração: {str(e)}")
        logger.info("Usando configuração padrão")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """
    Salva a configuração do CORTEX.
    
    Args:
        config: Dicionário com as configurações
        
    Returns:
        True se conseguir salvar, False caso contrário
    """
    ensure_config_dir()
    
    try:
        with open(CORTEX_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {str(e)}")
        return False


def update_config(key: str, value: Any) -> bool:
    """
    Atualiza uma configuração específica.
    
    Args:
        key: Chave da configuração
        value: Novo valor
        
    Returns:
        True se conseguir atualizar, False caso contrário
    """
    config = load_config()
    
    # Suporta chaves aninhadas tipo "jira.enabled"
    if "." in key:
        parts = key.split(".")
        current = config
        
        # Navega até o penúltimo nível
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
            
        # Define o valor no último nível
        current[parts[-1]] = value
    else:
        config[key] = value
    
    return save_config(config)


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Obtém um valor de configuração específico.
    
    Args:
        key: Chave da configuração
        default: Valor padrão se a chave não existir
        
    Returns:
        Valor da configuração ou o valor padrão
    """
    config = load_config()
    
    # Suporta chaves aninhadas tipo "jira.enabled"
    if "." in key:
        parts = key.split(".")
        current = config
        
        # Navega até o valor
        for part in parts:
            if part not in current:
                return default
            current = current[part]
            
        return current
    else:
        return config.get(key, default)


def setup_cursor_integration(force: bool = False) -> bool:
    """
    Configura a integração com o Cursor via MCP.
    
    Args:
        force: Se True, sobrescreve configuração existente
        
    Returns:
        True se configuração for realizada com sucesso, False caso contrário
    """
    cursor_dir = os.path.dirname(CURSOR_MCP_PATH)
    
    # Verifica se o diretório do Cursor existe
    if not os.path.exists(cursor_dir):
        os.makedirs(cursor_dir, exist_ok=True)
    
    # Define a configuração MCP para o CORTEX
    cortex_mcp_config = {
        "tools": [
            {
                "id": "cortex",
                "stdio": {
                    "command": ["python", "-m", "cortex.mcp.server"]
                },
                "tools": [
                    "start_session",
                    "end_session", 
                    "record_message",
                    "get_context",
                    "create_task",
                    "update_task_status",
                    "list_tasks",
                    "scan_markers",
                    "detect_context",
                    "add_context",
                    "apply_rule"
                ]
            }
        ]
    }
    
    try:
        # Lê configuração MCP atual, se existir
        mcp_config = {}
        if os.path.exists(CURSOR_MCP_PATH) and not force:
            with open(CURSOR_MCP_PATH, 'r') as f:
                mcp_config = json.load(f)
                
            # Verifica se já existe configuração para o CORTEX
            for tool in mcp_config.get("tools", []):
                if tool.get("id") == "cortex":
                    logger.info("Configuração CORTEX já existe no MCP do Cursor")
                    return False
            
            # Adiciona CORTEX às ferramentas existentes
            if "tools" not in mcp_config:
                mcp_config["tools"] = []
            mcp_config["tools"].append(cortex_mcp_config["tools"][0])
        else:
            # Usa configuração padrão
            mcp_config = cortex_mcp_config
        
        # Salva configuração MCP
        with open(CURSOR_MCP_PATH, 'w') as f:
            json.dump(mcp_config, f, indent=2)
            
        logger.info("Configuração MCP do Cursor atualizada com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao configurar integração com Cursor: {str(e)}")
        return False 