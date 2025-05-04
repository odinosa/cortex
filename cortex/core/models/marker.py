"""
Modelos relacionados aos marcadores do CORTEX.
"""

import enum
import uuid
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from cortex.core.db import Base


class MarkerType(enum.Enum):
    """Tipos possíveis de marcadores."""
    TODO = "TODO"
    FIXME = "FIXME"
    HACK = "HACK"
    BUG = "BUG"
    NOTE = "NOTE"
    REVIEW = "REVIEW"


class MarkerStatus(enum.Enum):
    """Status possíveis para um marcador."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    WONT_FIX = "wont_fix"


class Marker(Base):
    """
    Modelo de marcador do CORTEX.
    
    Um marcador representa um ponto de interesse no código, como TODOs ou FIXMEs.
    """
    __tablename__ = "markers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    type = Column(Enum(MarkerType), nullable=False)
    status = Column(Enum(MarkerStatus), default=MarkerStatus.OPEN, nullable=False)
    file_path = Column(String(1024), nullable=False)
    line_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    full_line = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    marker_metadata = Column(JSONB, nullable=True)
    
    # Relações
    session = relationship("Session")
    task = relationship("Task")
    
    def __repr__(self) -> str:
        return f"<Marker(id='{self.id}', type='{self.type}', file='{self.file_path}', line={self.line_number})>"
    
    def to_dict(self) -> Dict:
        """
        Converte o marcador para um dicionário.
        
        Returns:
            Dict: Representação do marcador como dicionário.
        """
        return {
            "id": str(self.id),
            "session_id": str(self.session_id) if self.session_id else None,
            "task_id": str(self.task_id) if self.task_id else None,
            "type": self.type.value,
            "status": self.status.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "content": self.content,
            "full_line": self.full_line,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.marker_metadata,
        }
    
    def resolve(self) -> None:
        """
        Marca o marcador como resolvido.
        """
        self.status = MarkerStatus.RESOLVED
        self.resolved_at = datetime.utcnow() 