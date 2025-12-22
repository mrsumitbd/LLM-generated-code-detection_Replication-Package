import os
from helper.utils import load_system_prompt, load_prompt_from_file, _collect_openhands_cost, setup_openhands_credential, setup_utils_logging, safe_json_load, call_oh_with_prompt, print_exception_and_traceback, _collect_inspectai_cost

def update_submodules(repo_path: str):
    original_dir = os.getcwd()  # Save current working directory
    try:
        os.chdir(repo_path)  # Change to repo directory
        print(f"📁 Changed to repo dir: {repo_path}")

        # Sync and update submodules
        os.system("git submodule sync")
        os.system("git submodule update --init --recursive")

        print("✅ Submodules synced and updated.")
    except Exception as e:
        print_exception_and_traceback(e, prefix=f"❌ Error updating submodules")
    finally:
        os.chdir(original_dir)  # Change back to original dir
        print(f"↩️ Returned to original dir: {original_dir}")