def gpt_personality_analysis(dialogs, client):
    """
    Analyzes conversations to extract structured personality traits, general user data, 
    and assistant-related knowledge.
    Returns: {"profile": str, "user_data": str, "assistant_knowledge": str}
    """
    conversation = "\n".join([f"User: {d['user_input']}\nAssistant: {d['agent_response']}\nTime:{d['timestamp']}" for d in dialogs])

    prompt = """
# Personality and User Data Analysis Task
Analyze the conversation and output in EXACTLY this format:

【User Profile】
1. Core Psychological Traits:
   - [Trait]: [Positive/Negative/Neutral] (Evidence)
   - (Max 5 most prominent traits)

2. Content Preferences:
   - [Topic]: [Like/Dislike/Neutral] (Evidence)
   - (Max 5 strongest preferences)

3. Interaction Style:
   - [Style]: [Preference] (Evidence)
   - (e.g., Direct/Indirect, Detailed/Concise)

4. Value Alignment:
   - [Value]: [Strong/Weak] (Evidence)
   - (e.g., Honesty, Helpfulness)

【User Data】
- [Fact 1]: [Details] (e.g., "User mentioned visiting a park on April 1st, 2025 in New York.")
- [Fact 2]: [Details] (e.g., "User likes pizza, enjoys sci-fi movies, and dislikes rainy weather.")
- (Include events, dates, locations, preferences, or other general or private information explicitly mentioned in the conversation. If none, write "None.")

Conversation:
""" + conversation
    messages = [
        {
            "role": "system",
            "content": """You are a personality and user data analysis engine. Rules:
1. Extract ONLY observable traits and data with direct evidence.
2. Include general user data such as events, dates, locations, and preferences.
3. Use concise and factual statements.
4. If no relevant information is found, output "None"."""
        },
        {"role": "user", "content": prompt}
    ]

    print("Running personality and user data analysis...")
    result = gpt_generate_answer(prompt, messages, client)
    
    # Parse output
    profile, user_data = result.split("【User Data】") if "【User Data】" in result else (result, "None")
    
    # Analyze assistant knowledge
    assistant_knowledge_result = analyze_assistant_knowledge(dialogs, client)
    
    return {
        "profile": profile.replace("【User Profile】", "").strip(),
        "private": user_data.strip(),
        "assistant_knowledge": assistant_knowledge_result["assistant_knowledge"]
    }