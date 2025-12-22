from typing import Dict, List, Optional, Type
from derisk.core.interface.message import (
    BaseMessage,
    ConversationIdentifier,
    MessageIdentifier,
    MessageStorageItem,
    StorageConversation,
    _conversation_to_dict,
    _messages_from_dict,
)

def _parse_old_conversations(old_conversations: List[Dict]) -> List[BaseMessage]:
    old_messages_dict = []
    for old_conversation in old_conversations:
        messages = (
            old_conversation["messages"] if "messages" in old_conversation else []
        )
        for message in messages:
            if "data" in message:
                message_data = message["data"]
                additional_kwargs = message_data.get("additional_kwargs", {})
                additional_kwargs["param_value"] = old_conversation.get("param_value")
                additional_kwargs["param_type"] = old_conversation.get("param_type")
                additional_kwargs["model_name"] = old_conversation.get("model_name")
                message_data["additional_kwargs"] = additional_kwargs

        old_messages_dict.extend(messages)

    old_messages: List[BaseMessage] = _messages_from_dict(old_messages_dict)
    return old_messages