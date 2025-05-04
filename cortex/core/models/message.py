"""
Modelos relacionados às mensagens do CORTEX.
"""

import enum
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from cortex.core.db import Base


class MessageRole(enum.Enum):
    """Papéis possíveis para uma mensagem."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"


class Message(Base):
    """
    Modelo de mensagem do CORTEX.
    
    Representa uma mensagem trocada entre o usuário e o assistente.
    """
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=True)
    name = Column(String(255), nullable=True)
    tools = Column(JSONB, nullable=True)
    tool_calls = Column(JSONB, nullable=True)
    function_call = Column(JSONB, nullable=True)
    token_count = Column(Integer, nullable=True)
    sequence = Column(Integer, nullable=False)  # Ordem na sessão
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relações
    session = relationship("Session", back_populates="messages")
    
    def __repr__(self) -> str:
        return f"<Message(id='{self.id}', role='{self.role}', seq={self.sequence})>"
    
    def to_dict(self) -> Dict:
        """
        Converte a mensagem para um dicionário.
        
        Returns:
            Dict: Representação da mensagem como dicionário.
        """
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "role": self.role.value,
            "content": self.content,
            "name": self.name,
            "tools": self.tools,
            "tool_calls": self.tool_calls,
            "function_call": self.function_call,
            "token_count": self.token_count,
            "sequence": self.sequence,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def to_cursor_format(self) -> Dict:
        """
        Converte a mensagem para o formato esperado pelo Cursor MCP.
        
        Returns:
            Dict: Mensagem no formato do Cursor.
        """
        # Formato base
        result = {"role": self.role.value}
        
        # Adicionar campos conforme existência
        if self.content:
            result["content"] = self.content
        
        if self.name:
            result["name"] = self.name
        
        if self.tools:
            result["tools"] = self.tools
        
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        
        if self.function_call:
            result["function_call"] = self.function_call
        
        return result
    
    @classmethod
    def from_cursor_format(cls, session_id: uuid.UUID, message: Dict, sequence: int) -> "Message":
        """
        Cria uma mensagem a partir do formato usado pelo Cursor.
        
        Args:
            session_id: ID da sessão à qual a mensagem pertence.
            message: Dicionário no formato Cursor.
            sequence: Ordem da mensagem na sessão.
            
        Returns:
            Message: Nova instância de mensagem.
        """
        role = MessageRole(message["role"])
        
        return cls(
            session_id=session_id,
            role=role,
            content=message.get("content"),
            name=message.get("name"),
            tools=message.get("tools"),
            tool_calls=message.get("tool_calls"),
            function_call=message.get("function_call"),
            sequence=sequence,
        ) 