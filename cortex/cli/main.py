#!/usr/bin/env python3
"""
CORTEX CLI - Interface de linha de comando para o sistema CORTEX.
"""
import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """CORTEX - Assistente de Contexto para Cursor.
    
    Esta ferramenta gerencia sessões, tarefas e contexto para desenvolvimento com o Cursor.
    """
    pass


@cli.command()
def init():
    """Inicializa o banco de dados SQLite e estruturas necessárias."""
    from cortex.storage.database import init_db
    
    console.print(Panel("Inicializando banco de dados CORTEX", style="blue"))
    try:
        init_db()
        console.print("[green]Banco de dados inicializado com sucesso![/green]")
    except Exception as e:
        console.print(f"[red]Erro ao inicializar banco de dados: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--dev", is_flag=True, help="Inicia em modo de desenvolvimento")
@click.option("--port", default=None, type=int, help="Porta para servidor HTTP (opcional)")
def serve(dev, port):
    """Inicia o servidor MCP do CORTEX."""
    from cortex.mcp.server import start_server
    
    console.print(Panel(f"Iniciando servidor MCP CORTEX", style="blue"))
    try:
        start_server(dev_mode=dev, http_port=port)
    except KeyboardInterrupt:
        console.print("[yellow]Servidor finalizado pelo usuário[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro ao iniciar servidor: {str(e)}[/red]")
        sys.exit(1)


@cli.command(name="setup-cursor")
@click.option("--force", is_flag=True, help="Sobrescreve configuração existente")
def setup_cursor(force):
    """Configura o Cursor para usar o CORTEX."""
    from cortex.core.config import setup_cursor_integration
    
    console.print(Panel("Configurando integração com o Cursor", style="blue"))
    try:
        result = setup_cursor_integration(force=force)
        if result:
            console.print("[green]Integração com Cursor configurada com sucesso![/green]")
            console.print("Reinicie o Cursor para aplicar as alterações.")
        else:
            console.print("[yellow]Configuração não alterada.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro ao configurar Cursor: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("project_name")
@click.option("--desc", help="Descrição do projeto")
@click.option("--template", default="default", help="Template a ser usado")
@click.option("--jira-key", help="Chave do projeto no Jira (opcional)")
def create_project(project_name, desc, template, jira_key):
    """Cria um novo projeto no CORTEX."""
    from cortex.core.project import create_project as create_project_func
    
    console.print(Panel(f"Criando projeto: {project_name}", style="blue"))
    try:
        project_id = create_project_func(
            name=project_name,
            description=desc,
            template=template,
            jira_project_key=jira_key
        )
        console.print(f"[green]Projeto criado com sucesso! ID: {project_id}[/green]")
    except Exception as e:
        console.print(f"[red]Erro ao criar projeto: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def list_projects():
    """Lista todos os projetos no CORTEX."""
    from cortex.core.project import list_projects as list_projects_func
    
    console.print(Panel("Projetos CORTEX", style="blue"))
    try:
        projects = list_projects_func()
        
        if not projects:
            console.print("[yellow]Nenhum projeto encontrado.[/yellow]")
            return
        
        table = Table("ID", "Nome", "Workspace", "Ativo", "Criado em")
        for project in projects:
            table.add_row(
                str(project["id"]),
                project["name"],
                project["workspace_path"] or "-",
                "✓" if project["active"] else "✗",
                project["created_at"]
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro ao listar projetos: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--verbose", is_flag=True, help="Mostra informações detalhadas")
def status(verbose):
    """Mostra o status atual do sistema CORTEX."""
    from cortex.core.session import get_active_session
    from cortex.core.project import get_current_project
    
    console.print(Panel("Status do CORTEX", style="blue"))
    try:
        # Verifica servidor
        server_running = False
        try:
            # TODO: Implementar verificação de servidor
            server_running = True
        except:
            pass
        
        # Projeto atual
        current_project = get_current_project()
        
        # Sessão ativa
        active_session = get_active_session() if current_project else None
        
        # Exibe informações
        console.print(f"[bold]Servidor MCP:[/bold] {'Ativo' if server_running else 'Inativo'}")
        
        if current_project:
            console.print(f"[bold]Projeto Atual:[/bold] {current_project['name']} (ID: {current_project['id']})")
        else:
            console.print("[bold]Projeto Atual:[/bold] Nenhum")
        
        if active_session:
            console.print(f"[bold]Sessão Ativa:[/bold] {active_session['title']} (ID: {active_session['id']})")
            console.print(f"[bold]Iniciada em:[/bold] {active_session['start_time']}")
        else:
            console.print("[bold]Sessão Ativa:[/bold] Nenhuma")
        
        if verbose:
            # TODO: Adicionar mais informações detalhadas
            pass
            
    except Exception as e:
        console.print(f"[red]Erro ao obter status: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli() 