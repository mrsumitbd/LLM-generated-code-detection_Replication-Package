"""
Global Intersection for Uncontaminated Dataset
Finds prompts where ALL 4 LLMs successfully generated code
"""

import pandas as pd
from utility import post_process_batch_results

# File paths
BASE_PATH = "../data/LLM_generated_contents"

FILES = {
    'function': {
        'claude-3-haiku': f"{BASE_PATH}/uncontaminated_raw_claude-3-haiku-20240307_func_0-1000.csv",
        'claude-4-5-haiku': f"{BASE_PATH}/uncontaminated_raw_claude-haiku-4-5_func_0-1000.csv",
        'gpt-3-5': f"{BASE_PATH}/uncontaminated_raw_gpt-3.5-turbo-0125_func_0-1000.csv",
        'gpt-oss': f"{BASE_PATH}/uncontaminated_raw_gpt-oss-20b_func_0-1000.csv",
    },
    'class': {
        'claude-3-haiku': f"{BASE_PATH}/uncontaminated_raw_claude-3-haiku-20240307_class_0-1000.csv",
        'claude-4-5-haiku': f"{BASE_PATH}/uncontaminated_raw_claude-haiku-4-5_class_0-1000.csv",
        'gpt-3-5': f"{BASE_PATH}/uncontaminated_raw_gpt-3.5-turbo-0125_class_0-1000.csv",
        'gpt-oss': f"{BASE_PATH}/uncontaminated_raw_gpt-oss-20b_class_0-1000.csv",
    }
}

# Column names for human-written code
HUMAN_CODE_COLUMNS = {
    'function': 'complete_extracted_code',
    'class': 'human_writted_class'  # Note: typo in original column name
}

print("=" * 80)
print("UNCONTAMINATED DATASET - GLOBAL INTERSECTION ANALYSIS")
print("=" * 80)

results = {}

