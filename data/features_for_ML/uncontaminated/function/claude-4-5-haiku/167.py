def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
    from random import Random
    from typing import Any
    
    # Scale difficulty to reasonable ranges
    difficulty = max(0.1, min(difficulty, 10.0))
    
    # Generate problem based on difficulty
    if difficulty < 2.0:
        # Simple arithmetic
        a = rng.randint(1, int(10 * difficulty))
        b = rng.randint(1, int(10 * difficulty))
        op = rng.choice(['+', '-', '*'])
        
        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        else:
            result = a * b
        
        question = f"{a} {op} {b}"
        
    elif difficulty < 5.0:
        # Multi-step arithmetic
        a = rng.randint(1, int(20 * difficulty))
        b = rng.randint(1, int(20 * difficulty))
        c = rng.randint(1, int(20 * difficulty))
        ops = [rng.choice(['+', '-', '*']) for _ in range(2)]
        
        question = f"{a} {ops[0]} {b} {ops[1]} {c}"
        
        # Evaluate with proper order of operations
        if ops[0] == '*':
            temp = a * b
        elif ops[0] == '+':
            temp = a + b
        else:
            temp = a - b
        
        if ops[1] == '*':
            result = temp * c
        elif ops[1] == '+':
            result = temp + c
        else:
            result = temp - c
    
    else:
        # Complex problems with variables
        a = rng.randint(1, int(50 * difficulty))
        b = rng.randint(1, int(50 * difficulty))
        c = rng.randint(1, int(50 * difficulty))
        
        question = f"Solve: {a}x + {b} = {c}"
        
        if a != 0:
            result = (c - b) / a
        else:
            result = 0
    
    return {
        "question": question,
        "answer": result,
        "difficulty": difficulty
    }