import openai

def call_llm(prompt):
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()