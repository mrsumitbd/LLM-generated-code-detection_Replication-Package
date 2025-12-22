import pandas as pd
import sys
import os
import together
import json
import time
import logging
from typing import List
from dotenv import load_dotenv
load_dotenv('../.env')

def batch_generate_with_together(
    skeletons: List[str],
    model: str,
    temperature: float = 0.0
    #max_tokens: int = 2048  # Reasonable default for code generation
) -> List[str]:
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    # Validate inputs
    if not skeletons:
        logger.error("No skeletons provided")
        raise ValueError("Skeletons list cannot be empty")
    for i, skeleton in enumerate(skeletons):
        if not isinstance(skeleton, str) or not skeleton.strip():
            logger.error(f"Invalid skeleton at index {i}: must be a non-empty string")
            raise ValueError(f"Invalid skeleton at index {i}")

    client = together.Together(api_key=os.getenv("TOGETHER_AI_API_KEY"))

    # System prompt
    system_prompt = (
        "You are an expert Python programmer who can correctly write complete Python programs based on provided class skeletons."
    )

    # Create batch requests JSONL
    file_path = 'batch_requests_togetherai.jsonl'
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, skeleton in enumerate(skeletons):
                user_prompt = f"Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
                body = {
                    "model": model,
                    "prompt": f"{system_prompt}\n{user_prompt}",
                    "temperature": temperature
                    #"max_tokens": max_tokens
                }
                request = {
                    "custom_id": f"request-{i}",
                    "body": body
                }
                json_line = json.dumps(request)
                try:
                    json.loads(json_line)  # Validate JSON
                    logger.debug(f"JSONL line {i}: {json_line}")
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON for request {i}: {str(e)}")
                    raise
                f.write(json_line + '\n')
        logger.info(f"Created batch file {file_path} with {len(skeletons)} requests")
    except Exception as e:
        logger.error(f"Failed to create batch file {file_path}: {str(e)}")
        raise

    # Verify file exists and is not empty
    if not os.path.exists(file_path):
        logger.error(f"Batch file {file_path} was not created")
        raise FileNotFoundError(f"Batch file {file_path} was not created")
    if os.path.getsize(file_path) == 0:
        logger.error(f"Batch file {file_path} is empty")
        raise ValueError(f"Batch file {file_path} is empty")

    # Upload file
    try:
        file_response = client.files.upload(file=file_path, purpose="batch-api")
        file_id = file_response.id
        logger.info(f"Uploaded batch file, ID: {file_id}")
    except Exception as e:
        logger.error(f"Failed to upload batch file: {str(e)}")
        raise

    # Create batch job
    try:
        batch = client.batches.create_batch(
            file_id=file_id,
            endpoint="/v1/chat/completions"
        )
        batch_id = batch.id
        logger.info(f"Created batch job, ID: {batch_id}")
    except Exception as e:
        logger.error(f"Failed to create batch job: {str(e)}")
        raise

    # Poll for completion
    while True:
        try:
            status = client.batches.get_batch(batch_id)
            error_info = getattr(status, 'error', None)
            logger.info(f"Polling batch job {batch_id}: Status: {status.status}, Error: {error_info if error_info else 'None'}")
            if status.status == 'COMPLETED':
                output_file_id = status.output_file_id
                logger.info(f"Batch completed, output file ID: {output_file_id}")
                break
            elif status.status in ['FAILED', 'EXPIRED', 'CANCELLED']:
                logger.error(f"Batch failed with status: {status.status}, Error details: {error_info if error_info else 'No additional details'}")
                raise ValueError(f"Batch failed with status: {status.status}, Error details: {error_info if error_info else 'No additional details'}")
            elif status.status in ['VALIDATING', 'IN_PROGRESS']:
                logger.info(f"Batch still processing: {status.status}")
            else:
                logger.warning(f"Unknown batch status: {status.status}")
        except Exception as e:
            logger.error(f"Failed to retrieve batch status: {str(e)}")
            raise
        time.sleep(30)  # Poll every 30 seconds

    # Retrieve output
    try:
        output_file_path = 'batch_outputs_togetherai.jsonl'
        client.files.retrieve_content(id=output_file_id, output=output_file_path)
    except Exception as e:
        logger.error(f"Failed to retrieve batch output: {str(e)}")
        raise

    # Extract code snippets (map by custom_id to preserve order)
    results = {}
    with open('batch_outputs_togetherai.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['response']['status_code'] == 200:
                content = data['response']['body']['choices'][0]['text']
                results[data['custom_id']] = content
            else:
                logger.warning(f"Request {data['custom_id']} failed with status {data['response']['status_code']}, Error: {data.get('error', 'No error details')}")
    code_snippets = [results.get(f"request-{i}", None) for i in range(len(skeletons))]
    logger.info(f"Extracted {len(code_snippets)} code snippets from batch output")

    # Clean up temporary files
    try:
        os.remove(file_path)
        os.remove(output_file_path)
        logger.info(f"Cleaned up temporary files: {file_path}, {output_file_path}")
    except Exception as e:
        logger.warning(f"Failed to clean up files: {str(e)}")

    return code_snippets


def generate_with_together(skeletons, model, granularity):
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

    # Validate inputs
    if not skeletons:
        logger.error("No skeletons provided")
        raise ValueError("Skeletons list cannot be empty")
    for i, skeleton in enumerate(skeletons):
        if not isinstance(skeleton, str) or not skeleton.strip():
            logger.error(f"Invalid skeleton at index {i}: must be a non-empty string")
            raise ValueError(f"Invalid skeleton at index {i}")

    client = together.Together(api_key=os.getenv("TOGETHER_AI_API_KEY"))

    generated_snippets = []

    counter = 1
    for skeleton in skeletons:
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.0,
                messages=[
                    {
                        "role": "assistant",
                        "content": f"You are an expert Python programmer who can correctly implement a complete Python {granularity} based on provided {instruction_unit}."
                    },
                    {
                        "role": "user",
                        "content": f"Implement the following {granularity}. Do not explain the code. The given {instruction_unit} is as follows:\n{skeleton}"
                    }
                ]
            )
            code_snippet = response.choices[0].message.content

            generated_snippets.append(code_snippet)
            logger.info(f"Generated snippet {counter}/{len(skeletons)}")
            counter += 1
        except Exception as e:
            logger.error(f"Failed to generate snippet: {str(e)}")
            generated_snippets.append(None)
            counter += 1

    return generated_snippets

