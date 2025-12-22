from pathlib import Path
from local_operator.notebook import save_code_history_to_notebook

def save_conversation_history_to_notebook(file_path: str = "notebook.ipynb") -> None:
        """Save the conversation history to an IPython notebook file (.ipynb).

        This function retrieves the code blocks and their execution results from the
        executor, formats them as notebook cells, and saves them to a .ipynb file
        in JSON format.

        Args:
            file_path (str): The path to save the notebook to. Defaults to "notebook.ipynb".

        Raises:
            Exception: If there is an error during notebook creation or file saving.
        """
        try:
            save_code_history_to_notebook(
                code_history=executor.agent_state.execution_history,
                model_configuration=executor.model_configuration,
                max_conversation_history=executor.max_conversation_history,
                detail_conversation_length=executor.detail_conversation_length,
                max_learnings_history=executor.max_learnings_history,
                file_path=Path(file_path),
            )
            print(f"Notebook saved to {file_path}")

        except Exception as e:
            raise Exception(f"Failed to save conversation history to notebook: {str(e)}")