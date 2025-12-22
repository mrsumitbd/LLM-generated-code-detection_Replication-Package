import openai

def call_ag():
    openai.api_key = "your_api_key_here"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Hello, how are you?",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()