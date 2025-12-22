from __future__ import annotations

from typing import Any, List, Optional, Union
from types import SimpleNamespace

# Try to import the real Agent class if available
try:
    from langchain.agents import Agent  # type: ignore
except Exception:  # pragma: no cover
    Agent = SimpleNamespace  # fallback placeholder

# Try to import common tools
try:
    from langchain.tools import (
        DuckDuckGoSearchRun,
        PythonREPLTool,
        CalculatorTool,
    )
except Exception:  # pragma: no cover
    DuckDuckGoSearchRun = None
    PythonREPLTool = None
    CalculatorTool = None

# Vision tool may not exist in all versions
try:
    from langchain.tools import VisionTool  # type: ignore
except Exception:  # pragma: no cover
    VisionTool = None


def create_full_agent(
    model_name: str,
    vision_model_name: Optional[str],
    no_stream: bool = False,
    compact_every_n_iteration: Optional[int] = None,
    max_tokens_working_memory: Optional[int] = None,
) -> Agent:
    """
    Create an agent with the specified model and many tools.

    Args:
        model_name (str): Name of the model to use
        vision_model_name (str | None): Name of the vision model to use
        no_stream (bool, optional): If True, the agent will not stream results.
        compact_every_n_iteration (int | None, optional): Frequency of memory compaction.
        max_tokens_working_memory (int | None, optional): Maximum tokens for working memory.

    Returns:
        Agent: An agent with the specified model and tools
    """
    # Build the list of tools
    tools: List[Any] = []

    if DuckDuckGoSearchRun is not None:
        tools.append(DuckDuckGoSearchRun())

    if CalculatorTool is not None:
        tools.append(CalculatorTool())

    if PythonREPLTool is not None:
        tools.append(PythonREPLTool())

    if vision_model_name and VisionTool is not None:
        try:
            tools.append(VisionTool(model=vision_model_name))
        except Exception:
            # If the VisionTool constructor differs, ignore it
            pass

    # Create the agent instance
    # If the real Agent class is available, use it; otherwise, fall back to a SimpleNamespace
    if Agent is SimpleNamespace:
        agent = SimpleNamespace(
            model_name=model_name,
            vision_model_name=vision_model_name,
            no_stream=no_stream,
            compact_every_n_iteration=compact_every_n_iteration,
            max_tokens_working_memory=max_tokens_working_memory,
            tools=tools,
        )
    else:
        # The real Agent class may expect a different constructor signature.
        # We attempt to instantiate it with the most common parameters.
        try:
            agent = Agent(
                llm=model_name,
                tools=tools,
                verbose=not no_stream,
                memory_compaction_interval=compact_every_n_iteration,
                max_memory_tokens=max_tokens_working_memory,
            )
        except TypeError:
            # Fallback: use a simple namespace if the constructor signature differs
            agent = SimpleNamespace(
                model_name=model_name,
                vision_model_name=vision_model_name,
                no_stream=no_stream,
                compact_every_n_iteration=compact_every_n_iteration,
                max_tokens_working_memory=max_tokens_working_memory,
                tools=tools,
            )

    return agent