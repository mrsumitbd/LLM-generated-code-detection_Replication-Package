import google.generativeai as genai

def get_model(name=GEMINI_PRO, temperature=0.2, top_p=0.95, top_k=40, max_output_tokens=2048):
    return genai.GenerativeModel(
        model_name=name,
        generation_config={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens
        }
    )