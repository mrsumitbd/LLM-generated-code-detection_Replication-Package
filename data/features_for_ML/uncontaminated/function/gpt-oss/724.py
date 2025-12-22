def gpt_personality_analysis(dialogs, client):
    """
    Analyzes conversations to extract structured personality traits, general user data, 
    and assistant-related knowledge.
    Returns: {"profile": str, "user_data": str, "assistant_knowledge": str}
    """
    # Prepare the conversation text
    conversation = "\n".join(
        f"{msg.get('role', 'user').capitalize()}: {msg.get('content', '')}"
        for msg in dialogs
    )

    # Build the prompt for the LLM
    system_prompt = (
        "You are an expert analyst. Based on the conversation below, extract the following "
        "information in a JSON object with keys 'profile', 'user_data', and 'assistant_knowledge':\n\n"
        "1. **Profile** – A concise description of the user's personality traits, preferences, "
        "and communication style.\n"
        "2. **User Data** – Any factual information about the user that can be inferred "
        "(e.g., age range, occupation, interests, location, etc.).\n"
        "3. **Assistant Knowledge** – Any knowledge or context that the assistant should "
        "retain for future interactions (e.g., user’s preferred tone, recurring topics, "
        "specific instructions, etc.).\n\n"
        "Respond **only** with the JSON object. Do not include any additional text."
    )

    user_prompt = f"Conversation:\n{conversation}\n\nExtract the requested information."

    # Determine the client interface
    # Prefer chat if available, otherwise fallback to completions
    try:
        if hasattr(client, "chat"):
            response = client.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            # Assume the response is a dict with 'choices' and 'message'
            content = response["choices"][0]["message"]["content"]
        elif hasattr(client, "completion"):
            response = client.completion(
                prompt=f"{system_prompt}\n\n{user_prompt}",
                max_tokens=500,
                temperature=0.2,
                stop=None,
            )
            content = response["choices"][0]["text"]
        else:
            raise ValueError("Client does not support chat or completion methods.")
    except Exception as e:
        # Fallback: return empty strings if the client fails
        return {"profile": "", "user_data": "", "assistant_knowledge": ""}

    # Parse the JSON response
    import json
    try:
        data = json.loads(content.strip())
        # Ensure all keys exist
        profile = data.get("profile", "")
        user_data = data.get("user_data", "")
        assistant_knowledge = data.get("assistant_knowledge", "")
    except json.JSONDecodeError:
        # If parsing fails, return empty strings
        profile = ""
        user_data = ""
        assistant_knowledge = ""

    return {
        "profile": profile,
        "user_data": user_data,
        "assistant_knowledge": assistant_knowledge,
    }