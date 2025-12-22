from typing import Sequence, Iterator, Optional
from transformers.generation.utils import GenerationMixin
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedTokenizer,
    BatchEncoding,
)

def __rollout(
        model: GenerationMixin,
        tokenizer: PreTrainedTokenizer,
        prompt: Sequence[str],
        device: str = "cpu",
    ) -> Sequence[str]:
        tokenized_prompt = tokenizer(
            prompt, padding=True, return_tensors="pt", padding_side="left"
        ).to(device)
        output = model.generate(
            **tokenized_prompt,
            pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=32,
            do_sample=True,
            top_p=0.9,
            top_k=50,
            temperature=1.0,
        )
        continuation = [
            i[len(j) :]
            for i, j in zip(
                tokenizer.batch_decode(output, skip_special_tokens=True), prompt
            )
        ]
        return continuation