def class_level_generation():
    cls_df = pd.read_csv("../data/metadata_folder/uncontaminated_cls_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = cls_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = cls_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    cls_sample_df_filtered = cls_df[cls_df.repository_name.isin(relevant_repos)]

    #cls_sample_df_filtered = cls_sample_df_filtered.iloc[start:end, :]

    cls_sample_df_filtered.dropna(inplace=True, subset=['class_skeleton'])

    generated = generate_with_together(cls_sample_df_filtered['class_skeleton'].tolist(), model=model, granularity="class")

    cls_sample_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in cls_sample_df_filtered.columns:
        cls_sample_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)
    cls_sample_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model.split('/')[1]}_class_{start}-{end}.csv", index=False)

def func_level_generation():
    func_df = pd.read_csv("../data/metadata_folder/uncontaminated_func_1k.csv")

    start, end = int(sys.argv[1]), int(sys.argv[2])

    model = sys.argv[3]

    lower, upper = func_df.repository_name.value_counts().quantile([0.01, 0.99])

    relevant_repos = func_df.repository_name.value_counts()[lambda x: (x >= lower) & (x <= upper)].index.tolist()

    func_sample_df_filtered = func_df[func_df.repository_name.isin(relevant_repos)]

    #func_sample_df_filtered = func_sample_df_filtered.iloc[start:end, :]

    func_sample_df_filtered.dropna(inplace=True, subset=['func_signature'])

    generated = generate_with_together(granularity='function', skeletons=func_sample_df_filtered['func_signature'].tolist(), model=model)

    func_sample_df_filtered['generated_code'] = generated

    if "Unnamed: 0" in func_sample_df_filtered.columns:
        func_sample_df_filtered.drop("Unnamed: 0", axis=1, inplace=True)
    func_sample_df_filtered.to_csv(f"../data/LLM_generated_contents/uncontaminated_raw_{model.split('/')[1]}_func_{start}-{end}.csv", index=False)

if __name__ == "__main__":
    class_level_generation()
    # func_level_generation()