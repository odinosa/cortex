"""
Modelos relacionados ao armazenamento de estados do CORTEX.
"""

import uuid
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from cortex.core.db import Base


class State(Base):
    """
    Modelo de estado do CORTEX.
    
    Um estado representa um conjunto de snapshots de um contexto de trabalho.
    """
    __tablename__ = "states"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relações
    session = relationship("Session", back_populates="states")
    snapshots = relationship("StateSnapshot", back_populates="state", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<State(id='{self.id}', name='{self.name}')>"
    
    def to_dict(self) -> Dict:
        """
        Converte o estado para um dicionário.
        
        Returns:
            Dict: Representação do estado como dicionário.
        """
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "snapshot_count": len(self.snapshots) if self.snapshots else 0,
        }


class StateSnapshot(Base):
    """
    Modelo de snapshot de estado.
    
    Um snapshot representa uma captura específica de um aspecto do estado.
    Por exemplo, o conteúdo de um arquivo, uma variável, ou outro estado do sistema.
    """
    __tablename__ = "state_snapshots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_id = Column(UUID(as_uuid=True), ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(255), nullable=False)  # Tipo ou categoria do snapshot
    path = Column(String(1024), nullable=True)  # Caminho do arquivo ou identificador
    content_json = Column(JSONB, nullable=True)  # Conteúdo em formato JSON
    content_text = Column(Text, nullable=True)  # Conteúdo em formato texto
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relações
    state = relationship("State", back_populates="snapshots")
    
    def __repr__(self) -> str:
        return f"<StateSnapshot(id='{self.id}', key='{self.key}', path='{self.path}')>"
    
    def to_dict(self) -> Dict:
        """
        Converte o snapshot para um dicionário.
        
        Returns:
            Dict: Representação do snapshot como dicionário.
        """
        return {
            "id": str(self.id),
            "state_id": str(self.state_id),
            "key": self.key,
            "path": self.path,
            "content": self.content_json if self.content_json is not None else self.content_text,
            "content_type": "json" if self.content_json is not None else "text",
            "created_at": self.created_at.isoformat() if self.created_at else None,
        } 