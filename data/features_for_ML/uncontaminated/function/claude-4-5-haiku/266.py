import anthropic
import json


def dtw_cuda(x, BLOCK_SIZE=1024):
    """
    Generate CUDA code for Dynamic Time Warping using Claude API.
    
    Args:
        x: Input sequence or parameter for DTW
        BLOCK_SIZE: CUDA block size for GPU computation
    
    Returns:
        Generated CUDA code as a string
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Generate optimized CUDA C++ code for Dynamic Time Warping (DTW) algorithm with the following specifications:

1. Input parameter: x (sequence data)
2. CUDA block size: {BLOCK_SIZE}
3. The code should:
   - Implement DTW distance calculation on GPU
   - Use shared memory for optimization
   - Handle 2D cost matrix computation
   - Include proper memory management (allocation/deallocation)
   - Have a kernel function for parallel computation
   - Include a host function to launch the kernel
   - Use appropriate synchronization

Please provide complete, production-ready CUDA code that:
- Computes the DTW distance between two sequences
- Uses the specified block size for thread organization
- Includes error checking for CUDA operations
- Has clear comments explaining the algorithm
- Is optimized for GPU execution

Return only the CUDA code without any explanation."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    cuda_code = message.content[0].text
    
    return cuda_code


if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    result = dtw_cuda(x, BLOCK_SIZE=256)
    print("Generated CUDA Code:")
    print("=" * 80)
    print(result)