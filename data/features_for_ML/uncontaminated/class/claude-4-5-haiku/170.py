import subprocess
import os
import re
from pathlib import Path

class MLIRLoweringPipeline:

    def __init__(self):
        self.mlir_opt_path = None
        self.available_passes = []
        self.working_passes = []

    def verify_tools(self):
        """Verify that mlir-opt is available in the system."""
        try:
            result = subprocess.run(['mlir-opt', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                self.mlir_opt_path = 'mlir-opt'
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return False

    def find_available_passes(self):
        """Find all available MLIR passes."""
        if not self.mlir_opt_path:
            return []
        
        try:
            result = subprocess.run([self.mlir_opt_path, '--help'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            # Extract pass names from help output
            pass_pattern = r'--(\w+(?:-\w+)*)\s'
            matches = re.findall(pass_pattern, result.stdout)
            
            self.available_passes = list(set(matches))
            return self.available_passes
        except (subprocess.TimeoutExpired, Exception):
            return []

    def test_lowering_passes(self, input_file):
        """Test individual lowering passes on the input file."""
        if not os.path.exists(input_file):
            return {}
        
        results = {}
        
        for pass_name in self.available_passes:
            results[pass_name] = self.test_pass_sequence(input_file, [pass_name])
        
        self.working_passes = [p for p, success in results.items() if success]
        return results

    def test_pass_sequence(self, input_file, passes):
        """Test a sequence of passes on the input file."""
        if not os.path.exists(input_file):
            return False
        
        try:
            cmd = [self.mlir_opt_path]
            for pass_name in passes:
                cmd.append(f'--{pass_name}')
            cmd.append(input_file)
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False

    def create_lowered_file(self, input_file, output_file, pass_sequence):
        """Create a lowered MLIR file by applying a sequence of passes."""
        if not os.path.exists(input_file):
            return False
        
        try:
            cmd = [self.mlir_opt_path]
            for pass_name in pass_sequence:
                cmd.append(f'--{pass_name}')
            cmd.append(input_file)
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)
            
            if result.returncode == 0:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                return True
            return False
        except (subprocess.TimeoutExpired, Exception):
            return False

    def process_file(self, input_file):
        """Process an MLIR file through the complete pipeline."""
        if not self.verify_tools():
            return None
        
        if not os.path.exists(input_file):
            return None
        
        self.find_available_passes()
        
        if not self.available_passes:
            return None
        
        # Test passes and find working ones
        self.test_lowering_passes(input_file)
        
        if not self.working_passes:
            return None
        
        # Create output file with working passes
        base_name = Path(input_file).stem
        output_file = f"{base_name}_lowered.mlir"
        
        success = self.create_lowered_file(input_file, output_file, self.working_passes)
        
        if success:
            return output_file
        return None