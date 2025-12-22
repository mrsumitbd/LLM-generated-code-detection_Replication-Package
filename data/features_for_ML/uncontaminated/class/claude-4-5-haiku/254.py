import os
import subprocess
import json
from pathlib import Path
import anthropic

class FallbackRepoManager:
    REPO_URL = "https://github.com/Digilent/digilent-xdc.git"
    REPO_DIR = Path.home() / ".cache" / "digilent-xdc"
    
    @staticmethod
    def read_xdc_constraints(board: str) -> str:
        """Read XDC constraints for a specific board using Claude."""
        client = anthropic.Anthropic()
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please provide the XDC (Xilinx Design Constraints) file content for the {board} board.
                    
If you have knowledge of this board's constraints, provide the complete XDC file content.
If not, provide a template XDC file with common constraint patterns for FPGA boards.

Format the response as valid XDC syntax only, without any markdown formatting or explanations."""
                }
            ]
        )
        
        return message.content[0].text
    
    @staticmethod
    def read_combined_xdc(board: str) -> str:
        """Read combined XDC constraints for a specific board using Claude."""
        client = anthropic.Anthropic()
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please provide a comprehensive combined XDC (Xilinx Design Constraints) file for the {board} board.
                    
This should include:
1. Pin assignments for all major I/O
2. Voltage standards
3. Timing constraints
4. Bank voltage specifications
5. Any board-specific constraints

If you have specific knowledge of this board, provide accurate constraints.
If not, provide a well-structured template with common patterns.

Format the response as valid XDC syntax only, without any markdown formatting or explanations."""
                }
            ]
        )
        
        return message.content[0].text
    
    @staticmethod
    def ensure_git_repo():
        """Ensure the git repository is cloned and up to date."""
        if not FallbackRepoManager.REPO_DIR.exists():
            FallbackRepoManager.REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
            try:
                subprocess.run(
                    ["git", "clone", FallbackRepoManager.REPO_URL, str(FallbackRepoManager.REPO_DIR)],
                    check=True,
                    capture_output=True,
                    timeout=30
                )
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass
        else:
            try:
                subprocess.run(
                    ["git", "-C", str(FallbackRepoManager.REPO_DIR), "pull"],
                    check=True,
                    capture_output=True,
                    timeout=30
                )
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass