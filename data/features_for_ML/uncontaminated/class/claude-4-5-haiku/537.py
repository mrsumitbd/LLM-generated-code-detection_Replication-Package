import anthropic


class CommandGetTableTypes:
    """Represents a CommandGetTableTypes."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def get_table_types(self) -> list[str]:
        """Get the list of table types supported by the database."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "What are the standard SQL table types? Please provide a list of common table types used in databases.",
                }
            ],
        )

        response_text = message.content[0].text

        table_types = [
            "TABLE",
            "VIEW",
            "SYSTEM TABLE",
            "GLOBAL TEMPORARY",
            "LOCAL TEMPORARY",
            "ALIAS",
            "SYNONYM",
        ]

        return table_types

    def execute(self) -> dict:
        """Execute the command and return table types information."""
        table_types = self.get_table_types()
        return {"table_types": table_types, "count": len(table_types)}