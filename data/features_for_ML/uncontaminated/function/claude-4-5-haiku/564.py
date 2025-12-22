import anthropic
import json


def instantiate_network(config):
    """
    Instantiate a network of Claude agents that can communicate with each other.
    
    Args:
        config: A dictionary containing network configuration with the following structure:
            {
                "agents": [
                    {
                        "name": "agent_name",
                        "role": "agent_role",
                        "model": "claude-3-5-sonnet-20241022"
                    },
                    ...
                ],
                "connections": [
                    {
                        "from": "agent1_name",
                        "to": "agent2_name"
                    },
                    ...
                ]
            }
    
    Returns:
        A dictionary representing the instantiated network with agents and their connections.
    """
    client = anthropic.Anthropic()
    
    network = {
        "agents": {},
        "connections": {},
        "client": client
    }
    
    # Create agents from config
    if "agents" in config:
        for agent_config in config["agents"]:
            agent_name = agent_config.get("name")
            agent = {
                "name": agent_name,
                "role": agent_config.get("role", ""),
                "model": agent_config.get("model", "claude-3-5-sonnet-20241022"),
                "messages": []
            }
            network["agents"][agent_name] = agent
    
    # Set up connections between agents
    if "connections" in config:
        for connection in config["connections"]:
            from_agent = connection.get("from")
            to_agent = connection.get("to")
            
            if from_agent not in network["connections"]:
                network["connections"][from_agent] = []
            
            network["connections"][from_agent].append(to_agent)
    
    # Add helper methods to the network
    def send_message(from_agent, to_agent, message):
        """Send a message from one agent to another."""
        if from_agent in network["agents"] and to_agent in network["agents"]:
            network["agents"][to_agent]["messages"].append({
                "from": from_agent,
                "content": message
            })
            return True
        return False
    
    def get_agent_response(agent_name, user_message):
        """Get a response from an agent using Claude."""
        if agent_name not in network["agents"]:
            return None
        
        agent = network["agents"][agent_name]
        
        # Build the system prompt based on agent role
        system_prompt = f"You are {agent_name}, a {agent['role']}. "
        system_prompt += "You are part of a network of agents that can communicate with each other. "
        system_prompt += "Respond helpfully and concisely."
        
        # Prepare messages for the API
        messages = [
            {"role": "user", "content": user_message}
        ]
        
        # Add any pending messages from other agents
        for msg in agent["messages"]:
            messages.insert(0, {
                "role": "user",
                "content": f"Message from {msg['from']}: {msg['content']}"
            })
        
        # Clear pending messages after processing
        agent["messages"] = []
        
        # Call Claude API
        response = client.messages.create(
            model=agent["model"],
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        
        return response.content[0].text
    
    def broadcast_message(from_agent, message):
        """Broadcast a message from one agent to all connected agents."""
        if from_agent in network["connections"]:
            for to_agent in network["connections"][from_agent]:
                send_message(from_agent, to_agent, message)
            return True
        return False
    
    # Attach methods to network
    network["send_message"] = send_message
    network["get_agent_response"] = get_agent_response
    network["broadcast_message"] = broadcast_message
    
    return network