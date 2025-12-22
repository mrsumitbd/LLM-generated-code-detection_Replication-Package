import pandas as pd
import os, sys
import openai
import json
import time
import backoff
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv('../.env')


def batch_generate_with_openai(
    skeletons: List[str],
    model: str,
    granularity='class',
    temperature: float = 0.0,
    reasoning_effort: Optional[str] = None,  # Ignored for Codex
    max_tokens: int = 8192  # Added for Codex
) -> List[str]:

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

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Exponential backoff decorator
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def api_call_with_backoff(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def is_reasoning_model(model: str) -> bool:
        """Test if the model is a reasoning model or Codex by checking if 'temperature' causes an error."""
        try:
            api_call_with_backoff(
                client.chat.completions.create,
                model=model,
                messages=[{"role": "user", "content": "test"}],
                temperature=0.7,
                max_tokens=1
            )
            return False
        except openai.BadRequestError as e:
            error_msg = str(e).lower()
            if "temperature" in error_msg or "unsupported" in error_msg:
                return True
            raise  # Re-raise if different error

    def is_codex_model(model: str) -> bool:
        """Check if the model is a Codex model (e.g., contains 'codex')."""
        return "codex" in model.lower()

    # Detect model type
    use_codex = is_codex_model(model)
    use_reasoning = is_reasoning_model(model) if not use_codex else True  # Codex behaves like reasoning (no temperature)
    logger.info(f"Model {model} detected as {'Codex' if use_codex else 'reasoning' if use_reasoning else 'non-reasoning'} model")

    # System prompt
    system_prompt = (
        f"You are an expert Python programmer who can correctly implement a complete Python {granularity} based on provided {instruction_unit}."
    )

    # Create batch requests JSONL
    file_path = 'openai_batch_requests.jsonl'
    with open(file_path, 'w') as f:
        for i, skeleton in enumerate(skeletons):
            user_prompt = f"Implement the following {granularity}. Do not explain the code. The given {instruction_unit} is as follows:\n{skeleton}"
            if use_codex:
                # Codex uses /v1/responses with a single prompt
                body = {
                    "model": model,
                    "prompt": f"{system_prompt}\n{user_prompt}",
                    "max_tokens": max_tokens
                }
            else:
                # Non-Codex models use chat completions
                if use_reasoning:
                    messages = [
                        {"role": "developer", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                else:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                body = {
                    "model": model,
                    "messages": messages
                }
                if not use_reasoning:
                    body["temperature"] = temperature
                if use_reasoning and reasoning_effort and not use_codex:
                    body["reasoning_effort"] = reasoning_effort

            request = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/responses" if use_codex else "/v1/chat/completions",
                "body": body
            }
            f.write(json.dumps(request) + '\n')
    logger.info(f"Created batch file {file_path} with {len(skeletons)} requests")

    # Upload file
    with open(file_path, 'rb') as f:
        file_response = api_call_with_backoff(client.files.create, file=f, purpose='batch')
    file_id = file_response.id
    logger.info(f"Uploaded batch file, ID: {file_id}")

    # Create batch job
    batch = api_call_with_backoff(
        client.batches.create,
        input_file_id=file_id,
        endpoint="/v1/responses" if use_codex else "/v1/chat/completions",
        completion_window="24h"
    )
    batch_id = batch.id
    logger.info(f"Created batch job, ID: {batch_id}")

    # Poll for completion
    while True:
        status = api_call_with_backoff(client.batches.retrieve, batch_id)
        completed = 0
        total = len(skeletons)
        if hasattr(status, 'request_counts'):
            completed = status.request_counts.completed
            total = status.request_counts.total
        logger.info(f"Polling batch job {batch_id}: Status: {status.status}, Requests processed: {completed}/{total}")
        if status.status == 'completed':
            output_file_id = status.output_file_id
            logger.info(f"Batch completed, output file ID: {output_file_id}")
            error_file_id = status.error_file_id if hasattr(status, 'error_file_id') and status.error_file_id else None
            logger.info(f"Error file ID: {error_file_id if error_file_id else 'None'}")
            break
        elif status.status in ['failed', 'expired', 'cancelled']:
            logger.error(f"Batch failed with status: {status.status}")
            raise ValueError(f"Batch failed with status: {status.status}")
        time.sleep(30)  # Poll every 30 seconds

    # Retrieve output
    output_response = api_call_with_backoff(client.files.content, output_file_id)
    output_file_path = 'openai_batch_outputs.jsonl'
    with open(output_file_path, 'wb') as f:
        f.write(output_response.content)
    logger.info(f"Downloaded batch output to {output_file_path}")

    # Retrieve error file if it exists
    error_file_path = None
    if error_file_id:
        error_response = api_call_with_backoff(client.files.content, error_file_id)
        error_file_path = 'openai_batch_errors.jsonl'
        with open(error_file_path, 'wb') as f:
            f.write(error_response.content)
        logger.info(f"Downloaded error file to {error_file_path}")

    # Extract code snippets
    results = {}
    with open(output_file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            custom_id = data['custom_id']
            if data['response']['status_code'] == 200:
                if use_codex:
                    content = data['response']['body']['output']['text']
                else:
                    content = data['response']['body']['choices'][0]['message']['content']
                results[custom_id] = content
            else:
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed with status {data['response']['status_code']}")

    # Process error file if exists
    if error_file_path:
        with open(error_file_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                custom_id = data['custom_id']
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed with error: {data.get('error', 'No error details')}")

    # Build code_snippets list in order
    code_snippets = []
    for i in range(len(skeletons)):
        custom_id = f"request-{i}"
        code_snippets.append(results.get(custom_id, None))

    logger.info(f"Extracted {len(code_snippets)} code snippets from batch output (including Nones for failures)")

    # Clean up files (optional)
    os.remove(file_path)
    os.remove(output_file_path)
    if error_file_path:
        os.remove(error_file_path)
    logger.info(f"Cleaned up temporary files")

    return code_snippets


def class_main():
    cls_df = pd.read_csv("../data/metadata_folder/uncontaminated_cls_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = cls_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = cls_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    cls_sample_df_filtered = cls_df[cls_df.repository_name.isin(relevant_repos)]

    # cls_sample_df_filtered = cls_sample_df_filtered.iloc[start:end, :]

    cls_sample_df_filtered.dropna(inplace=True, subset=['class_skeleton'])

    generated = batch_generate_with_openai(cls_sample_df_filtered['class_skeleton'].tolist(), model=model)

    cls_sample_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in cls_sample_df_filtered.columns:
        cls_sample_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)

    cls_sample_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model}_class_{start}-{end}.csv", index=False)

def function_main():
    func_df = pd.read_csv("../data/metadata_folder/uncontaminated_func_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = func_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = func_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    func_df_filtered = func_df[func_df.repository_name.isin(relevant_repos)]

    # cls_sample_df_filtered = cls_sample_df_filtered.iloc[start:end, :]

    func_df_filtered.dropna(inplace=True, subset=['func_signature'])

    generated = batch_generate_with_openai(func_df_filtered['func_signature'].tolist(), model=model, granularity='function')

    func_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in func_df_filtered.columns:
        func_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)

    func_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model}_func_{start}-{end}.csv", index=False)

if __name__ == "__main__":
    # class_main()
    function_main()