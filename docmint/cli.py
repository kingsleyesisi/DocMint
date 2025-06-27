import os
import sys
import json
import requests
import click
from requests.exceptions import ConnectionError, Timeout, RequestException
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

API_URL = os.getenv('DOCMINT_API_URL', 'http://localhost:8000')
INDEX_ENDPOINT = f"{API_URL}/"  # POST for prompt generation
FILES_ENDPOINT = f"{API_URL}/generate"

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    DocMint CLI Tool

    By default, scans current directory for files to generate README.md.
    Use subcommands `prompt` for custom prompts or `files` explicitly.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(files)

@cli.command()
@click.option('-p', '--prompt', help='Prompt or description for README generation', required=False)
def prompt(prompt):
    """Generate README.md based on a prompt"""
    try:
        if not prompt:
            prompt = Prompt.ask("Enter your README prompt")
        payload = {'message': prompt}
        console.print(f"[cyan]Sending prompt to DocMint API...[/cyan]")
        response = requests.post(INDEX_ENDPOINT, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get('answer') or data.get('result', {}).get('answer')
        if not answer:
            console.print("[red]No answer returned from API.[/red]")
            sys.exit(1)
        write_readme(answer)
    except ConnectionError:
        console.print("[bold red]Error:[/] Cannot connect to DocMint API. Check your network or API URL.")
        sys.exit(1)
    except Timeout:
        console.print("[bold red]Error:[/] Request to DocMint API timed out.")
        sys.exit(1)
    except RequestException as e:
        console.print(f"[bold red]Error:[/] {e}")
        sys.exit(1)

@cli.command()
@click.option('-t', '--type', 'project_type', help='Project type (e.g., Django API, React App)', required=False)
def files(project_type):
    """Generate README.md by uploading project files in current directory"""
    try:
        cwd = os.getcwd()
        if not project_type:
            project_type = Prompt.ask("Enter the project type (e.g., Django API, React App)")
        files_to_send = []
        for filename in os.listdir(cwd):
            if filename.startswith('.') or filename == 'README.md':
                continue
            filepath = os.path.join(cwd, filename)
            if os.path.isfile(filepath):
                files_to_send.append(('files', open(filepath, 'rb')))
        if not files_to_send:
            console.print(f"[red]No files found in directory {cwd}[/red]")
            sys.exit(1)
        console.print(f"[cyan]Uploading {len(files_to_send)} files to DocMint API...[/cyan]")
        data = {'projectType': project_type, 'contribution': 'true'}
        with Progress(SpinnerColumn(), TextColumn("[green]Uploading...[/green]")):
            response = requests.post(FILES_ENDPOINT, files=files_to_send, data=data, timeout=120)
        response.raise_for_status()
        result = response.json().get('result')
        answer = None
        if isinstance(result, dict):
            answer = result.get('answer') or result.get('result', {}).get('answer')
        elif isinstance(result, str):
            answer = result
        if not answer:
            console.print("[red]No answer returned from API.[/red]")
            sys.exit(1)
        write_readme(answer)
    except ConnectionError:
        console.print("[bold red]Error:[/] Cannot connect to DocMint API. Check your network or API URL.")
        sys.exit(1)
    except Timeout:
        console.print("[bold red]Error:[/] Request to DocMint API timed out.")
        sys.exit(1)
    except RequestException as e:
        console.print(f"[bold red]Error:[/] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/] {e}")
        sys.exit(1)


def write_readme(content):
    """Write content to README.md, prompting if file exists"""
    output_file = os.path.join(os.getcwd(), 'README.md')
    if os.path.exists(output_file):
        overwrite = Confirm.ask(f"README.md already exists. Overwrite?", default=False)
        if not overwrite:
            console.print("[yellow]Aborted: README.md not overwritten.[/yellow]")
            sys.exit(0)
    lines = content.splitlines(keepends=True)
    console.print(f"[green]Writing to {output_file}...[/green]")
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            console.print(line.rstrip(), end='\n')
            f.write(line)
    console.print("[bold green]README.md generated successfully![/bold green]")

if __name__ == '__main__':
    cli()
