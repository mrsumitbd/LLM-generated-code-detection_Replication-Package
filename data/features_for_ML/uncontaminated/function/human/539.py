def redo():
    global stack_pointer, number_of_prompts
    if (stack_pointer < number_of_prompts):
        stack_pointer += 1
        return stack_pointer
    return number_of_prompts