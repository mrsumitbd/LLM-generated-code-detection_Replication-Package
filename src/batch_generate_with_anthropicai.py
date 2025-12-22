
from anthropic import Anthropic, APIError, RateLimitError
import pandas as pd
import os, sys
import json
import time
import backoff
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv('../.env')



def batch_generate_with_claude(
        skeletons: List[str],
        model: str,
        granularity='class',
        temperature: float = 0.0,
        max_tokens: int = 8192,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None
) -> List[str]:
    """
    Generate code completions using Claude's Message Batches API.

    Args:
        skeletons: List of code skeletons to implement
        model: Claude model name (e.g., 'claude-sonnet-4-20250514', 'claude-opus-4-20250514')
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter (optional)
        top_k: Top-k sampling parameter (optional)

    Returns:
        List of generated code strings (None for failed requests)
    """
    if granularity.lower() == "class":
        instruction_unit = "class skeleton"

    else:
        instruction_unit = "function signature"

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Exponential backoff decorator
    @backoff.on_exception(backoff.expo, RateLimitError)
    def api_call_with_backoff(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    # Validate and filter skeletons
    valid_skeletons = []
    skeleton_indices = []  # Track original indices
    for i, skeleton in enumerate(skeletons):
        # Check for invalid skeletons (nan, None, empty strings)
        if skeleton is None or str(skeleton).strip().lower() in ['nan', 'none', '']:
            logger.warning(f"Skipping invalid skeleton at index {i}: {skeleton}")
            continue

        skeleton_str = str(skeleton).strip()

        # Check if skeleton is empty after stripping
        if not skeleton_str:
            logger.warning(f"Skipping empty skeleton at index {i}")
            continue

        # Try to parse as Python code to catch syntax errors
        try:
            import ast
            ast.parse(skeleton_str)
        except SyntaxError as e:
            logger.warning(f"Skipping skeleton at index {i} due to syntax error: {e}")
            continue
        except Exception as e:
            logger.warning(f"Skipping skeleton at index {i} due to parsing error: {e}")
            continue

        valid_skeletons.append(skeleton_str)
        skeleton_indices.append(i)

    if not valid_skeletons:
        logger.error("No valid skeletons to process")
        return [None] * len(skeletons)

    logger.info(f"Processing {len(valid_skeletons)} valid skeletons out of {len(skeletons)} total")

    # System prompt
    system_prompt = (
        f"You are an expert Python programmer who can correctly implement a complete Python {granularity} based on provided {instruction_unit}."
    )

    # Create batch requests JSONL
    file_path = 'claude_batch_requests.jsonl'
    with open(file_path, 'w') as f:
        for i, skeleton in enumerate(valid_skeletons):
            user_prompt = f"Implement the following {granularity}. Do not explain the code. The given {instruction_unit} is as follows:\n{skeleton}"

            # Build request body according to Claude's Message Batches API format
            body = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "user", "content": user_prompt}
                ]
            }

            # Add system prompt
            body["system"] = system_prompt

            # Add sampling parameters
            body["temperature"] = temperature
            if top_p is not None:
                body["top_p"] = top_p
            if top_k is not None:
                body["top_k"] = top_k

            # Claude's batch format
            request = {
                "custom_id": f"request-{i}",
                "params": body
            }
            f.write(json.dumps(request) + '\n')

    logger.info(f"Created batch file {file_path} with {len(valid_skeletons)} requests")

    # Upload and create batch job
    try:
        # Read the JSONL file and parse each line into request objects
        requests_list = []
        with open(file_path, 'r') as f:
            for line in f:
                requests_list.append(json.loads(line))

        batch = api_call_with_backoff(
            client.messages.batches.create,
            requests=requests_list
        )
        batch_id = batch.id
        logger.info(f"Created batch job, ID: {batch_id}")
    except APIError as e:
        logger.error(f"Failed to create batch: {e}")
        raise

    # Poll for completion
    while True:
        try:
            status = api_call_with_backoff(client.messages.batches.retrieve, batch_id)

            # Get request counts
            request_counts = status.request_counts
            completed = request_counts.succeeded + request_counts.errored + request_counts.canceled + request_counts.expired
            total = completed + request_counts.processing

            logger.info(
                f"Polling batch job {batch_id}: Status: {status.processing_status}, "
                f"Succeeded: {request_counts.succeeded}, "
                f"Errored: {request_counts.errored}, "
                f"Processing: {request_counts.processing}, "
                f"Requests processed: {completed}/{total}"
            )

            if status.processing_status == 'ended':
                logger.info(f"Batch completed")
                logger.info(
                    f"Final counts - Succeeded: {request_counts.succeeded}, "
                    f"Errored: {request_counts.errored}, "
                    f"Canceled: {request_counts.canceled}, "
                    f"Expired: {request_counts.expired}"
                )
                break
            elif status.processing_status in ['canceling', 'canceled']:
                logger.error(f"Batch was canceled")
                raise ValueError(f"Batch was canceled")

            time.sleep(30)  # Poll every 30 seconds

        except APIError as e:
            logger.error(f"Error polling batch status: {e}")
            raise

    # Retrieve results
    try:
        results = {}

        # Iterate through all results using pagination
        for result in api_call_with_backoff(client.messages.batches.results, batch_id):
            custom_id = result.custom_id

            if result.result.type == 'succeeded':
                # Extract the content from the successful response
                content = result.result.message.content[0].text
                results[custom_id] = content
            elif result.result.type == 'errored':
                # Log error details
                error = result.result.error
                error_type = getattr(error, 'type', 'unknown')
                error_message = str(error) if hasattr(error, '__str__') else 'No error details'
                logger.warning(
                    f"Request {custom_id} failed with error type: {error_type}, "
                    f"error: {error_message}"
                )
                results[custom_id] = None
            else:
                # Handle other result types (canceled, expired)
                logger.warning(f"Request {custom_id} had result type: {result.result.type}")
                results[custom_id] = None

        logger.info(f"Retrieved {len(results)} results from batch")

    except APIError as e:
        logger.error(f"Error retrieving batch results: {e}")
        raise

    # Build code_snippets list in order, mapping back to original indices
    code_snippets = [None] * len(skeletons)  # Initialize with None for all
    for i, original_idx in enumerate(skeleton_indices):
        custom_id = f"request-{i}"
        code_snippets[original_idx] = results.get(custom_id, None)

    successful_count = sum(1 for snippet in code_snippets if snippet is not None)
    logger.info(
        f"Extracted {len(code_snippets)} code snippets from batch output "
        f"({successful_count} successful, {len(code_snippets) - successful_count} failed/invalid)"
    )

    # Clean up files (optional)
    try:
        os.remove(file_path)
        logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to clean up temporary file: {e}")

    return code_snippets


