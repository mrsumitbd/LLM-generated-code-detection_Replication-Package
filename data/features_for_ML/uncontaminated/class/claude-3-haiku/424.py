import openai
from typing import Dict, Any

class NeMoRLOpenAIChatRequestMixin:
    def model_post_init(self, context: Dict[str, Any]):
        self.openai_api_key = context.get("openai_api_key", None)
        self.openai_model = context.get("openai_model", "gpt-3.5-turbo")
        self.openai_temperature = context.get("openai_temperature", 0.7)
        self.openai_max_tokens = context.get("openai_max_tokens", 2048)
        self.openai_top_p = context.get("openai_top_p", 1)
        self.openai_frequency_penalty = context.get("openai_frequency_penalty", 0)
        self.openai_presence_penalty = context.get("openai_presence_penalty", 0)

        openai.api_key = self.openai_api_key

    def generate_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.openai_temperature,
            max_tokens=self.openai_max_tokens,
            top_p=self.openai_top_p,
            frequency_penalty=self.openai_frequency_penalty,
            presence_penalty=self.openai_presence_penalty
        )

        return response.choices[0].message.content