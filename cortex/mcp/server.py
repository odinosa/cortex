#!/usr/bin/env python
"""
CORTEX MCP Server - Servidor principal do Model Context Protocol

Implementação do servidor MCP que recebe comandos via stdio/stdout.
"""

import json
import logging
import os
import sys
import traceback
from typing import Any, Dict, List, Optional, Union

import structlog

# Configurar logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.dev.ConsoleRenderer(),
    ]
)

logger = structlog.get_logger()


class MCPError(Exception):
    """Erro genérico de MCP."""
    
    def __init__(self, message: str, code: str = "internal_error"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class MCPServer:
    """
    Servidor principal MCP para CORTEX.
    
    Processa comandos MCP recebidos via stdin e envia respostas via stdout.
    """
    
    def __init__(self):
        self.tools = {}
        self.register_tools()
        logger.info("MCPServer inicializado")
    
    def register_tools(self):
        """Registra todas as ferramentas disponíveis."""
        try:
            # Importar dinamicamente para evitar dependências circulares
            from cortex.mcp.tools.session import start_session, end_session, list_sessions
            from cortex.mcp.tools.conversation import record_message, get_context, summarize_conversation
            from cortex.mcp.tools.markers import scan_markers
            
            # Mapear ferramentas para funções
            self.tools = {
                "start_session": start_session,
                "end_session": end_session,
                "list_sessions": list_sessions,
                "record_message": record_message,
                "get_context": get_context,
                "summarize_conversation": summarize_conversation,
                "scan_markers": scan_markers,
            }
            
            logger.info("Ferramentas MCP registadas", count=len(self.tools))
        except ImportError as e:
            logger.error("Erro ao importar ferramentas", error=str(e))
            # Implementar stubs temporários para desenvolvimento
            self.register_stub_tools()
    
    def register_stub_tools(self):
        """Registra ferramentas stub para desenvolvimento."""
        def stub_tool(*args, **kwargs):
            return {"status": "stub", "message": "Esta ferramenta ainda não está implementada"}
        
        self.tools = {
            "start_session": stub_tool,
            "end_session": stub_tool,
            "list_sessions": stub_tool,
            "record_message": stub_tool,
            "get_context": stub_tool,
            "summarize_conversation": stub_tool,
            "scan_markers": stub_tool,
        }
        logger.warning("Usando ferramentas STUB para desenvolvimento")
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa uma requisição MCP.
        
        Args:
            request: Dicionário de requisição JSON
            
        Returns:
            Resposta JSON formatada
        """
        try:
            # Validar requisição
            if "id" not in request:
                raise MCPError("Campo 'id' ausente na requisição", "invalid_request")
            
            if "method" not in request:
                raise MCPError("Campo 'method' ausente na requisição", "invalid_request")
            
            method = request["method"]
            req_id = request["id"]
            params = request.get("params", {})
            
            # Verificar se o método existe
            if method not in self.tools:
                raise MCPError(f"Método não encontrado: {method}", "method_not_found")
            
            # Executar o método
            logger.info("Processando requisição", method=method, req_id=req_id)
            result = self.tools[method](**params)
            
            # Formatar resposta de sucesso
            return {
                "id": req_id,
                "result": result,
            }
            
        except MCPError as e:
            # Erros conhecidos de MCP
            logger.warning("Erro MCP", error=str(e), code=e.code)
            return {
                "id": request.get("id", 0),
                "error": {
                    "code": e.code,
                    "message": str(e),
                }
            }
        except Exception as e:
            # Erros não tratados
            logger.error(
                "Erro não tratado",
                error=str(e),
                traceback=traceback.format_exc()
            )
            return {
                "id": request.get("id", 0),
                "error": {
                    "code": "internal_error",
                    "message": f"Erro interno: {str(e)}",
                }
            }
    
    def run(self):
        """Executa o loop principal de processamento de requisições."""
        logger.info("Iniciando servidor MCP")
        
        try:
            # Loop principal
            for line in sys.stdin:
                # Pular linhas vazias
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parsear JSON
                    request = json.loads(line)
                    
                    # Processar requisição
                    response = self.process_request(request)
                    
                    # Enviar resposta
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                    
                except json.JSONDecodeError:
                    logger.error("JSON inválido na entrada", input=line[:100])
                    sys.stdout.write(
                        json.dumps({
                            "id": 0,
                            "error": {
                                "code": "parse_error",
                                "message": "Não foi possível parsear a requisição JSON",
                            }
                        }) + "\n"
                    )
                    sys.stdout.flush()
        
        except KeyboardInterrupt:
            logger.info("Servidor interrompido")
        except Exception as e:
            logger.critical(
                "Erro fatal no servidor",
                error=str(e),
                traceback=traceback.format_exc()
            )
            sys.exit(1)


def main():
    """Função principal."""
    try:
        server = MCPServer()
        server.run()
    except Exception as e:
        logger.critical("Falha ao iniciar servidor", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 