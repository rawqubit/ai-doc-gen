import os
import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def doc_gen(file_path):
    """AI-powered documentation generator for code files."""
    with open(file_path, 'r') as f:
        code = f.read()

    console.print(f"[bold blue]Generating documentation for {file_path}...[/bold blue]")

    prompt = f"""
    Generate comprehensive documentation (docstrings, function comments, basic README sections) for the following code.
    Format your response in Markdown.

    Code:
    ```{os.path.splitext(file_path)[1][1:]}
    {code}
    ```
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert technical writer."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        doc_text = response.choices[0].message.content
        console.print(Markdown(doc_text))
    except Exception as e:
        console.print(f"[bold red]Error during documentation generation:[/bold red] {e}")

if __name__ == '__main__':
    doc_gen()
