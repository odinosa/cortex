#!/usr/bin/env python
"""
CORTEX CLI - Interface de linha de comando para gerenciamento do CORTEX.
"""

import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Criar aplicação Typer
app = typer.Typer(
    name="cortex",
    help="Memória de contexto para o Cursor via Model Context Protocol (MCP)",
    add_completion=False,
)

# Console rich para output formatado
console = Console()


@app.command("serve")
def serve(
    dev: bool = typer.Option(False, "--dev", help="Modo de desenvolvimento"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host para o servidor da API REST"),
    port: int = typer.Option(8000, "--port", help="Porta para o servidor da API REST"),
    daemon: bool = typer.Option(False, "--daemon", "-d", help="Executar em segundo plano"),
    log_level: str = typer.Option("INFO", "--log-level", help="Nível de logging"),
):
    """
    Inicia o servidor MCP e opcionalmente o servidor REST.
    """
    env = os.environ.copy()
    env["LOG_LEVEL"] = log_level
    
    if dev:
        env["CORTEX_ENV"] = "development"
        console.print("[yellow]Iniciando servidor em modo de desenvolvimento[/]")
    else:
        env["CORTEX_ENV"] = "production"
    
    # Default: servidor MCP
    cmd = [sys.executable, "-m", "cortex.mcp.server"]
    server_type = "MCP"
    
    # Modo de servidor REST (somente em produção)
    if host and port and not dev:
        console.print("[yellow]Iniciando servidor REST[/]")
        try:
            from cortex.api import server as api_server
            cmd = [sys.executable, "-m", "cortex.api.server", "--host", host, "--port", str(port)]
            server_type = "REST"
        except ImportError:
            console.print("[yellow]Módulo API não encontrado. Usando apenas servidor MCP.[/]")
    
    if daemon:
        console.print(f"[bold green]Iniciando servidor {server_type} em segundo plano...[/]")
        # Usar subprocess.Popen para execução em segundo plano
        subprocess.Popen(
            cmd, 
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        console.print("[bold green]Servidor iniciado com sucesso![/]")
    else:
        console.print(f"[bold green]Iniciando servidor {server_type}...[/]")
        console.print("[yellow]Pressione Ctrl+C para interromper[/]")
        
        try:
            # Execução em foreground
            process = subprocess.Popen(cmd, env=env)
            process.wait()
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrompendo servidor...[/]")
            process.send_signal(signal.SIGINT)
            process.wait()
            console.print("[bold green]Servidor encerrado com sucesso![/]")


@app.command("migrate")
def migrate(
    revision: str = typer.Argument("head", help="Revisão Alembic para migrar"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mostrar logs detalhados"),
):
    """
    Executa as migrações do banco de dados usando Alembic.
    """
    # Verificar se alembic está disponível
    try:
        import alembic
    except ImportError:
        console.print("[bold red]Erro: Alembic não está instalado.[/]")
        console.print("Instale com: pip install alembic")
        raise typer.Exit(1)
    
    console.print("[bold yellow]Executando migrações...[/]")
    
    cmd = ["alembic", "upgrade", revision]
    if verbose:
        cmd.insert(1, "--verbose")
    
    try:
        process = subprocess.run(cmd, check=True, capture_output=not verbose)
        console.print("[bold green]Migrações aplicadas com sucesso![/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Erro ao executar migrações: {e}[/]")
        if e.stdout:
            console.print(e.stdout.decode())
        if e.stderr:
            console.print(e.stderr.decode())
        raise typer.Exit(1)


@app.command("session")
def session(
    command: str = typer.Argument(..., help="Comando: list, show, export"),
    session_id: Optional[str] = typer.Argument(None, help="ID da sessão"),
    format: str = typer.Option("table", "--format", "-f", help="Formato de saída: table, json, md"),
    limit: int = typer.Option(10, "--limit", "-n", help="Número de itens a exibir"),
):
    """
    Gerencia sessões via CLI.
    """
    if command == "list":
        console.print("[bold]Listando sessões recentes...[/]")
        
        # Placeholder - implementar com API real
        table = Table(title="Sessões Recentes")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("Criada em", style="magenta")
        table.add_column("Status", style="yellow")
        
        # Dados de exemplo
        table.add_row("1", "Desenvolvimento inicial", "2024-06-04 09:30", "ativa")
        table.add_row("2", "Refatoração do módulo X", "2024-06-03 14:22", "concluída")
        
        console.print(table)
    
    elif command == "show" and session_id:
        console.print(f"[bold]Detalhes da sessão {session_id}[/]")
        
        # Placeholder - implementar com API real
        panel = Panel.fit(
            "[bold]Nome:[/] Desenvolvimento inicial\n"
            "[bold]Criada em:[/] 2024-06-04 09:30\n"
            "[bold]Status:[/] ativa\n"
            "[bold]Mensagens:[/] 42\n"
            "[bold]Tarefas:[/] 5 (3 concluídas)\n",
            title=f"Sessão #{session_id}"
        )
        console.print(panel)
    
    elif command == "export" and session_id:
        console.print(f"[bold]Exportando sessão {session_id}...[/]")
        
        # Placeholder - implementar com API real
        console.print("[green]Sessão exportada para session_1.json[/]")
    
    else:
        console.print("[bold red]Comando de sessão inválido![/]")
        console.print("Comandos disponíveis: list, show <id>, export <id>")


@app.command("task")
def task(
    command: str = typer.Argument(..., help="Comando: list, create, update, show"),
    task_id: Optional[str] = typer.Argument(None, help="ID da tarefa"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Título da tarefa"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Status: todo, doing, done"),
    session_id: Optional[str] = typer.Option(None, "--session", help="ID da sessão associada"),
):
    """
    Gerencia tarefas via CLI.
    """
    if command == "list":
        console.print("[bold]Listando tarefas...[/]")
        
        # Placeholder - implementar com API real
        table = Table(title="Tarefas")
        table.add_column("ID", style="cyan")
        table.add_column("Título", style="green")
        table.add_column("Status", style="magenta")
        table.add_column("Sessão", style="yellow")
        
        # Dados de exemplo
        table.add_row("1", "Implementar servidor MCP", "doing", "1")
        table.add_row("2", "Criar CLI básica", "todo", "1")
        
        console.print(table)
    
    elif command == "create" and title:
        console.print(f"[bold]Criando tarefa: {title}[/]")
        # Placeholder - implementar com API real
        console.print("[green]Tarefa criada com ID: 3[/]")
    
    elif command == "update" and task_id:
        console.print(f"[bold]Atualizando tarefa {task_id}[/]")
        # Placeholder - implementar com API real
        console.print(f"[green]Tarefa {task_id} atualizada com sucesso![/]")
    
    elif command == "show" and task_id:
        console.print(f"[bold]Detalhes da tarefa {task_id}[/]")
        # Placeholder - implementar com API real
        panel = Panel.fit(
            "[bold]Título:[/] Implementar servidor MCP\n"
            "[bold]Status:[/] doing\n"
            "[bold]Sessão:[/] 1\n"
            "[bold]Criada em:[/] 2024-06-04 10:15\n",
            title=f"Tarefa #{task_id}"
        )
        console.print(panel)
    
    else:
        console.print("[bold red]Comando de tarefa inválido![/]")
        console.print("Comandos disponíveis: list, create --title <título>, update <id>, show <id>")


@app.command("scan")
def scan(
    path: str = typer.Argument(".", help="Caminho para verificar"),
    pattern: str = typer.Option("*.py,*.js,*.ts,*.tsx,*.jsx", "--pattern", "-p", help="Padrão de arquivos"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Arquivo de saída"),
):
    """
    Escaneia arquivos em busca de TODOs e FIXMEs.
    """
    console.print(f"[bold]Escaneando {path} em busca de marcadores...[/]")
    
    # Placeholder - implementar com API real
    table = Table(title="Marcadores Encontrados")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Linha", style="magenta")
    table.add_column("Tipo", style="yellow")
    table.add_column("Descrição", style="green")
    
    # Dados de exemplo
    table.add_row("cortex/mcp/server.py", "42", "TODO", "Implementar autenticação")
    table.add_row("cortex/cli/main.py", "87", "FIXME", "Melhorar tratamento de erros")
    
    console.print(table)
    
    if output:
        console.print(f"[green]Resultados salvos em {output}[/]")


@app.command("version")
def version():
    """
    Exibe a versão atual do CORTEX.
    """
    # Placeholder - implementar com versão real
    console.print("[bold]CORTEX - Memória de contexto para o Cursor[/]")
    console.print("Versão: [bold cyan]0.1.0[/]")
    console.print("Python: [bold cyan]3.12+[/]")


if __name__ == "__main__":
    app() 