def class_level_generation():
    cls_df = pd.read_csv("../data/metadata_folder/uncontaminated_cls_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = cls_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = cls_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    cls_sample_df_filtered = cls_df[cls_df.repository_name.isin(relevant_repos)]

    # cls_sample_df_filtered = cls_sample_df_filtered.iloc[start:end, :]

    cls_sample_df_filtered.dropna(inplace=True, subset=['class_skeleton'])

    generated = batch_generate_with_claude(cls_sample_df_filtered['class_skeleton'].tolist(), model=model, max_tokens=4096)

    cls_sample_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in cls_sample_df_filtered.columns:
        cls_sample_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)

    cls_sample_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model}_class_{start}-{end}.csv", index=False)

def func_level_generation():
    func_df = pd.read_csv("../data/metadata_folder/uncontaminated_func_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = func_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = func_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    func_sample_df_filtered = func_df[func_df.repository_name.isin(relevant_repos)]

    # func_sample_df_filtered = func_sample_df_filtered.iloc[start:end, :]

    func_sample_df_filtered.dropna(inplace=True, subset=['func_signature'])

    generated = batch_generate_with_claude(granularity='function', skeletons=func_sample_df_filtered['func_signature'].tolist(), model=model, max_tokens=4096)

    func_sample_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in func_sample_df_filtered.columns:
        func_sample_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)

    func_sample_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model}_func_{start}-{end}.csv", index=False)

if __name__ == "__main__":
    # class_level_generation()
    func_level_generation()