def get_model(name=GEMINI_PRO, temperature=0.2, top_p=0.95, top_k=40, max_output_tokens=2048):
    import openai
    openai.api_key = "your_openai_api_key"

    model_parameters = {
        "model": name,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": max_output_tokens,
        "n": 1,
        "stop": None,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    response = openai.Completion.create(**model_parameters)
    return response.choices[0].text.strip()