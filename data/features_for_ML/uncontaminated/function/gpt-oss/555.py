import os
import json
import openai

def call_llm(prompt: str) -> str:
    """
    Sends a prompt to an LLM (OpenAI's GPT-3.5-turbo by default) and returns the response text.
    The OpenAI API key must be set in the environment variable `OPENAI_API_KEY`.
    """
    # Ensure the API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    openai.api_key = api_key

    try:
        # Use the chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
            n=1,
            stop=None,
        )
        # Extract the assistant's reply
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        # In case of an error, return a helpful message
        return f"Error calling LLM: {e}"