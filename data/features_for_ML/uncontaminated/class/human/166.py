from typing import Optional
from omnicoreagent import OmniAgent, MemoryRouter, EventRouter, ToolRegistry, logger

class AirlineAgentCLI:
    """CLI interface for Airline Booking Agent. initialize() once and reuse the agent."""

    def __init__(self):
        self.agent: Optional[OmniAgent] = None
        self.memory_router: Optional[MemoryRouter] = None
        self.event_router: Optional[EventRouter] = None

    async def initialize(self):
        """Initialize the airline agent (instantiate routers and the OmniAgent)."""
        create_crm()  # bootstrap crm.json if missing
        print("🚀 Initializing Flight Booking Agent...")

        self.memory_router = MemoryRouter("in_memory")
        self.event_router = EventRouter("in_memory")

        self.agent = OmniAgent(
            name="flight_booking_agent",
            system_instruction=(
                "You are an expert Flight Booking Agent with access to flight search, booking, cancellation, "
                "and customer profile tools. You MUST use the `think` tool as your reasoning scratchpad for "
                "ANY multi-step or complex requests before taking action.\n\n"
                "## CRITICAL: Always use the think tool first for complex requests\n\n"
                "**When to use think tool:**\n"
                "- Multi-step operations (search + book, cancel + rebook)\n"
                "- Complex requests requiring policy verification\n"
                "- Requests needing customer profile analysis\n"
                "- Operations requiring rule compliance checks\n"
                "- Any request with multiple conditions or constraints\n\n"
                "**Think tool workflow:**\n"
                "1. **Analyze the request** - Break down what's needed\n"
                "2. **List applicable rules** - Identify policies, restrictions, requirements\n"
                "3. **Check information gaps** - What data do you need vs. what you have\n"
                "4. **Verify compliance** - Ensure planned actions follow all policies\n"
                "5. **Plan execution steps** - Outline the exact sequence of tool calls\n"
                "6. **Validate assumptions** - Check if your plan makes sense\n\n"
                "**Examples of think tool usage:**\n"
                "- User: 'Book cheapest flight for John on Sept 1'\n"
                "  → Think: Need user ID, search flights, compare prices, verify payment methods, check baggage rules\n"
                "- User: 'Cancel John's booking and rebook tomorrow'\n"
                "  → Think: Verify cancellation policy, check rebooking rules, ensure no double-booking, calculate fees\n"
                "- User: 'Book 3 tickets with 2 bags each'\n"
                "  → Think: Check membership tier for baggage allowance, verify payment method limits, calculate total costs\n\n"
                "**After thinking, execute your plan step-by-step using the appropriate tools.**\n"
                "Always include booking IDs in confirmations and keep responses professional but concise.\n\n"
                "**Remember:** The think tool is your strategic planning center. Use it to avoid mistakes and ensure compliance with all airline policies and customer requirements."
            ),
            model_config={
                "provider": "openai",
                "model": "gpt-4.1",
                "temperature": 0.2,
                "max_context_length": 50000,
            },
            local_tools=local_tools,
            agent_config={
                "max_steps": 12,
                "tool_call_timeout": 45,
                "request_limit": 500,
                "memory_config": {"mode": "token_budget", "value": 8000},
            },
            memory_store=self.memory_router,
            event_router=self.event_router,
            debug=True,
        )

    async def demo_flow(self):
        """Show sample interactions."""
        queries = [
            "Search flights from NYC to LON on 2025-09-01",
            "Book the cheapest flight on 2025-09-01 for user U1001",
            "Get profile for user U1001",
            "Cancel booking B2001 for user U1001",
            "Book 2 tickets to LON for U1002 with extra baggage allowance",
            "Cancel U1001's booking and rebook him on the next available flight",
        ]

        for q in queries:
            print(f"\nUser: {q}")
            result = await self.agent.run(q)
            print("Agent:", result)