class SparkAnalysisAgent:
    """Optimized interactive LangGraph agent with enhanced terminal formatting."""

    def __init__(self, model: str = Config.DEFAULT_MODEL, verbose: bool = False):
        self.model = model
        self.verbose = verbose
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.tools = self._initialize_tools()
        self.graph = None
        self.state = None
        self._reset_state()
        self._create_graph()

    def _reset_state(self) -> None:
        self.state = {
            "messages": [],
            "analysis_results": [],
            "current_query": None,
            "tool_calls": [],
            "iterations": 0,
            "max_iterations": 10
        }

    def _print_service_setup_instructions(self, services: Dict[str, bool]) -> None:
        print("\n" + "="*60)
        print("SERVICE SETUP INSTRUCTIONS")
        print("="*60)
        for service, is_configured in services.items():
            status = "✓ Configured" if is_configured else "✗ Not Configured"
            print(f"{service}: {status}")
        print("="*60 + "\n")

    def _print_tools_table(self) -> None:
        print("\n" + "="*60)
        print("AVAILABLE TOOLS")
        print("="*60)
        for tool in self.tools:
            print(f"• {tool.name}: {tool.description}")
        print("="*60 + "\n")

    def _create_graph(self) -> None:
        workflow = StateGraph(AgentState)
        
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", self._tools_node)
        workflow.add_node("end", self._end_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": "end"
            }
        )
        workflow.add_edge("tools", "agent")
        workflow.add_edge("end", END)
        
        self.graph = workflow.compile()

    def _get_system_prompt(self) -> str:
        return """You are an expert Spark data analysis assistant. 
        You help users analyze Spark DataFrames, optimize queries, and provide insights.
        Use the available tools to help answer questions about Spark operations.
        Always provide clear explanations and recommendations."""

    def _should_continue(self, state: AgentState) -> str:
        messages = state.get("messages", [])
        if not messages:
            return "end"
        
        last_message = messages[-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        
        return "end"

    def _initialize_tools(self) -> list:
        tools = [
            Tool(
                name="analyze_dataframe",
                func=self._analyze_dataframe,
                description="Analyze a Spark DataFrame structure and statistics"
            ),
            Tool(
                name="optimize_query",
                func=self._optimize_query,
                description="Provide optimization suggestions for Spark queries"
            ),
            Tool(
                name="check_performance",
                func=self._check_performance,
                description="Check performance metrics of Spark operations"
            )
        ]
        return tools

    def _analyze_dataframe(self, query: str) -> str:
        return f"Analysis of DataFrame: {query}"

    def _optimize_query(self, query: str) -> str:
        return f"Optimization suggestions for: {query}"

    def _check_performance(self, query: str) -> str:
        return f"Performance check for: {query}"

    def _agent_node(self, state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        
        response = self.llm.invoke(
            messages,
            system=self._get_system_prompt()
        )
        
        state["messages"].append(response)
        state["iterations"] += 1
        
        if self.verbose:
            print(f"Agent iteration {state['iterations']}: {response.content[:100]}...")
        
        return state

    def _tools_node(self, state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        last_message = messages[-1]
        
        if hasattr(last_message, 'tool_calls'):
            for tool_call in last_message.tool_calls:
                tool_name = tool_call.get("name")
                tool_input = tool_call.get("args", {})
                
                tool = next((t for t in self.tools if t.name == tool_name), None)
                if tool:
                    result = tool.func(**tool_input)
                    state["tool_calls"].append({
                        "tool": tool_name,
                        "input": tool_input,
                        "output": result
                    })
        
        return state

    def _end_node(self, state: AgentState) -> AgentState:
        if self.verbose:
            print("Analysis complete")
        return state

    def run(self, query: str) -> str:
        self._reset_state()
        
        from langchain_core.messages import HumanMessage
        self.state["messages"].append(HumanMessage(content=query))
        self.state["current_query"] = query
        
        result = self.graph.invoke(self.state)
        
        if result.get("messages"):
            return result["messages"][-1].content
        
        return "No response generated"

    def interactive_session(self) -> None:
        print("\n" + "="*60)
        print("SPARK ANALYSIS AGENT - INTERACTIVE SESSION")
        print("="*60)
        self._print_tools_table()
        
        while True:
            try:
                user_input = input("\nEnter your query (or 'exit' to quit): ").strip()
                
                if user_input.lower() == 'exit':
                    print("Exiting session...")
                    break
                
                if not user_input:
                    continue
                
                response = self.run(user_input)
                print(f"\nAgent Response:\n{response}")
                
            except KeyboardInterrupt:
                print("\nSession interrupted by user")
                break
            except Exception as e:
                print(f"Error: {str(e)}")