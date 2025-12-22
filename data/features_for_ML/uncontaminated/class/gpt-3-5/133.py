class OnnxExportArguments:
    def __init__(self, opset_version=11, target_opset=None, do_constant_folding=True, input_names=None, output_names=None):
        self.opset_version = opset_version
        self.target_opset = target_opset
        self.do_constant_folding = do_constant_folding
        self.input_names = input_names
        self.output_names = output_names

    def set_opset_version(self, opset_version):
        self.opset_version = opset_version

    def set_target_opset(self, target_opset):
        self.target_opset = target_opset

    def set_do_constant_folding(self, do_constant_folding):
        self.do_constant_folding = do_constant_folding

    def set_input_names(self, input_names):
        self.input_names = input_names

    def set_output_names(self, output_names):
        self.output_names = output_names

    def get_opset_version(self):
        return self.opset_version

    def get_target_opset(self):
        return self.target_opset

    def get_do_constant_folding(self):
        return self.do_constant_folding

    def get_input_names(self):
        return self.input_names

    def get_output_names(self):
        return self.output_names