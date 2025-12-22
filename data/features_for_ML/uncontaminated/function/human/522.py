from agentstack_sdk.platform import (
    ModelCapability,
    ModelProvider,
    ModelProviderType,
    SystemConfiguration,
)
from rich.table import Column
from agentstack_cli.async_typer import AsyncTyper, console, create_table

def _list_providers(providers: list[ModelProvider]):
    with create_table(Column("Type"), Column("Name"), Column("Base URL", ratio=1)) as provider_table:
        for provider in providers:
            provider_table.add_row(provider.type, provider.name, str(provider.base_url))
    console.print(provider_table)