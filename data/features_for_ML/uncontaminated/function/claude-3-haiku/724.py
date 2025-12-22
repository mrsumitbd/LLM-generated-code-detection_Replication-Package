import openai
from collections import defaultdict

def gpt_personality_analysis(dialogs, client):
    """
    Analyzes conversations to extract structured personality traits, general user data, 
    and assistant-related knowledge.
    Returns: {"profile": str, "user_data": str, "assistant_knowledge": str}
    """
    profile = ""
    user_data = ""
    assistant_knowledge = ""

    for dialog in dialogs:
        prompt = f"Analyze the following conversation and provide a structured personality profile, user data, and assistant knowledge:\n\n{dialog}"
        response = client.create_completion(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )

        result = response.choices[0].text.strip()
        sections = result.split("\n\n")

        for section in sections:
            if section.startswith("Personality Profile:"):
                profile = section.replace("Personality Profile:", "").strip()
            elif section.startswith("User Data:"):
                user_data = section.replace("User Data:", "").strip()
            elif section.startswith("Assistant Knowledge:"):
                assistant_knowledge = section.replace("Assistant Knowledge:", "").strip()

    return {"profile": profile, "user_data": user_data, "assistant_knowledge": assistant_knowledge}