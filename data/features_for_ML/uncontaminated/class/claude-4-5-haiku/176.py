import os
import time
import anthropic


class ContextualAutoTuner:

    def __init__(self, fn, is_dist=False, n_repeat=5, n_warmup=3):
        self.fn = fn
        self.is_dist = is_dist
        self.n_repeat = n_repeat
        self.n_warmup = n_warmup
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.tuning_history = []

    def dist_print(self, *args, **kwargs):
        if not self.is_dist or (self.is_dist and int(os.environ.get("RANK", 0)) == 0):
            print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        # Warm up runs
        for _ in range(self.n_warmup):
            self.fn(*args, **kwargs)

        # Timed runs
        times = []
        for _ in range(self.n_repeat):
            start = time.time()
            result = self.fn(*args, **kwargs)
            end = time.time()
            times.append(end - start)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        # Prepare context for Claude
        fn_name = self.fn.__name__
        fn_code = self.fn.__code__.co_filename
        
        context = f"""
Function: {fn_name}
File: {fn_code}
Average execution time: {avg_time:.6f}s
Min time: {min_time:.6f}s
Max time: {max_time:.6f}s
Number of runs: {self.n_repeat}
Warmup runs: {self.n_warmup}
"""

        # Get optimization suggestions from Claude
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Based on the following performance metrics for a Python function, 
provide brief optimization suggestions:

{context}

Please provide 2-3 specific, actionable optimization suggestions for this function."""
                }
            ]
        )

        suggestions = message.content[0].text

        # Store in history
        self.tuning_history.append({
            "function": fn_name,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "suggestions": suggestions
        })

        # Print results
        self.dist_print(f"\n=== Performance Report for {fn_name} ===")
        self.dist_print(f"Average time: {avg_time:.6f}s")
        self.dist_print(f"Min time: {min_time:.6f}s")
        self.dist_print(f"Max time: {max_time:.6f}s")
        self.dist_print(f"\n=== Optimization Suggestions ===")
        self.dist_print(suggestions)
        self.dist_print("=" * 40)

        return result