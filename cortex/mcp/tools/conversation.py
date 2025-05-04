"""
Ferramentas MCP relacionadas à gestão de conversas/mensagens.
"""

import uuid
from typing import Dict, List, Optional, Union

import structlog
from sqlalchemy import desc, func

from cortex.core.db import get_db
from cortex.core.models.message import Message, MessageRole
from cortex.core.models.session import Session, SessionStatus

logger = structlog.get_logger()


def record_message(
    session_id: Union[str, uuid.UUID],
    role: str,
    content: Optional[str] = None,
    name: Optional[str] = None,
    tools: Optional[List[Dict]] = None,
    tool_calls: Optional[List[Dict]] = None,
    function_call: Optional[Dict] = None,
    token_count: Optional[int] = None,
) -> Dict:
    """
    Registra uma nova mensagem em uma sessão.
    
    Args:
        session_id: ID da sessão
        role: Papel da mensagem (user, assistant, system, tool, function)
        content: Conteúdo da mensagem
        name: Nome opcional (para funções/ferramentas)
        tools: Ferramentas disponíveis (formato Cursor/OpenAI)
        tool_calls: Chamadas de ferramentas (formato Cursor/OpenAI)
        function_call: Chamada de função (formato Cursor/OpenAI)
        token_count: Contagem de tokens da mensagem
        
    Returns:
        Dict: Informações da mensagem registrada
    """
    try:
        # Converter string para UUID se necessário
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
        
        logger.info("Registrando mensagem", session_id=str(session_id), role=role)
        
        # Validar role
        try:
            message_role = MessageRole(role)
        except ValueError:
            return {
                "success": False,
                "error": f"Role '{role}' inválido",
                "message": f"Role deve ser um dos: {', '.join([r.value for r in MessageRole])}"
            }
        
        with get_db() as db:
            # Verificar se a sessão existe e está ativa
            session = db.query(Session).filter(Session.id == session_id).first()
            
            if not session:
                return {
                    "success": False,
                    "error": "Sessão não encontrada",
                    "message": f"Sessão com ID {session_id} não existe"
                }
            
            if session.status != SessionStatus.ACTIVE:
                return {
                    "success": False,
                    "error": "Sessão não está ativa",
                    "message": f"Sessão '{session.name}' está com status {session.status.value}"
                }
            
            # Obter próxima sequência
            sequence = db.query(func.coalesce(func.max(Message.sequence), -1) + 1).filter(
                Message.session_id == session_id
            ).scalar()
            
            # Criar mensagem
            message = Message(
                session_id=session_id,
                role=message_role,
                content=content,
                name=name,
                tools=tools,
                tool_calls=tool_calls,
                function_call=function_call,
                token_count=token_count,
                sequence=sequence
            )
            
            db.add(message)
            db.flush()  # Para obter o ID
            
            # Atualizar última atualização da sessão (handled by SQLAlchemy)
            
            # Obter dados da mensagem
            message_dict = message.to_dict()
            
            logger.info(
                "Mensagem registrada com sucesso",
                session_id=str(session_id),
                message_id=str(message.id),
                sequence=sequence
            )
            
            return {
                "success": True,
                "message": message_dict,
                "session_id": str(session_id)
            }
    
    except ValueError:
        # Erro ao converter UUID
        logger.error("UUID inválido", session_id=session_id)
        return {
            "success": False,
            "error": "UUID inválido",
            "message": f"O ID '{session_id}' não é um UUID válido"
        }
    
    except Exception as e:
        logger.error(
            "Erro ao registrar mensagem",
            error=str(e),
            session_id=str(session_id) if isinstance(session_id, uuid.UUID) else session_id
        )
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao registrar mensagem: {str(e)}"
        }


