import anthropic


def check_finished(goals, pclist):
    """
    Check if a list of goals has been finished based on a list of postconditions.
    
    Args:
        goals: A list of goal strings
        pclist: A list of postcondition strings
    
    Returns:
        A boolean indicating whether all goals have been satisfied by the postconditions
    """
    client = anthropic.Anthropic()
    
    goals_str = "\n".join([f"- {goal}" for goal in goals])
    pclist_str = "\n".join([f"- {pc}" for pc in pclist])
    
    prompt = f"""Given the following goals and postconditions, determine if all goals have been satisfied.

Goals:
{goals_str}

Postconditions:
{pclist_str}

Analyze whether each goal has been achieved based on the postconditions provided. 
Respond with only "true" if all goals are satisfied, or "false" if any goal is not satisfied."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip().lower()
    return response_text == "true"


if __name__ == "__main__":
    goals = [
        "User is logged in",
        "User has admin privileges",
        "Database connection is established"
    ]
    
    pclist = [
        "User authentication successful",
        "Admin role assigned to user",
        "Database connection active"
    ]
    
    result = check_finished(goals, pclist)
    print(f"All goals finished: {result}")
    
    goals2 = [
        "User is logged in",
        "User has admin privileges",
        "Email notification sent"
    ]
    
    pclist2 = [
        "User authentication successful",
        "Admin role assigned to user"
    ]
    
    result2 = check_finished(goals2, pclist2)
    print(f"All goals finished (should be false): {result2}")