from launch.agent.prompt import ReAct_prompt
from langchain.schema import HumanMessage, SystemMessage
from launch.agent.state import AgentState, auto_catch

def verify(max_steps: int, state: AgentState) -> dict:
    """
    ReAct agent for environment verification through test command execution.
    
    Args:
        max_steps (int): Maximum number of verification steps allowed
        state (AgentState): Current agent state with setup results
        
    Returns:
        dict: Updated state with verification results and success status
    """
    if state["exception"]:
        raise state["exception"]

    session = state["session"]
    llm = state["llm"]
    logger = state["logger"]
    setup_commands = state["setup_commands"]
    logger.info("-" * 10 + "Start verify conversation" + "-" * 10)
    messages = [
        SystemMessage(
            system_msg.format(
                base_image=state["base_image"], setup_commands=setup_commands
            )
        ),
        HumanMessage(
            ReAct_prompt.format(
                tools=VerifyAction.__doc__,
                project_structure=state["repo_structure"],
                docs=state["docs"],
            )
        ),
    ]
    prefix_messages = len(messages)
    commands = []
    step = 0
    success = False
    issue = None
    while step < max_steps:
        step += 1
        # uses a window to avoid exceed context
        if len(messages) < VERIFY_CONVERSATION_WINDOW + prefix_messages:
            input_messages = messages
        else:
            input_messages = (
                messages[:prefix_messages] + messages[-VERIFY_CONVERSATION_WINDOW:]
            )
        response = llm.invoke(input_messages)
        # print(response.pretty_repr())
        logger.info(response.pretty_repr())
        messages.append(response)
        action = parse_verify_action(response.content)
        if action.action == "command":
            commands.append(action.args)
        observation = observation_for_verify_action(action, session)
        message = HumanMessage(f"Observation:\n{observation.content}")
        # print(message.pretty_repr())
        logger.info(message.pretty_repr())
        messages.append(message)
        if action.action == "issue":
            if observation.content == "":
                success = True
                logger.info("The setup is successful")
                break
            issue = observation.content
            logger.info(f"Verification failed due to: {issue}")
            break

    trials = state["trials"] + 1
    logger.info("-" * 10 + "End verify conversation" + "-" * 10)
    return {
        "messages": messages,
        "verify_messages": messages[prefix_messages:],
        "test_commands": commands,
        "commands": commands,
        "trials": trials,
        "success": success,
        "issue": issue,
    }