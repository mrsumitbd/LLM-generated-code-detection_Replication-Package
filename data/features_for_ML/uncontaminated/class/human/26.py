from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import platform
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

class SparkAnalysisAgent:
    """Optimized interactive LangGraph agent with enhanced terminal formatting."""

    def __init__(self, model: str = Config.DEFAULT_MODEL, verbose: bool = False):
        self.model = model
        self.verbose = verbose
        self.formatter = TerminalFormatter()
        self._reset_state()

    def _reset_state(self) -> None:
        """Reset agent state."""
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.tools: List = []
        self.llm: Optional[ChatOllama] = None
        self.llm_with_tools = None
        self.graph = None
        self.initialized = False

    async def initialize(self) -> bool:
        """Initialize MCP client, tools, and LLM."""
        if self.initialized:
            return True

        try:
            await self._print_initialization_info()

            if not await self._check_and_report_services():
                return False

            await self._setup_mcp_client()
            await self._setup_llm()
            self._create_graph()

            self.initialized = True
            console_print("✅ Agent initialized successfully!")
            return True

        except Exception as e:
            console_print(f"❌ Initialization failed: {e}")
            return False

    async def _print_initialization_info(self) -> None:
        """Print initialization information."""
        console_print("🔄 Initializing Spark Analysis Agent...")
        console_print(f"🐍 Python {platform.python_version()} on {platform.system()}")
        console_print(f"🧠 Model: {self.model}")

    async def _check_and_report_services(self) -> bool:
        """Check services and report status."""
        if self.verbose:
            console_print("🔄 Checking required services...")

        services = await ServiceChecker.check_all_services()

        if self.verbose:
            for service, status in services.items():
                status_icon = "✅" if status else "❌"
                console_print(
                    f"  {status_icon} {service}: {'Running' if status else 'Not available'}"
                )

        if not all(services.values()):
            self._print_service_setup_instructions(services)
            return False

        return True

    def _print_service_setup_instructions(self, services: Dict[str, bool]) -> None:
        """Print setup instructions for failed services."""
        console_print("\n❌ Not all required services are running!")
        console_print("🔧 Setup instructions:")

        instructions = {
            "mcp_server": "Start MCP server: task start-mcp-bg",
            "spark_history": "Start Spark History server: task start-spark-bg",
            "ollama": "Install and start Ollama: brew install ollama && ollama pull qwen3:1.7b",
        }

        for service, running in services.items():
            if not running:
                console_print(f"  - {instructions[service]}")

    async def _setup_mcp_client(self) -> None:
        """Setup MCP client and load tools."""
        if self.verbose:
            console_print("🔄 Connecting to MCP server...")

        self.mcp_client = MultiServerMCPClient(
            {
                "spark": {
                    "url": f"{Config.MCP_SERVER_URL}mcp/",
                    "transport": "streamable_http",
                }
            }
        )

        if self.verbose:
            console_print("🔄 Loading MCP tools...")

        self.tools = await self.mcp_client.get_tools()
        self._print_tools_table()

    def _print_tools_table(self) -> None:
        """Print available tools in table format."""
        console_print(f"✅ Loaded {len(self.tools)} MCP tools:")
        console_print(f"\n{'Tool Name':<25} {'Description'}")
        console_print("─" * 75)

        for tool in self.tools:
            name = getattr(tool, "name", str(tool))
            desc = " ".join(
                getattr(tool, "description", "No description available").split()
            )
            desc = desc[:49] + "..." if len(desc) > 50 else desc
            console_print(f"{name:<25} {desc}")

        console_print("─" * 75)

    async def _setup_llm(self) -> None:
        """Setup Ollama LLM."""
        if self.verbose:
            console_print(f"🔄 Initializing Ollama with {self.model}...")

        self.llm = ChatOllama(
            model=self.model,
            base_url=Config.OLLAMA_URL,
            temperature=Config.TEMPERATURE,
            timeout=Config.TIMEOUT,
            num_predict=Config.MAX_TOKENS,
        )

        # Test connection
        await self.llm.ainvoke([HumanMessage(content="Hello")])
        if self.verbose:
            console_print("✅ Ollama connection successful")

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def _create_graph(self) -> None:
        """Create the LangGraph StateGraph."""
        workflow = StateGraph(AgentState)
        tool_node = ToolNode(self.tools)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", tool_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent", self._should_continue, {"continue": "tools", "end": END}
        )
        workflow.add_edge("tools", "agent")

        self.graph = workflow.compile()

    async def _call_model(self, state: AgentState) -> Dict[str, Any]:
        """Call the LLM with optimized system prompt."""
        messages = state["messages"]

        if not any("system" in str(msg).lower() for msg in messages):
            messages = [SystemMessage(content=self._get_system_prompt())] + messages

        response = await self.llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    def _get_system_prompt(self) -> str:
        """Get optimized system prompt."""
        return f"""You are a professional Spark performance analysis expert with MCP tools for Spark History Server data.

INSTRUCTIONS:
- Provide direct, professional analysis without <think> tags
- Use markdown headers (### 1., ### 2.) with proper spacing
- Format as key-value pairs where appropriate
- Use bullet points only for actual lists
- Be comprehensive but well-structured
- Focus on actionable insights

Available sample Spark application IDs:
{chr(10).join(f"- {app_id}" for app_id in Config.SAMPLE_APPS)}

Analysis approach:
1. Use MCP tools to fetch comprehensive application data
2. Identify performance metrics, bottlenecks, and resource utilization
3. Provide specific, actionable recommendations
4. Format with clear sections using markdown headers
5. Include specific metrics and measurements

Respond professionally with detailed technical analysis. /no_think"""

    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue with tool calls."""
        last_message = state["messages"][-1]
        return (
            "continue"
            if hasattr(last_message, "tool_calls") and last_message.tool_calls
            else "end"
        )

    async def query(self, user_input: str) -> str:
        """Process user query with enhanced terminal formatting."""
        if not self.initialized:
            return "❌ Agent not initialized. Call initialize() first."

        try:
            message = HumanMessage(content=user_input)
            result = await self.graph.ainvoke({"messages": [message]})
            response_content = result["messages"][-1].content
            return self.formatter.format_for_terminal(response_content)
        except Exception as e:
            return f"❌ Error processing query: {e}"

    async def close(self) -> None:
        """Clean up resources."""
        if self.mcp_client:
            try:
                await self.mcp_client.close()
            except Exception as e:
                # Ignore cleanup errors during shutdown
                del e