def get_context(
    session_id: Union[str, uuid.UUID],
    limit: int = 20,
    offset: int = 0,
    format: str = "cursor",
) -> Dict:
    """
    Recupera o contexto da conversa (mensagens anteriores).
    
    Args:
        session_id: ID da sessão
        limit: Número máximo de mensagens a retornar
        offset: Deslocamento para paginação (começando do mais recente)
        format: Formato de saída ('cursor', 'dict', 'raw')
        
    Returns:
        Dict: Mensagens da sessão formatadas
    """
    try:
        # Converter string para UUID se necessário
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
        
        logger.info("Obtendo contexto", session_id=str(session_id), limit=limit, offset=offset)
        
        with get_db() as db:
            # Verificar se a sessão existe
            session = db.query(Session).filter(Session.id == session_id).first()
            
            if not session:
                return {
                    "success": False,
                    "error": "Sessão não encontrada",
                    "message": f"Sessão com ID {session_id} não existe"
                }
            
            # Obter total de mensagens
            total_messages = db.query(func.count(Message.id)).filter(
                Message.session_id == session_id
            ).scalar()
            
            # Obter mensagens ordenadas por sequência (mais recentes primeiro)
            query = (
                db.query(Message)
                .filter(Message.session_id == session_id)
                .order_by(desc(Message.sequence))
                .limit(limit)
                .offset(offset)
            )
            
            messages = query.all()
            
            # Inverter para ordem cronológica (mais antigas primeiro)
            messages.reverse()
            
            # Formatar conforme solicitado
            if format == "cursor":
                # Formato para o Cursor MCP
                formatted_messages = [message.to_cursor_format() for message in messages]
            elif format == "dict":
                # Dicionário completo
                formatted_messages = [message.to_dict() for message in messages]
            else:
                # Raw - apenas IDs e conteúdo básico
                formatted_messages = [{
                    "id": str(message.id),
                    "role": message.role.value,
                    "content": message.content,
                    "sequence": message.sequence,
                } for message in messages]
            
            logger.info(
                "Contexto obtido com sucesso",
                session_id=str(session_id),
                count=len(messages),
                total=total_messages
            )
            
            return {
                "success": True,
                "messages": formatted_messages,
                "session_id": str(session_id),
                "session_name": session.name,
                "total_messages": total_messages,
                "has_more": (offset + len(messages)) < total_messages
            }
    
    except ValueError:
        # Erro ao converter UUID
        logger.error("UUID inválido", session_id=session_id)
        return {
            "success": False,
            "error": "UUID inválido",
            "message": f"O ID '{session_id}' não é um UUID válido"
        }
    
    except Exception as e:
        logger.error(
            "Erro ao obter contexto",
            error=str(e),
            session_id=str(session_id) if isinstance(session_id, uuid.UUID) else session_id
        )
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao obter contexto: {str(e)}"
        }


def summarize_conversation(
    session_id: Union[str, uuid.UUID],
    max_tokens: Optional[int] = 1000,
) -> Dict:
    """
    Gera um resumo da conversa atual.
    
    Esta é uma implementação simplificada que retorna um erro
    informando que a funcionalidade ainda será implementada com LLMs.
    
    Args:
        session_id: ID da sessão
        max_tokens: Limite de tokens para o resumo
        
    Returns:
        Dict: Resumo da conversa ou erro
    """
    try:
        # Converter string para UUID se necessário
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
        
        logger.info("Solicitando resumo da conversa", session_id=str(session_id))
        
        # Verificar se a sessão existe
        with get_db() as db:
            session = db.query(Session).filter(Session.id == session_id).first()
            
            if not session:
                return {
                    "success": False,
                    "error": "Sessão não encontrada",
                    "message": f"Sessão com ID {session_id} não existe"
                }
        
        # TODO: Implementar geração de resumo com LLM
        # Por enquanto, retornamos um erro informativo
        return {
            "success": False,
            "error": "not_implemented",
            "message": "A funcionalidade de resumo automático será implementada em versões futuras.",
            "session_id": str(session_id),
            "session_name": session.name
        }
    
    except ValueError:
        # Erro ao converter UUID
        logger.error("UUID inválido", session_id=session_id)
        return {
            "success": False,
            "error": "UUID inválido",
            "message": f"O ID '{session_id}' não é um UUID válido"
        }
    
    except Exception as e:
        logger.error(
            "Erro ao resumir conversa",
            error=str(e),
            session_id=str(session_id) if isinstance(session_id, uuid.UUID) else session_id
        )
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao resumir conversa: {str(e)}"
        } 