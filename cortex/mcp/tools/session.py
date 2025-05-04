"""
Ferramentas MCP relacionadas à gestão de sessões.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

import structlog
from sqlalchemy import desc, func

from cortex.core.db import get_db
from cortex.core.models.session import Session, SessionMetadata, SessionStatus

logger = structlog.get_logger()


def start_session(
    name: str,
    objective: Optional[str] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> Dict:
    """
    Inicia uma nova sessão de trabalho.
    
    Args:
        name: Nome da sessão
        objective: Objetivo principal da sessão
        description: Descrição detalhada da sessão
        metadata: Metadados adicionais como contexto, tags, etc.
        
    Returns:
        Dict: Informações da sessão criada
    """
    try:
        logger.info("Iniciando nova sessão", name=name)
        
        # Criar sessão no banco de dados
        with get_db() as db:
            session = Session(
                name=name,
                objective=objective,
                description=description,
                status=SessionStatus.ACTIVE,
            )
            db.add(session)
            db.flush()  # Para obter o ID
            
            # Adicionar metadados, se fornecidos
            if metadata:
                for key, value in metadata.items():
                    # Verificar tipo para decidir entre JSON ou texto
                    if isinstance(value, (dict, list)):
                        meta = SessionMetadata(
                            session_id=session.id,
                            key=key,
                            value_json=value
                        )
                    else:
                        meta = SessionMetadata(
                            session_id=session.id,
                            key=key,
                            value_text=str(value)
                        )
                    db.add(meta)
            
            # Anotar timestamp para rastreamento
            created_meta = SessionMetadata(
                session_id=session.id,
                key="cortex_created_timestamp",
                value_text=datetime.utcnow().isoformat()
            )
            db.add(created_meta)
            
            # Obter dados da sessão
            session_dict = session.to_dict()
            
            logger.info("Sessão iniciada com sucesso", session_id=str(session.id))
            
            return {
                "success": True,
                "session": session_dict,
                "message": f"Sessão '{name}' iniciada com ID {session.id}"
            }
    
    except Exception as e:
        logger.error("Erro ao iniciar sessão", error=str(e), name=name)
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao iniciar sessão: {str(e)}"
        }


def end_session(
    session_id: Union[str, uuid.UUID],
    status: str = "completed",
    summary: Optional[str] = None,
) -> Dict:
    """
    Finaliza uma sessão existente.
    
    Args:
        session_id: ID da sessão a ser finalizada
        status: Status final (completed, archived)
        summary: Resumo opcional da sessão
        
    Returns:
        Dict: Resultado da operação
    """
    try:
        # Converter string para UUID se necessário
        if isinstance(session_id, str):
            session_id = uuid.UUID(session_id)
        
        logger.info("Finalizando sessão", session_id=str(session_id), status=status)
        
        # Mapear string de status para enum
        try:
            session_status = SessionStatus[status.upper()]
        except KeyError:
            return {
                "success": False,
                "error": f"Status '{status}' inválido",
                "message": f"Status deve ser um dos: {', '.join([s.name.lower() for s in SessionStatus])}"
            }
        
        with get_db() as db:
            # Buscar sessão
            session = db.query(Session).filter(Session.id == session_id).first()
            
            if not session:
                return {
                    "success": False,
                    "error": "Sessão não encontrada",
                    "message": f"Sessão com ID {session_id} não existe"
                }
            
            # Atualizar status e completed_at
            session.status = session_status
            session.completed_at = datetime.utcnow() if session_status == SessionStatus.COMPLETED else None
            
            # Adicionar resumo se fornecido
            if summary:
                meta = SessionMetadata(
                    session_id=session.id,
                    key="summary",
                    value_text=summary
                )
                db.add(meta)
            
            # Obter dados atualizados
            session_dict = session.to_dict()
            
            logger.info("Sessão finalizada com sucesso", session_id=str(session_id), status=status)
            
            return {
                "success": True,
                "session": session_dict,
                "message": f"Sessão '{session.name}' finalizada com status {status}"
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
        logger.error("Erro ao finalizar sessão", error=str(e), session_id=str(session_id))
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao finalizar sessão: {str(e)}"
        }


def list_sessions(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    order_by: str = "updated_at",
    order_dir: str = "desc",
) -> Dict:
    """
    Lista sessões existentes com paginação e filtros.
    
    Args:
        limit: Número máximo de sessões a retornar
        offset: Deslocamento para paginação
        status: Filtro de status (active, paused, completed, archived)
        order_by: Campo para ordenação (created_at, updated_at, name)
        order_dir: Direção da ordenação (asc, desc)
        
    Returns:
        Dict: Lista de sessões e contagem total
    """
    try:
        logger.info("Listando sessões", limit=limit, offset=offset, status=status)
        
        with get_db() as db:
            # Consulta base
            query = db.query(Session)
            count_query = db.query(func.count(Session.id))
            
            # Aplicar filtro de status se fornecido
            if status:
                try:
                    session_status = SessionStatus[status.upper()]
                    query = query.filter(Session.status == session_status)
                    count_query = count_query.filter(Session.status == session_status)
                except KeyError:
                    return {
                        "success": False,
                        "error": f"Status '{status}' inválido",
                        "message": f"Status deve ser um dos: {', '.join([s.name.lower() for s in SessionStatus])}"
                    }
            
            # Aplicar ordenação
            if order_by and hasattr(Session, order_by):
                order_column = getattr(Session, order_by)
                if order_dir.lower() == "desc":
                    query = query.order_by(desc(order_column))
                else:
                    query = query.order_by(order_column)
            else:
                # Ordenação padrão
                query = query.order_by(desc(Session.updated_at))
            
            # Contagem total
            total_count = count_query.scalar()
            
            # Aplicar paginação
            query = query.limit(limit).offset(offset)
            
            # Obter resultados
            sessions = query.all()
            
            # Converter para dicionários
            result = [session.to_dict() for session in sessions]
            
            logger.info("Sessões listadas com sucesso", count=len(result), total=total_count)
            
            return {
                "success": True,
                "sessions": result,
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + len(result)) < total_count
            }
    
    except Exception as e:
        logger.error("Erro ao listar sessões", error=str(e))
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao listar sessões: {str(e)}"
        } 