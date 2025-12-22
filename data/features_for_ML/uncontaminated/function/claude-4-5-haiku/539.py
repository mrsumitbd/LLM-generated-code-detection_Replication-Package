def redo():
    global current_state, redo_stack, undo_stack
    if redo_stack:
        state = redo_stack.pop()
        undo_stack.append(current_state)
        current_state = state
        update_display()