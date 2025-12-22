import os
import subprocess

class MLIRLoweringPipeline:
    def __init__(self):
        self.required_tools = ['mlir-opt', 'mlir-translate']

    def verify_tools(self):
        for tool in self.required_tools:
            if not self.is_tool_available(tool):
                raise RuntimeError(f"Required tool '{tool}' not found.")

    def is_tool_available(self, tool):
        try:
            subprocess.check_output(['which', tool])
            return True
        except subprocess.CalledProcessError:
            return False

    def find_available_passes(self):
        passes = []
        try:
            output = subprocess.check_output(['mlir-opt', '--help-list-available-passes'])
            for line in output.decode().splitlines():
                if line.startswith('Available passes:'):
                    passes = [pass_name.strip() for pass_name in line.split(':')[1].split(',')]
                    break
        except subprocess.CalledProcessError:
            pass
        return passes

    def test_lowering_passes(self, input_file):
        passes = self.find_available_passes()
        for pass_name in passes:
            self.test_pass_sequence(input_file, [pass_name])

    def test_pass_sequence(self, input_file, passes):
        self.verify_tools()
        try:
            subprocess.check_call(['mlir-opt', input_file] + passes + ['--mlir-print-op-on-failure'])
        except subprocess.CalledProcessError:
            return False
        return True

    def create_lowered_file(self, input_file, output_file, pass_sequence):
        self.verify_tools()
        try:
            subprocess.check_call(['mlir-opt', input_file] + pass_sequence + ['--mlir-print-op-on-failure', '-o', output_file])
        except subprocess.CalledProcessError:
            return False
        return True

    def process_file(self, input_file):
        self.verify_tools()
        passes = self.find_available_passes()
        for pass_name in passes:
            output_file = os.path.splitext(input_file)[0] + f'_{pass_name}.mlir'
            if self.create_lowered_file(input_file, output_file, [pass_name]):
                print(f"Lowered file created: {output_file}")
            else:
                print(f"Failed to create lowered file: {output_file}")