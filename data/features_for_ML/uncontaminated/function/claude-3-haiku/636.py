from langchain.agents import create_agent
from langchain.agents.agent_toolkits import create_openai_agent
from langchain.agents.agent_toolkits.openai_plugin.base import OpenAIPluginAgent
from langchain.agents.agent_toolkits.openai_plugin.toolkit import OpenAIPluginToolkit
from langchain.agents.agent_toolkits.openai_plugin.tools import OpenAIPluginTool
from langchain.agents.agent_toolkits.openai_plugin.config import OpenAIPluginConfig
from langchain.agents.agent_toolkits.openai_plugin.memory import OpenAIPluginMemory
from langchain.agents.agent_toolkits.openai_plugin.prompt import OpenAIPluginPromptTemplate
from langchain.agents.agent_toolkits.openai_plugin.agent import OpenAIPluginAgent
from langchain.agents.agent_toolkits.openai_plugin.tools import get_openai_plugin_tools
from langchain.agents.agent_toolkits.openai_plugin.config import OpenAIPluginConfig
from langchain.agents.agent_toolkits.openai_plugin.memory import OpenAIPluginMemory
from langchain.agents.agent_toolkits.openai_plugin.prompt import OpenAIPluginPromptTemplate
from langchain.agents.agent_toolkits.openai_plugin.agent import OpenAIPluginAgent
from langchain.agents.agent_toolkits.openai_plugin.tools import get_openai_plugin_tools
from langchain.agents.agent_toolkits.openai_plugin.config import OpenAIPluginConfig
from langchain.agents.agent_toolkits.openai_plugin.memory import OpenAIPluginMemory
from langchain.agents.agent_toolkits.openai_plugin.prompt import OpenAIPluginPromptTemplate
from langchain.agents.agent_toolkits.openai_plugin.agent import OpenAIPluginAgent

def create_full_agent(
    model_name: str,
    vision_model_name: str | None,
    no_stream: bool = False,
    compact_every_n_iteration: int | None = None,
    max_tokens_working_memory: int | None = None,
) -> Agent:
    """Create an agent with the specified model and many tools."""
    config = OpenAIPluginConfig(
        model_name=model_name,
        vision_model_name=vision_model_name,
        no_stream=no_stream,
        compact_every_n_iteration=compact_every_n_iteration,
        max_tokens_working_memory=max_tokens_working_memory,
    )
    toolkit = OpenAIPluginToolkit(config=config)
    tools = get_openai_plugin_tools(toolkit)
    memory = OpenAIPluginMemory(config=config)
    prompt = OpenAIPluginPromptTemplate(config=config, tools=tools)
    agent = OpenAIPluginAgent(
        llm=toolkit.llm,
        tools=tools,
        memory=memory,
        prompt=prompt,
        config=config,
    )
    return agent