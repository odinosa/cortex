#!/usr/bin/env python3
"""
CORTEX MCP Server - Implementação do servidor Model Context Protocol (MCP).

Este módulo gerencia a comunicação com o Cursor via stdio.
"""
import json
import logging
import os
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Tuple, Union

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/.cortex/logs/server.log")),
        logging.StreamHandler() if "--debug" in sys.argv else logging.NullHandler(),
    ],
)
logger = logging.getLogger("cortex.mcp")

# Garantir que o diretório de logs existe
os.makedirs(os.path.expanduser("~/.cortex/logs"), exist_ok=True)

# Importa ferramentas MCP
from cortex.mcp.tools.session_tools import start_session, end_session, get_context, record_message
from cortex.mcp.tools.task_tools import create_task, update_task_status, list_tasks
from cortex.mcp.tools.marker_tools import scan_markers
from cortex.mcp.tools.context_tools import detect_context, add_context, apply_rule

# Registro de ferramentas disponíveis
AVAILABLE_TOOLS = {
    "start_session": start_session,
    "end_session": end_session,
    "record_message": record_message,
    "get_context": get_context,
    "create_task": create_task,
    "update_task_status": update_task_status,
    "list_tasks": list_tasks,
    "scan_markers": scan_markers,
    "detect_context": detect_context,
    "add_context": add_context,
    "apply_rule": apply_rule,
}


def parse_mcp_request(request_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Interpreta uma requisição MCP e extrai o nome da ferramenta e seus parâmetros.
    
    Args:
        request_data: Dados da requisição MCP
        
    Returns:
        Tupla contendo o nome da ferramenta e um dicionário de parâmetros
    """
    try:
        tool_name = request_data.get("name", "")
        parameters = request_data.get("parameters", {})
        
        return tool_name, parameters
    except Exception as e:
        logger.error(f"Erro ao interpretar requisição MCP: {str(e)}")
        return "", {}


def handle_mcp_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa uma requisição MCP chamando a ferramenta apropriada.
    
    Args:
        request_data: Dados da requisição MCP
        
    Returns:
        Resultado da execução da ferramenta ou mensagem de erro
    """
    tool_name, parameters = parse_mcp_request(request_data)
    
    if not tool_name:
        return {"error": "Tool name not provided"}
    
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Unknown tool: {tool_name}"}
    
    try:
        # Executa a ferramenta com os parâmetros
        logger.info(f"Executando ferramenta: {tool_name}")
        result = AVAILABLE_TOOLS[tool_name](**parameters)
        
        return result
    except Exception as e:
        logger.error(f"Erro ao executar {tool_name}: {str(e)}")
        return {"error": f"Error executing {tool_name}: {str(e)}"}


def mcp_read_request() -> Optional[Dict[str, Any]]:
    """
    Lê uma requisição MCP da entrada padrão.
    
    Returns:
        Dicionário com dados da requisição ou None se não conseguir ler
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return None
            
        # Tenta interpretar como JSON
        request_data = json.loads(line)
        return request_data
    except json.JSONDecodeError:
        logger.error(f"Recebido JSON inválido: {line}")
        return None
    except Exception as e:
        logger.error(f"Erro ao ler requisição: {str(e)}")
        return None


def mcp_write_response(response: Dict[str, Any]) -> bool:
    """
    Escreve uma resposta MCP na saída padrão.
    
    Args:
        response: Dados da resposta
        
    Returns:
        True se conseguir escrever, False caso contrário
    """
    try:
        # Converte resposta para JSON
        json_response = json.dumps(response)
        
        # Escreve na saída padrão
        sys.stdout.write(json_response + "\n")
        sys.stdout.flush()
        
        return True
    except Exception as e:
        logger.error(f"Erro ao escrever resposta: {str(e)}")
        return False


def mcp_server_loop() -> None:
    """Loop principal do servidor MCP."""
    logger.info("Iniciando loop do servidor MCP")
    
    while True:
        try:
            # Lê requisição
            request = mcp_read_request()
            if request is None:
                # Se não conseguir ler, pode significar que o cliente desconectou
                time.sleep(0.1)
                continue
                
            # Processa requisição
            response = handle_mcp_request(request)
            
            # Envia resposta
            mcp_write_response(response)
        except KeyboardInterrupt:
            logger.info("Servidor MCP finalizado pelo usuário")
            break
        except Exception as e:
            logger.error(f"Erro no loop principal: {str(e)}")
            # Não quebra o loop para manter o servidor rodando


def start_http_server(port: int) -> None:
    """
    Inicia um servidor HTTP simples para debugging e administração.
    
    Args:
        port: Porta onde o servidor vai escutar
    """
    # Implementação será adicionada mais tarde
    pass


def start_server(dev_mode: bool = False, http_port: Optional[int] = None) -> None:
    """
    Inicia o servidor MCP e, opcionalmente, um servidor HTTP.
    
    Args:
        dev_mode: Se True, ativa logs de debug e outras ferramentas
        http_port: Porta para o servidor HTTP opcional
    """
    logger.info(f"Iniciando servidor CORTEX (dev_mode={dev_mode})")
    
    if dev_mode:
        logger.setLevel(logging.DEBUG)
    
    # Inicia servidor HTTP em thread separada, se solicitado
    if http_port is not None:
        logger.info(f"Iniciando servidor HTTP na porta {http_port}")
        http_thread = threading.Thread(
            target=start_http_server,
            args=(http_port,),
            daemon=True
        )
        http_thread.start()
    
    # Inicia o loop principal
    try:
        mcp_server_loop()
    except KeyboardInterrupt:
        logger.info("Servidor finalizado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Se executado diretamente, inicia servidor com argumentos da linha de comando
    dev_mode = "--dev" in sys.argv
    
    # Extrai porta HTTP dos argumentos, se presente
    http_port = None
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            try:
                http_port = int(sys.argv[i + 1])
            except ValueError:
                pass
    
    start_server(dev_mode=dev_mode, http_port=http_port) 