import json
import os
from typing import Optional

import anthropic


class HelpSteer3Dataset:
    """HelpSteer3 preference dataset for DPO training."""

    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.dataset = []

    def generate_preference_pair(
        self, prompt: str, num_pairs: int = 1
    ) -> list[dict]:
        """Generate preference pairs using Claude."""
        pairs = []

        for _ in range(num_pairs):
            # Generate two different responses
            response1 = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            response2 = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            chosen = response1.content[0].text
            rejected = response2.content[0].text

            pair = {
                "prompt": prompt,
                "chosen": chosen,
                "rejected": rejected,
            }
            pairs.append(pair)

        return pairs

    def add_samples(self, prompts: list[str], num_pairs_per_prompt: int = 1) -> None:
        """Add samples to the dataset."""
        for prompt in prompts:
            pairs = self.generate_preference_pair(prompt, num_pairs_per_prompt)
            self.dataset.extend(pairs)

    def get_dataset(self) -> list[dict]:
        """Get the current dataset."""
        return self.dataset

    def save_dataset(self, filepath: str) -> None:
        """Save the dataset to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.dataset, f, indent=2)

    def load_dataset(self, filepath: str) -> None:
        """Load a dataset from a JSON file."""
        with open(filepath, "r") as f:
            self.dataset = json.load(f)

    def clear_dataset(self) -> None:
        """Clear the current dataset."""
        self.dataset = []

    def get_dataset_size(self) -> int:
        """Get the number of preference pairs in the dataset."""
        return len(self.dataset)

    def format_for_dpo(self) -> list[dict]:
        """Format the dataset for DPO training."""
        formatted = []
        for pair in self.dataset:
            formatted.append(
                {
                    "prompt": pair["prompt"],
                    "chosen": pair["chosen"],
                    "rejected": pair["rejected"],
                }
            )
        return formatted


if __name__ == "__main__":
    dataset = HelpSteer3Dataset()

    test_prompts = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "How do I make a chocolate cake?",
    ]

    print("Generating preference pairs...")
    dataset.add_samples(test_prompts, num_pairs_per_prompt=1)

    print(f"Dataset size: {dataset.get_dataset_size()}")

    formatted_data = dataset.format_for_dpo()
    print("\nFormatted dataset sample:")
    if formatted_data:
        print(json.dumps(formatted_data[0], indent=2))

    dataset.save_dataset("helpsteer3_dataset.json")
    print("\nDataset saved to helpsteer3_dataset.json")