def save_conversation_history_to_notebook(file_path: str = "notebook.ipynb") -> None:
    import nbformat
    from nbformat.v4 import new_code_cell, new_output, new_notebook

    notebook = new_notebook()
    cells = []

    # Retrieve code blocks and their execution results
    # Assume code_blocks and execution_results are defined elsewhere
    for code_block, execution_result in zip(code_blocks, execution_results):
        code_cell = new_code_cell(code_block)
        output = new_output(output_type='execute_result', data={'text/plain': execution_result})
        code_cell.outputs = [output]
        cells.append(code_cell)

    notebook.cells = cells

    try:
        with open(file_path, 'w') as f:
            nbformat.write(notebook, f)
    except Exception as e:
        raise Exception("Error during notebook creation or file saving: {}".format(str(e)))