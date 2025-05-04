"""
Modelos relacionados às sessões do CORTEX.
"""

import enum
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from cortex.core.db import Base


class SessionStatus(enum.Enum):
    """Status possíveis para uma sessão."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Session(Base):
    """
    Modelo de sessão do CORTEX.
    
    Uma sessão representa uma conversa ou contexto de trabalho no Cursor.
    """
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    objective = Column(Text, nullable=True)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relações
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="session", cascade="all, delete-orphan")
    session_metadata = relationship("SessionMetadata", back_populates="session", cascade="all, delete-orphan")
    states = relationship("State", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Session(id='{self.id}', name='{self.name}', status='{self.status}')>"
    
    def to_dict(self) -> Dict:
        """
        Converte a sessão para um dicionário.
        
        Returns:
            Dict: Representação da sessão como dicionário.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "objective": self.objective,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "message_count": len(self.messages) if self.messages else 0,
            "task_count": len(self.tasks) if self.tasks else 0,
        }
    
    def update(self, **kwargs) -> None:
        """
        Atualiza os atributos da sessão.
        
        Args:
            **kwargs: Atributos a serem atualizados.
        """
        # Verificar o status para atualizar completed_at
        if "status" in kwargs and kwargs["status"] == SessionStatus.COMPLETED:
            kwargs["completed_at"] = datetime.utcnow()
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class SessionMetadata(Base):
    """
    Metadados adicionais da sessão.
    
    Armazena informações como contexto detectado, tags, etc.
    """
    __tablename__ = "session_metadata"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(255), nullable=False)
    value_text = Column(Text, nullable=True)
    value_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relações
    session = relationship("Session", back_populates="session_metadata")
    
    def __repr__(self) -> str:
        return f"<SessionMetadata(session_id='{self.session_id}', key='{self.key}')>"
    
    def to_dict(self) -> Dict:
        """
        Converte os metadados para um dicionário.
        
        Returns:
            Dict: Representação dos metadados como dicionário.
        """
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "key": self.key,
            "value": self.value_json if self.value_json is not None else self.value_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 