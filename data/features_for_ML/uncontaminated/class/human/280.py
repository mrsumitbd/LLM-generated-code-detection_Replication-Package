from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agentops.sdk.decorators import operation, trace
from langchain_core.messages import AIMessage

class DebateAgent:
    """Represents a debate participant"""
    agent_id: str
    name: str
    model_name: str
    temperature: float
    memory_lst: List[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.memory_lst is None:
            self.memory_lst = []
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            request_timeout=60,
            max_retries=2
        )

    def set_meta_prompt(self, meta_prompt: str):
        """Set meta prompt"""
        self.memory_lst.append({"role": "system", "content": meta_prompt})

    def add_event(self, event: str):
        """Add new event to memory"""
        self.memory_lst.append({"role": "user", "content": event})

    def add_memory(self, memory: str):
        """Add generated response to memory"""
        self.memory_lst.append({"role": "assistant", "content": memory})

    @operation
    async def ask(self):
        """Query and get response"""
        from langchain_core.messages import AIMessage
        
        messages = []
        for msg in self.memory_lst:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        response = await self.llm.ainvoke(messages)
        response.name = self.name
        response.id = self.agent_id
        return response