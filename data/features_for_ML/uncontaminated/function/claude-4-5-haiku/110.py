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
    import json
    from datetime import datetime
    
    try:
        # Get code blocks and results from executor
        code_blocks = getattr(self, 'code_blocks', [])
        execution_results = getattr(self, 'execution_results', {})
        
        # Create notebook cells
        cells = []
        
        # Add markdown cell with metadata
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# Conversation History\n",
                f"Generated on: {datetime.now().isoformat()}"
            ]
        })
        
        # Add code cells with their outputs
        for i, code_block in enumerate(code_blocks):
            # Add code cell
            cells.append({
                "cell_type": "code",
                "execution_count": i + 1,
                "metadata": {},
                "source": [code_block] if isinstance(code_block, str) else code_block,
                "outputs": []
            })
            
            # Add output if available
            if str(i) in execution_results:
                result = execution_results[str(i)]
                output_cell = {
                    "output_type": "execute_result",
                    "data": {
                        "text/plain": [str(result)]
                    },
                    "metadata": {},
                    "execution_count": i + 1
                }
                cells[-1]["outputs"].append(output_cell)
        
        # Create notebook structure
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(notebook, f, indent=2)
            
    except Exception as e:
        raise Exception(f"Error saving conversation history to notebook: {str(e)}")