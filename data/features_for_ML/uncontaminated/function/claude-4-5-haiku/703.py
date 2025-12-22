import anthropic
import json
import random
from typing import Optional

def load_environment(
    dataset_name: str = "math",
    dataset_split: str = "train",
    num_train_examples: int = -1,
    max_turns: int = 100,
    **kwargs,
):
    """
    Load a dataset environment for multi-turn conversations.
    
    Args:
        dataset_name: Name of the dataset to load (default: "math")
        dataset_split: Dataset split to use (default: "train")
        num_train_examples: Number of examples to load (-1 for all)
        max_turns: Maximum number of turns in conversation
        **kwargs: Additional arguments
    
    Returns:
        A dictionary containing the environment configuration and dataset
    """
    
    # Initialize Anthropic client
    client = anthropic.Anthropic()
    
    # Create environment configuration
    environment = {
        "dataset_name": dataset_name,
        "dataset_split": dataset_split,
        "num_train_examples": num_train_examples,
        "max_turns": max_turns,
        "client": client,
        "examples": [],
        "current_example_idx": 0,
        "conversation_history": [],
        "turn_count": 0,
    }
    
    # Load dataset based on dataset_name
    if dataset_name.lower() == "math":
        # Create sample math problems for demonstration
        sample_problems = [
            {
                "problem": "What is 2 + 2?",
                "solution": "2 + 2 = 4",
                "answer": "4"
            },
            {
                "problem": "Solve for x: 2x + 5 = 13",
                "solution": "2x + 5 = 13\n2x = 8\nx = 4",
                "answer": "4"
            },
            {
                "problem": "What is the derivative of x^2?",
                "solution": "d/dx(x^2) = 2x",
                "answer": "2x"
            },
            {
                "problem": "Calculate 15% of 200",
                "solution": "15% of 200 = 0.15 * 200 = 30",
                "answer": "30"
            },
            {
                "problem": "What is the area of a circle with radius 5?",
                "solution": "Area = πr^2 = π * 5^2 = 25π ≈ 78.54",
                "answer": "25π or approximately 78.54"
            },
        ]
        
        if num_train_examples > 0:
            environment["examples"] = sample_problems[:num_train_examples]
        else:
            environment["examples"] = sample_problems
            
    elif dataset_name.lower() == "gsm8k":
        # Create sample GSM8K-style problems
        sample_problems = [
            {
                "problem": "James has 5 apples. He buys 3 more apples. How many apples does James have now?",
                "solution": "James starts with 5 apples and buys 3 more, so 5 + 3 = 8 apples.",
                "answer": "8"
            },
            {
                "problem": "If a book costs $12 and Sarah has $50, how much change will she get after buying the book?",
                "solution": "Sarah has $50 and the book costs $12, so 50 - 12 = $38 change.",
                "answer": "$38"
            },
        ]
        
        if num_train_examples > 0:
            environment["examples"] = sample_problems[:num_train_examples]
        else:
            environment["examples"] = sample_problems
            
    else:
        # Default to empty examples for unknown datasets
        environment["examples"] = []
    
    # Shuffle examples if requested
    if kwargs.get("shuffle", False):
        random.shuffle(environment["examples"])
    
    return environment