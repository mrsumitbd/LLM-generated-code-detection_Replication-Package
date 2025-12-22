class linear1:
    def __init__(self, in_features):
        self.in_features = in_features
        self.weight = self.init_weight(in_features)
        self.bias = self.init_bias(in_features)

    def init_weight(self, in_features):
        import numpy as np
        return np.random.randn(in_features)

    def init_bias(self, in_features):
        import numpy as np
        return np.random.randn(1)

    def forward(self, x):
        import numpy as np
        return np.dot(x, self.weight) + self.bias

    def backward(self, x, grad_output):
        import numpy as np
        grad_weight = np.dot(x.T, grad_output)
        grad_bias = np.sum(grad_output, axis=0)
        grad_input = np.dot(grad_output, self.weight.T)
        return grad_input, grad_weight, grad_bias