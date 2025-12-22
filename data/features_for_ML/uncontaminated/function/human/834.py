from datetime import datetime
import copy
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from src.interface.agent import State

def apply_prompt_template(prompt_name: str, state: State, template:str=None) -> list:
    state = copy.deepcopy(state)
    messages = []
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, dict) and 'role' in msg:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            else:
                messages.append({"role": "assistant", "content": msg["content"]})
    state["messages"] = messages
    
    _template, _ = get_prompt_template(prompt_name) if not template else template
    system_prompt = PromptTemplate(
        input_variables=["CURRENT_TIME"],
        template=_template,
    ).format(CURRENT_TIME=datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"), **state)

    return [{"role": "system", "content": system_prompt}] + messages