for granularity in ['function', 'class']:
    print(f"\n{'=' * 80}")
    print(f"{granularity.upper()}-LEVEL ANALYSIS")
    print(f"{'=' * 80}")

    # Load all 4 LLM datasets
    dfs = {}
    human_code_col = HUMAN_CODE_COLUMNS[granularity]

    for model, filepath in FILES[granularity].items():
        print(f"\nLoading {model}...")
        df = pd.read_csv(filepath)

        print(f"  Total rows: {len(df)}")

        # Check for generated_code column
        if 'generated_code' not in df.columns:
            print(f"  ERROR: 'generated_code' column not found!")
            print(f"  Available columns: {df.columns.tolist()}")
            continue

        # Apply post-processing to extract clean code
        print(f"  Applying post-processing to extract clean code...")
        raw_code = df['generated_code'].fillna('').tolist()
        processed_code = post_process_batch_results(raw_code, validate_syntax=True)
        df['processed_code'] = processed_code

        # Check for valid processed code (not None and not empty)
        df['has_valid_code'] = df['processed_code'].notna() & (df['processed_code'] != '')
        valid = df['has_valid_code'].sum()
        invalid = len(df) - valid

        print(f"  Valid after post-processing: {valid} ({valid / len(df) * 100:.1f}%)")
        print(f"  Invalid/filtered out: {invalid} ({invalid / len(df) * 100:.1f}%)")

        dfs[model] = df

    # Create composite keys for intersection
    # For functions: repository_name + path + func_name
    # For classes: repository_name + path + class_name

    print(f"\n{'-' * 80}")
    print("Creating composite keys...")
    print(f"{'-' * 80}")

    for model, df in dfs.items():
        if granularity == 'function':
            # Check which key columns exist
            if 'func_name' in df.columns:
                df['composite_key'] = df['repository_name'].astype(str) + '|||' + \
                                      df['path'].astype(str) + '|||' + \
                                      df['func_name'].astype(str)
            else:
                print(f"  WARNING: 'func_name' not found in {model}, checking alternatives...")
                print(f"  Available columns: {df.columns.tolist()}")
                # Try to use path as key if func_name doesn't exist
                df['composite_key'] = df['repository_name'].astype(str) + '|||' + \
                                      df['path'].astype(str)
        else:  # class
            df['composite_key'] = df['repository_name'].astype(str) + '|||' + \
                                  df['path'].astype(str) + '|||' + \
                                  df['class_name'].astype(str)

        print(f"  {model}: {len(df)} total, {df['composite_key'].nunique()} unique keys")

    # Find intersection: composite keys present in ALL 4 models
    print(f"\n{'-' * 80}")
    print("Computing intersection...")
    print(f"{'-' * 80}")

    # Get valid keys (with processed code) for each model
    valid_keys = {}
    for model, df in dfs.items():
        valid_df = df[df['has_valid_code']]
        valid_keys[model] = set(valid_df['composite_key'].values)
        print(f"  {model}: {len(valid_keys[model])} valid keys (post-processed)")

    # Intersection: keys present in ALL 4 models
    intersection_keys = valid_keys['claude-3-haiku']
    for model in ['claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
        intersection_keys = intersection_keys.intersection(valid_keys[model])

    print(f"\n  INTERSECTION: {len(intersection_keys)} keys present in ALL 4 models")
    print(f"  Retention rate: {len(intersection_keys) / 1000 * 100:.1f}% of original 1000")

    # Store results
    results[granularity] = {
        'intersection_size': len(intersection_keys),
        'intersection_keys': intersection_keys,
        'original_size': 1000,
        'retention_rate': len(intersection_keys) / 1000 * 100
    }

    # Show breakdown by model
    print(f"\n{'-' * 80}")
    print("Loss breakdown:")
    print(f"{'-' * 80}")
    for model in ['claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']:
        lost = 1000 - len(valid_keys[model])
        print(f"  {model}: Lost {lost} ({lost / 10:.1f}%)")

    # Calculate intersection loss
    union_size = len(set.union(*valid_keys.values()))
    intersection_loss = union_size - len(intersection_keys)
    print(f"\n  Total union: {union_size}")
    print(f"  Lost to intersection requirement: {intersection_loss} ({intersection_loss / union_size * 100:.1f}%)")

# Summary report
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

print(f"\nFunction-level:")
print(f"  Original dataset: 1,000 functions")
print(f"  Intersection: {results['function']['intersection_size']} functions")
print(f"  Retention: {results['function']['retention_rate']:.1f}%")

print(f"\nClass-level:")
print(f"  Original dataset: 1,000 classes")
print(f"  Intersection: {results['class']['intersection_size']} classes")
print(f"  Retention: {results['class']['retention_rate']:.1f}%")

print(
    f"\nTotal intersection samples: {results['function']['intersection_size'] + results['class']['intersection_size']}")

# Save intersection keys to files
print("\n" + "=" * 80)
print("SAVING INTERSECTION KEYS")
print("=" * 80)

for granularity in ['function', 'class']:
    output_file = f"../data/uncontaminated_intersection_keys_{granularity}.txt"
    with open(output_file, 'w') as f:
        for key in sorted(results[granularity]['intersection_keys']):
            f.write(key + '\n')
    print(f"  {granularity.capitalize()}: {output_file}")

print("\n" + "=" * 80)
print("COMPARISON TO MAIN DATASET")
print("=" * 80)

print(f"\nMain dataset (CodeSearchNet-based):")
print(f"  Functions: 14,485")
print(f"  Classes: 11,913")

print(f"\nUncontaminated dataset:")
print(f"  Functions: {results['function']['intersection_size']}")
print(f"  Classes: {results['class']['intersection_size']}")

print(f"\nSize ratio (uncontaminated / main):")
print(f"  Functions: {results['function']['intersection_size'] / 14485 * 100:.1f}%")
print(f"  Classes: {results['class']['intersection_size'] / 11913 * 100:.1f}%")

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)