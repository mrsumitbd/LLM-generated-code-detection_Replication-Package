def _parse_old_conversations(old_conversations: List[Dict]) -> List[BaseMessage]:
    from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
    
    messages: List[BaseMessage] = []
    
    for conversation in old_conversations:
        if isinstance(conversation, dict):
            if "human" in conversation:
                messages.append(HumanMessage(content=conversation["human"]))
            if "ai" in conversation:
                messages.append(AIMessage(content=conversation["ai"]))
    
    return messages