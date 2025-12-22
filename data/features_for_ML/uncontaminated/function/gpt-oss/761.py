from typing import List, Dict
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage

def _parse_old_conversations(old_conversations: List[Dict]) -> List[BaseMessage]:
    """
    Convert a list of legacy conversation dictionaries into a list of
    langchain BaseMessage objects.

    Each dictionary is expected to contain at least a `role` key and may
    contain `content` and `name` keys. The mapping is:

        role == "assistant" -> AIMessage
        role == "user"      -> HumanMessage
        role == "system"    -> SystemMessage

    Unknown roles are ignored.
    """
    messages: List[BaseMessage] = []

    for entry in old_conversations:
        role = entry.get("role")
        content = entry.get("content", "")
        name = entry.get("name")

        if role == "assistant":
            messages.append(AIMessage(content=content, name=name))
        elif role == "user":
            messages.append(HumanMessage(content=content, name=name))
        elif role == "system":
            messages.append(SystemMessage(content=content, name=name))
        else:
            # Skip unknown roles to avoid creating invalid messages
            continue

    return messages