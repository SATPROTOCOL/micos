"""
absorb-osp — CLI Tool

Usage:
    absorb-osp run <github-url>    Run the 12-step absorption workflow
    absorb-osp list                List all absorbed projects
    absorb-osp status [name]       Show project or system status
    absorb-osp init                Initialize workspace directories
    absorb-osp validate <file>    Validate a report file
    absorb-osp scan <path>        Run privacy/security scan
    absorb-osp daemon             Start daemon mode (watch for URLs)
    absorb-osp mcp                Start MCP protocol server
"""

import os
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from . import __version__
from .lib.models import WorkflowResult
from .lib.scanner import scan_for_leaks, security_scan
from .lib.workflow import WorkflowEngine

app = typer.Typer(
    name="absorb-osp",
    help="Open source project absorption workflow — 12-step closed-loop flywheel",
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)


@app.callback()
def callback():
    """absorb-osp — Systematic OSP absorption for AI agents."""


@app.command()
def run(
    url: str = typer.Argument(..., help="GitHub repository URL"),
    output: str = typer.Option(
        None, "--output", "-o", help="Output directory for absorption artifacts"
    ),
):
    """Run the 12-step absorption workflow on a GitHub URL."""
    console.print(Panel(f"[bold]absorb-osp v{__version__}[/]\n{url}",
                        title="🎯 Absorption Workflow"))

    engine = WorkflowEngine(absorbed_dir=output)
    result = engine.run(url)

    if result.success:
        console.print(f"\n[green]✅ Workflow complete[/]")
        console.print(f"   Report: {result.report_path}")
    else:
        err_console.print(f"\n[red]❌ Workflow failed: {result.error}[/]")
        raise typer.Exit(code=1)


@app.command()
def list():
    """List all absorbed projects."""
    engine = WorkflowEngine()
    projects = engine.list_absorbed()

    if not projects:
        console.print("[yellow]No absorbed projects found.[/]")
        console.print("Run [bold]absorb-osp run <url>[/] to absorb your first project.")
        return

    table = Table(title="Absorbed Projects")
    table.add_column("Project", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Depth", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Date", style="white")

    for p in projects:
        table.add_row(p["name"], p["type"], p["depth"], p["status"], p["date"])

    console.print(table)


@app.command()
def status(
    name: str = typer.Argument(None, help="Project name to check"),
):
    """Show absorbed project status or system info."""
    if name:
        console.print(f"[bold]Project:[/] {name}")
        console.print("[yellow]Detailed status requires INDEX.md lookup.[/]")
    else:
        # System status
        engine = WorkflowEngine()
        projects = engine.list_absorbed()

        console.print(Panel(
            f"[bold]absorb-osp v{__version__}[/]\n\n"
            f"[cyan]Absorbed projects:[/] {len(projects)}\n"
            f"[cyan]Workspace:[/] {engine.absorbed_dir}\n"
            f"[cyan]Skills dir:[/] {engine.skills_dir}\n"
            f"[cyan]Projects dir:[/] {engine.projects_dir}",
            title="📊 System Status"
        ))


@app.command()
def init(
    directory: str = typer.Option(
        None, "--dir", "-d", help="Custom workspace directory"
    ),
):
    """Initialize workspace directories for absorption."""
    base = Path(directory) if directory else Path.home() / ".claude"
    dirs = [
        base / "absorbed",
        base / "skills",
        base / "instincts",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        console.print(f"  [green]✅[/] {d}")

    console.print(f"\n[bold]Workspace initialized at:[/] {base}")


@app.command()
def validate(
    file: str = typer.Argument(..., help="Report file path"),
):
    """Validate an analysis report file."""
    path = Path(file)
    if not path.exists():
        err_console.print(f"[red]❌ File not found: {file}[/]")
        raise typer.Exit(code=1)

    content = path.read_text(encoding="utf-8")
    if content.startswith("---"):
        # Basic frontmatter check
        parts = content.split("---", 2)
        if len(parts) >= 3:
            console.print(f"[green]✅ Valid frontmatter[/] in {file}")
            console.print(f"   Sections: {len(parts[2].split('## ')) - 1}")
        else:
            err_console.print(f"[red]❌ Invalid frontmatter in {file}[/]")
            raise typer.Exit(code=1)
    else:
        err_console.print(f"[red]❌ Missing frontmatter in {file}[/]")
        raise typer.Exit(code=1)


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to scan"),
    security: bool = typer.Option(False, "--security", "-s",
                                  help="Run full security audit"),
):
    """Run privacy leak scan or security audit."""
    scan_path = Path(path)
    if not scan_path.exists():
        err_console.print(f"[red]❌ Path not found: {path}[/]")
        raise typer.Exit(code=1)

    if security:
        console.print("[bold]🔒 Security Audit[/]")
        results = security_scan(str(scan_path))
        for check in results["checks"]:
            icon = {"pass": "✅", "warn": "⚠️", "fail": "❌", "skip": "⏭️"}.get(
                check["status"], "❓")
            console.print(f"  {icon} {check['name']}")
            if check["detail"]:
                console.print(f"     {check['detail']}")
        console.print(f"\nGate: {results['gate']}")
    else:
        console.print("[bold]🛡️ Privacy Leak Scan[/]")
        console.print(f"   Scanning: {scan_path}")
        findings = scan_for_leaks(str(scan_path))
        if findings:
            for f in findings[:10]:
                console.print(f"  [red]⚠️[/] {f['file']}:{f['line']} — {f['pattern']}")
        else:
            console.print("  [green]✅ No leaks detected[/]")
        console.print(f"\n   Files scanned, {len(findings)} finding(s)")


@app.command()
def daemon(
    port: int = typer.Option(8765, "--port", "-p", help="Webhook listen port"),
    watch: str = typer.Option(
        None, "--watch", "-w", help="Directory to watch for URL files"
    ),
):
    """Start daemon mode — webhook listener or directory watcher."""
    from .daemon import start_daemon
    start_daemon(port=port, watch_dir=watch)


@app.command()
def mcp():
    """Start MCP protocol server for agent integration."""
    from .mcp_server import start_mcp_server
    start_mcp_server()


def entry():
    """Entry point for the CLI."""
    app()
