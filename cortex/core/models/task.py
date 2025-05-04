"""
Modelos relacionados às tarefas do CORTEX.
"""

import enum
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                       String, Text, Boolean)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from cortex.core.db import Base


class TaskLevel(enum.Enum):
    """Níveis hierárquicos possíveis para tarefas."""
    PHASE = "phase"        # Fase: maior nível (ex: "Implementação Backend")
    STAGE = "stage"        # Etapa: agrupamento de tarefas (ex: "Autenticação")
    TASK = "task"          # Tarefa: unidade de trabalho (ex: "Implementar login")
    ACTIVITY = "activity"  # Atividade: subitem de tarefa (ex: "Validar senha")


class TaskStatus(enum.Enum):
    """Status possíveis para uma tarefa."""
    TODO = "todo"
    DOING = "doing"
    BLOCKED = "blocked"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


class Task(Base):
    """
    Modelo de tarefa do CORTEX.
    
    Tarefas são organizadas em uma hierarquia de 4 níveis:
    Fase → Etapa → Tarefa → Atividade
    """
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    level = Column(Enum(TaskLevel), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Integer, default=0, nullable=False)  # 0-5, maior = mais prioritário
    progress = Column(Float, default=0.0, nullable=False)  # 0.0 - 1.0 (0-100%)
    task_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    
    # Auto-propagação de estado para subtarefas
    propagate_status = Column(Boolean, default=True, nullable=False)
    
    # Relações
    session = relationship("Session", back_populates="tasks")
    parent = relationship("Task", back_populates="children", remote_side=[id])
    children = relationship("Task", back_populates="parent", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Task(id='{self.id}', title='{self.title}', status='{self.status}', level='{self.level}')>"
    
    def to_dict(self, include_children: bool = False) -> Dict:
        """
        Converte a tarefa para um dicionário.
        
        Args:
            include_children: Se deve incluir subtarefas recursivamente.
            
        Returns:
            Dict: Representação da tarefa como dicionário.
        """
        result = {
            "id": str(self.id),
            "session_id": str(self.session_id) if self.session_id else None,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "title": self.title,
            "description": self.description,
            "level": self.level.value,
            "status": self.status.value,
            "priority": self.priority,
            "progress": self.progress,
            "metadata": self.task_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "propagate_status": self.propagate_status,
        }
        
        # Adicionar subtarefas se solicitado
        if include_children and self.children:
            result["children"] = [child.to_dict(include_children=True) for child in self.children]
        else:
            result["children_count"] = len(self.children) if self.children else 0
        
        return result
    
    def get_all_children(self) -> List["Task"]:
        """
        Retorna recursivamente todas as subtarefas.
        
        Returns:
            List[Task]: Lista de todas as subtarefas em todos os níveis inferiores.
        """
        all_children = []
        
        for child in self.children:
            all_children.append(child)
            all_children.extend(child.get_all_children())
        
        return all_children
    
    def calculate_progress(self) -> float:
        """
        Calcula o progresso baseado nas subtarefas.
        
        Se não houver subtarefas, retorna o progresso direto.
        Se houver subtarefas, a média ponderada dos progressos.
        
        Returns:
            float: Progresso calculado (0.0 - 1.0)
        """
        if not self.children:
            return self.progress
        
        # Calcular média ponderada do progresso das subtarefas
        total_weight = len(self.children)
        if total_weight == 0:
            return self.progress
        
        sum_progress = sum(child.calculate_progress() for child in self.children)
        return sum_progress / total_weight
    
    def update_status_from_children(self) -> TaskStatus:
        """
        Atualiza o status com base nas subtarefas.
        
        Returns:
            TaskStatus: Novo status calculado
        """
        if not self.children or not self.propagate_status:
            return self.status
        
        # Contar status das subtarefas
        status_counts = {}
        for child in self.children:
            status = child.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total = len(self.children)
        
        # Regras de propagação
        if status_counts.get("todo", 0) == total:
            return TaskStatus.TODO
        
        if status_counts.get("done", 0) == total:
            return TaskStatus.DONE
        
        if status_counts.get("cancelled", 0) == total:
            return TaskStatus.CANCELLED
        
        if status_counts.get("blocked", 0) > 0:
            return TaskStatus.BLOCKED
        
        if status_counts.get("doing", 0) > 0:
            return TaskStatus.DOING
        
        if status_counts.get("review", 0) > 0:
            return TaskStatus.REVIEW
        
        # Caso misto: em andamento
        return TaskStatus.DOING
    
    def update_status(self, new_status: TaskStatus) -> None:
        """
        Atualiza o status da tarefa e possivelmente de suas subtarefas.
        
        Args:
            new_status: Novo status a ser definido
        """
        self.status = new_status
        
        # Atualizar timestamps
        if new_status == TaskStatus.DOING and not self.started_at:
            self.started_at = datetime.utcnow()
        
        if new_status == TaskStatus.DONE and not self.completed_at:
            self.completed_at = datetime.utcnow()
            self.progress = 1.0
        
        # Propagar para subtarefas se configurado
        if self.propagate_status and self.children:
            for child in self.children:
                child.update_status(new_status)
    
    def get_hierarchy_path(self) -> List[str]:
        """
        Retorna o caminho hierárquico completo da tarefa.
        
        Returns:
            List[str]: Lista de títulos de tarefas do topo até esta tarefa
        """
        if not self.parent:
            return [self.title]
        
        # Recursivamente obter o caminho até o topo
        return self.parent.get_hierarchy_path() + [self.title] 