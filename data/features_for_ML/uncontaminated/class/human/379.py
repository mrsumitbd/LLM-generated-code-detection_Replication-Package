from deep_next.core.steps.action_plan.srf.file_selection.analysis_model import (
    Analysis,
    RelevantFile,
    analysis_parser,
    example_output_next_steps,
    example_output_select_files,
)
from deep_next.core.steps.action_plan.srf.file_selection.tools.tools import (
    get_llm_tools,
    get_tool_node,
)
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
import json
from deep_next.common.llm import LLMConfigType, create_llm
from langgraph.prebuilt import tools_condition
from deep_next.core.steps.action_plan.srf.file_selection.utils import (
    tools_to_json,
    validate_files,
)
from loguru import logger

class _Node:
    @staticmethod
    def analyze_knowledge(state: State) -> dict:
        """
        Analyze the knowledge and provide the next steps for the investigation.

        The analysis is based on the following pieces of information:
        - The issue statement,
        - The `_root_path_ls`,
        - The tools available,
        - The previous knowledge analysis.
        - The results of tools called after the previous knowledge analysis.
        """
        logger.debug("Analyzing knowledge")

        analysis: Analysis = _call_analyze_llm(state)

        return {
            "_previous_analysis": state["_current_analysis"],
            "_current_analysis": analysis,
            "_iteration_count": state["_iteration_count"] + 1,
        }

    @staticmethod
    def call_tools(state: State) -> dict:
        logger.debug("Calling tools")

        next_steps = json.dumps(state["_current_analysis"].next_steps)
        llm = create_llm(
            LLMConfigType.SRF_TOOLS, tools=get_llm_tools(state["root_path"])
        )
        response = llm.invoke(
            [
                SystemMessage(SelectFilesPrompt.role_description),
                HumanMessage(f"Next steps:\n{next_steps}"),
                HumanMessage(SelectFilesPrompt.output_format_tools),
            ]
        )

        state["_messages"].append(response)

        if (value := tools_condition(state, "_messages")) != "tools":
            raise ValueError(f"Unexpected next node value: {value}")

        result = get_tool_node(state["root_path"]).invoke(state)
        result["_iteration_count"] = state["_iteration_count"] + 1

        return result

    @staticmethod
    def select_files(state: State) -> dict:
        logger.debug("Selecting files")

        if state["_current_analysis"].next_steps:
            logger.warning(
                "The analysis is not complete, however flow was forced to make final "
                f"decision. Next steps: `{state['_current_analysis'].next_steps}`"
            )

        valid_files, invalid_files = validate_files(
            state["_current_analysis"].relevant_files_so_far, state["root_path"]
        )

        logger.debug(f"Relevant files: {valid_files}\nInvalid files: {invalid_files}")

        return {"relevant_files": valid_files, "invalid_files": invalid_files}