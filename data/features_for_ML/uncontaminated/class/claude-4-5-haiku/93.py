import anthropic
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.panel import Panel


class DevopsCopilotCli:

    def __init__(self) -> None:
        self.client = anthropic.Anthropic()
        self.console = Console()
        self.conversation_history = []

    def print_styled(self, content: str, style: str = ""):
        if style == "code":
            syntax = Syntax(content, "python", theme="monokai", line_numbers=True)
            self.console.print(syntax)
        elif style == "markdown":
            markdown = Markdown(content)
            self.console.print(markdown)
        elif style == "panel":
            panel = Panel(content, expand=False)
            self.console.print(panel)
        elif style == "error":
            self.console.print(f"[bold red]{content}[/bold red]")
        elif style == "success":
            self.console.print(f"[bold green]{content}[/bold green]")
        elif style == "warning":
            self.console.print(f"[bold yellow]{content}[/bold yellow]")
        elif style == "info":
            self.console.print(f"[bold blue]{content}[/bold blue]")
        else:
            self.console.print(content)

    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system="""You are an expert DevOps engineer and cloud infrastructure specialist. 
You provide practical, actionable advice on DevOps practices, cloud architecture, CI/CD pipelines, 
infrastructure as code, containerization, orchestration, monitoring, and deployment strategies.
You are knowledgeable about tools like Docker, Kubernetes, Terraform, Ansible, Jenkins, GitLab CI, 
GitHub Actions, AWS, Azure, GCP, and other DevOps technologies.
Provide clear, concise answers with practical examples when relevant.""",
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def run_interactive(self):
        self.print_styled("🚀 DevOps Copilot CLI", style="info")
        self.print_styled("Type 'exit' to quit, 'clear' to clear history", style="info")
        self.console.print()

        while True:
            try:
                user_input = self.console.input("[bold cyan]You:[/bold cyan] ")

                if user_input.lower() == "exit":
                    self.print_styled("Goodbye!", style="success")
                    break

                if user_input.lower() == "clear":
                    self.conversation_history = []
                    self.print_styled("Conversation history cleared.", style="success")
                    continue

                if not user_input.strip():
                    continue

                self.print_styled("Thinking...", style="info")
                response = self.chat(user_input)

                self.console.print()
                self.print_styled("DevOps Copilot:", style="success")
                self.print_styled(response, style="markdown")
                self.console.print()

            except KeyboardInterrupt:
                self.console.print()
                self.print_styled("Interrupted by user.", style="warning")
                break
            except anthropic.APIError as e:
                self.print_styled(f"API Error: {str(e)}", style="error")


def main():
    cli = DevopsCopilotCli()
    cli.run_interactive()


if __name__ == "__main__":
    main()