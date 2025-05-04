"""
Pacote de ferramentas MCP do CORTEX.

Este pacote contém todas as ferramentas implementadas para o Model Context Protocol,
que podem ser chamadas pelo Cursor AI.
"""

# Importar principais ferramentas para facilitar acesso
try:
    from cortex.mcp.tools.session import start_session, end_session, list_sessions
    from cortex.mcp.tools.conversation import record_message, get_context, summarize_conversation
    from cortex.mcp.tools.markers import scan_markers
    from cortex.mcp.tools.tasks import create_task, update_task_status, list_tasks
    from cortex.mcp.tools.context import detect_context, apply_context_rules
    from cortex.mcp.tools.state import save_state, load_state
except ImportError:
    # Durante o desenvolvimento, alguns módulos podem não existir ainda
    pass

__all__ = [
    "start_session", "end_session", "list_sessions",
    "record_message", "get_context", "summarize_conversation",
    "scan_markers",
    "create_task", "update_task_status", "list_tasks",
    "detect_context", "apply_context_rules",
    "save_state", "load_state",
] 