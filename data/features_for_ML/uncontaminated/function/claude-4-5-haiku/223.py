import anthropic
import json


def create_fast_allgather_context(rank, node, num_ranks, num_nodes, max_buffer_size: int = 2 * 32 * 1024 * 1024):
    """
    Create a fast allgather context using Claude API to generate distributed communication patterns.
    
    Args:
        rank: The rank of the current process
        node: The node identifier
        num_ranks: Total number of ranks
        num_nodes: Total number of nodes
        max_buffer_size: Maximum buffer size for communication
    
    Returns:
        A dictionary containing the allgather context configuration
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Generate a fast allgather communication pattern for a distributed system with the following parameters:
- Current rank: {rank}
- Current node: {node}
- Total ranks: {num_ranks}
- Total nodes: {num_nodes}
- Max buffer size: {max_buffer_size} bytes

Please provide a JSON response with the following structure:
{{
    "rank": {rank},
    "node": {node},
    "communication_pattern": "description of the pattern",
    "phases": [
        {{
            "phase_id": 0,
            "send_to": [list of ranks to send to],
            "recv_from": [list of ranks to receive from],
            "buffer_size": size in bytes
        }}
    ],
    "optimization_strategy": "description of optimization",
    "estimated_latency_ms": estimated latency in milliseconds
}}

Ensure the pattern is efficient for the given number of ranks and nodes."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            context = json.loads(json_str)
        else:
            context = {
                "rank": rank,
                "node": node,
                "communication_pattern": "ring_allgather",
                "phases": [
                    {
                        "phase_id": 0,
                        "send_to": [(rank + 1) % num_ranks],
                        "recv_from": [(rank - 1) % num_ranks],
                        "buffer_size": max_buffer_size // num_ranks
                    }
                ],
                "optimization_strategy": "ring_based_communication",
                "estimated_latency_ms": 100
            }
    except json.JSONDecodeError:
        context = {
            "rank": rank,
            "node": node,
            "communication_pattern": "ring_allgather",
            "phases": [
                {
                    "phase_id": 0,
                    "send_to": [(rank + 1) % num_ranks],
                    "recv_from": [(rank - 1) % num_ranks],
                    "buffer_size": max_buffer_size // num_ranks
                }
            ],
            "optimization_strategy": "ring_based_communication",
            "estimated_latency_ms": 100
        }
    
    context["max_buffer_size"] = max_buffer_size
    context["num_ranks"] = num_ranks
    context["num_nodes"] = num_nodes
    
    return context