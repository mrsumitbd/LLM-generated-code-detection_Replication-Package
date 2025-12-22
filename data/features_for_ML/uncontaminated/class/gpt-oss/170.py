import os
import subprocess
import shutil
from typing import List, Dict, Tuple, Optional


class MLIRLoweringPipeline:
    def __init__(self, mlir_opt: Optional[str] = None, mlir_translate: Optional[str] = None):
        """
        Initialize the pipeline with optional custom paths for mlir-opt and mlir-translate.
        If not provided, the executables are searched in the system PATH.
        """
        self.mlir_opt_path = mlir_opt or shutil.which("mlir-opt")
        self.mlir_translate_path = mlir_translate or shutil.which("mlir-translate")
        self.available_passes: List[str] = []

    def verify_tools(self) -> None:
        """
        Verify that mlir-opt and mlir-translate are available.
        Raises RuntimeError if either is missing.
        """
        missing = []
        if not self.mlir_opt_path:
            missing.append("mlir-opt")
        if not self.mlir_translate_path:
            missing.append("mlir-translate")
        if missing:
            raise RuntimeError(f"Missing required tools: {', '.join(missing)}")

    def find_available_passes(self) -> List[str]:
        """
        Discover available MLIR passes by invoking `mlir-opt --passes`.
        Returns a list of pass names.
        """
        self.verify_tools()
        try:
            result = subprocess.run(
                [self.mlir_opt_path, "--passes"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to list passes: {e.stderr}") from e

        passes = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("-"):
                pass_name = line.lstrip("-").strip()
                if pass_name:
                    passes.append(pass_name)
        self.available_passes = passes
        return passes

    def _run_pass(self, passes: List[str], input_file: str, output_file: str) -> Tuple[int, str, str]:
        """
        Internal helper to run mlir-opt with a list of passes.
        Returns (returncode, stdout, stderr).
        """
        cmd = [self.mlir_opt_path, "-passes=" + ",".join(passes), input_file, "-o", output_file]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr

    def test_lowering_passes(self, input_file: str) -> Dict[str, Tuple[int, str, str]]:
        """
        Test each available pass individually on the input file.
        Returns a dictionary mapping pass name to (returncode, stdout, stderr).
        """
        if not self.available_passes:
            self.find_available_passes()
        results = {}
        for p in self.available_passes:
            rc, out, err = self._run_pass([p], input_file, "/dev/null")
            results[p] = (rc, out, err)
        return results

    def test_pass_sequence(self, input_file: str, passes: List[str]) -> Tuple[int, str, str]:
        """
        Test a sequence of passes on the input file.
        Returns (returncode, stdout, stderr).
        """
        return self._run_pass(passes, input_file, "/dev/null")

    def create_lowered_file(self, input_file: str, output_file: str, pass_sequence: List[str]) -> None:
        """
        Apply a sequence of passes to the input file and write the result to output_file.
        Raises RuntimeError if the lowering fails.
        """
        rc, out, err = self._run_pass(pass_sequence, input_file, output_file)
        if rc != 0:
            raise RuntimeError(f"Lowering failed:\n{err}")

    def process_file(self, input_file: str, output_file: str, pass_sequence: Optional[List[str]] = None) -> None:
        """
        Convenience method to process a file: verifies tools, discovers passes if needed,
        and creates a lowered file using the provided pass sequence or a default.
        """
        self.verify_tools()
        if not self.available_passes:
            self.find_available_passes()
        if pass_sequence is None:
            # Default sequence: canonicalize followed by cse if available
            default = ["canonicalize"]
            if "cse" in self.available_passes:
                default.append("cse")
            pass_sequence = default
        self.create_lowered_file(input_file, output_file, pass_sequence)