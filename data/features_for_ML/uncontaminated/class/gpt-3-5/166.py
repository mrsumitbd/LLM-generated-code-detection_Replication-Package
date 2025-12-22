class AirlineAgentCLI:
    """CLI interface for Airline Booking Agent. initialize() once and reuse the agent."""

    def __init__(self):
        self.agent_name = ""
        self.agent_id = ""
        self.agent_email = ""

    def set_agent_details(self, name, agent_id, email):
        self.agent_name = name
        self.agent_id = agent_id
        self.agent_email = email

    def display_agent_details(self):
        print("Agent Name:", self.agent_name)
        print("Agent ID:", self.agent_id)
        print("Agent Email:", self.agent_email)

# Example usage:
agent_cli = AirlineAgentCLI()
agent_cli.set_agent_details("John Doe", "A123", "john.doe@example.com")
agent_cli.display_agent_details()