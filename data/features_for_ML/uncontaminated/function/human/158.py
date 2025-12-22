import argparse
from chunkhound.core.config.indexing_config import IndexingConfig
from chunkhound.core.config.embedding_config import EmbeddingConfig
from chunkhound.core.config.database_config import DatabaseConfig
from chunkhound.core.config.mcp_config import MCPConfig
from chunkhound.core.config.llm_config import LLMConfig

def add_config_arguments(parser: argparse.ArgumentParser, configs: list[str]) -> None:
    """Add CLI arguments for specified config sections.

    Args:
        parser: Argument parser to add config arguments to
        configs: List of config section names to include
    """
    if "database" in configs:
        from chunkhound.core.config.database_config import DatabaseConfig

        DatabaseConfig.add_cli_arguments(parser)

    if "embedding" in configs:
        from chunkhound.core.config.embedding_config import EmbeddingConfig

        EmbeddingConfig.add_cli_arguments(parser)

    if "indexing" in configs:
        from chunkhound.core.config.indexing_config import IndexingConfig

        IndexingConfig.add_cli_arguments(parser)

    if "mcp" in configs:
        from chunkhound.core.config.mcp_config import MCPConfig

        MCPConfig.add_cli_arguments(parser)

    if "llm" in configs:
        from chunkhound.core.config.llm_config import LLMConfig

        LLMConfig.add_cli_arguments(parser)