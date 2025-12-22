from dataclasses import field, dataclass

class AIRAState:
    """State object for AIRA LangGraph workflow."""
    queries: list[GeneratedQuery] | None = None    
    web_research_results: list[str] | None = None
    citations: str | None = None
    running_summary: str | None = field(default=None) 
    final_report: str | None = field(default=None)