import anthropic


def get_task_str(task_type_ind, object_ind, receptacle_ind=None, toggle_ind=None, mrecep_ind=None):
    """
    Generate a task string based on task type and object indices using Claude API.
    
    Args:
        task_type_ind: Index indicating the type of task
        object_ind: Index of the object involved in the task
        receptacle_ind: Optional index of the receptacle
        toggle_ind: Optional index of the toggle
        mrecep_ind: Optional index of the main receptacle
    
    Returns:
        A string describing the task
    """
    client = anthropic.Anthropic()
    
    # Build the prompt with the provided indices
    prompt = f"""Generate a task description based on the following indices:
- Task type index: {task_type_ind}
- Object index: {object_ind}
- Receptacle index: {receptacle_ind}
- Toggle index: {toggle_ind}
- Main receptacle index: {mrecep_ind}

Please provide a clear, concise task description that incorporates these indices appropriately."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test the function
    result = get_task_str(1, 5, receptacle_ind=2, toggle_ind=3, mrecep_ind=4)
    print(result)