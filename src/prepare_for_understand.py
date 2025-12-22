"""
Extract code from CSVs and create individual .py files for Understand analysis.

This script:
1. Creates the folder structure for features_for_ML
2. Extracts human-written and LLM-generated code from CSVs
3. Saves each code snippet as a separate .py file with unique ID as filename
"""

import pandas as pd
from pathlib import Path

def create_folder_structure(base_path='data/features_for_ML'):
    """Create the complete folder structure."""
    levels = ['class', 'function']
    llms = ['human', 'claude-3-haiku', 'claude-4-5-haiku', 'gpt-3-5', 'gpt-oss']

    for level in levels:
        for llm in llms:
            folder = Path(base_path) / level / llm
            folder.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {folder}")

    print(f"\n✅ Folder structure created at: {base_path}\n")


def extract_class_level_code(csv_path, output_base='data/features_for_ML/class'):
    """
    Extract class-level code from CSV and save as individual .py files.

    Args:
        csv_path: Path to claude-3-haiku_class_level_processed.csv
        output_base: Base output directory for class-level files
    """
    print(f"📖 Reading class-level CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    #df = df.sample(n = 14000, random_state=1234)

    print(f"   Found {len(df)} classes")

    # Extract human-written code
    human_folder = Path(output_base) / 'human'
    for idx, row in df.iterrows():
        file_id = row['id']
        code = row['human_written_code']

        if pd.notna(code) and code.strip():
            file_path = human_folder / f"{file_id}.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

    print(f"   ✓ Saved {len(df)} human-written classes to {human_folder}")

    # Extract LLM-generated code
    if "3" in csv_path and "5" not in csv_path:
        llm_folder = Path(output_base) / 'claude-3-haiku'
    elif "3" in csv_path and "5" in csv_path:
        llm_folder = Path(output_base) / 'gpt-3-5'
    elif "oss" in csv_path:
        llm_folder = Path(output_base) / 'gpt-oss'
    else:
        llm_folder = Path(output_base) / 'claude-4-5-haiku'

    for idx, row in df.iterrows():
        file_id = row['id']
        code = row['generated_code_cleaned']

        if pd.notna(code) and code.strip():
            file_path = llm_folder / f"{file_id}.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

    print(f"   ✓ Saved {len(df)} LLM-generated classes to {llm_folder}")


def extract_function_level_code(csv_path, output_base='data/features_for_ML/function'):
    """
    Extract function-level code from CSV and save as individual .py files.

    Args:
        csv_path: Path to claude-3-haiku_function_level_processed.csv
        output_base: Base output directory for function-level files
    """
    print(f"\n📖 Reading function-level CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    #df = df.sample(n=15000, random_state=1234)

    print(f"   Found {len(df)} functions")

    # Extract human-written code
    human_folder = Path(output_base) / 'human'
    for idx, row in df.iterrows():
        file_id = row['index']
        code = row['complete_extracted_code']

        if pd.notna(code) and code.strip():
            file_path = human_folder / f"{file_id}.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

    print(f"   ✓ Saved {len(df)} human-written functions to {human_folder}")

    # Extract LLM-generated code
    if "3" in csv_path and "5" not in csv_path:
        llm_folder = Path(output_base) / 'claude-3-haiku'
    elif "3" in csv_path and "5" in csv_path:
        llm_folder = Path(output_base) / 'gpt-3-5'
    elif "oss" in csv_path:
        llm_folder = Path(output_base) / 'gpt-oss'
    else:
        llm_folder = Path(output_base) / 'claude-4-5-haiku'
    for idx, row in df.iterrows():
        file_id = row['index']
        code = row['generated_code_cleaned']

        if pd.notna(code) and code.strip():
            file_path = llm_folder / f"{file_id}.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

    print(f"   ✓ Saved {len(df)} LLM-generated functions to {llm_folder}")


def verify_extraction(base_path='data/features_for_ML'):
    """Verify the extraction by counting files in each folder."""
    print("\n" + "=" * 60)
    print("📊 EXTRACTION SUMMARY")
    print("=" * 60)

    levels = ['class', 'function']
    llms = ['human', 'claude-3-haiku']

    for level in levels:
        print(f"\n{level.upper()} LEVEL:")
        for llm in llms:
            folder = Path(base_path) / level / llm
            file_count = len(list(folder.glob('*.py')))
            print(f"  {llm:20s}: {file_count:4d} files")


def main():
    """Main execution."""
    print("=" * 60)
    print("EXTRACT CODE FROM CSVs FOR UNDERSTAND ANALYSIS")
    print("=" * 60 + "\n")

    # Step 1: Create folder structure
    create_folder_structure()

    # # Step 2: Extract class-level code
    class_csv_list = ['data/LLM_generated_contents_intersection/gpt-3_5_class_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/gpt-oss_class_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/claude-3-haiku_class_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/claude-4_5-haiku_class_level_filtered.csv']
    for class_csv in class_csv_list:
        if Path(class_csv).exists():
            extract_class_level_code(class_csv)
        else:
            print(f"⚠️  Class CSV not found: {class_csv}")

    # Step 3: Extract function-level code
    func_csv_list = ['data/LLM_generated_contents_intersection/gpt-3_5_func_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/gpt-oss_func_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/claude-3-haiku_func_level_filtered.csv',
                      'data/LLM_generated_contents_intersection/claude-4_5-haiku_func_level_filtered.csv']
    for func_csv in func_csv_list:
        if Path(func_csv).exists():
            extract_function_level_code(func_csv)
        else:
            print(f"⚠️  Class CSV not found: {func_csv}")

    # Step 4: Verify extraction
    verify_extraction()

    print("\n" + "=" * 60)
    print("✅ EXTRACTION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()