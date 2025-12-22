class linear1:

    def __init__(self, in_features):
        self.in_features = in_features
        self.weight = None
        self.bias = None
        self.input = None
        self.output = None

    def forward(self, x):
        """
        Forward pass: y = xW + b
        x: input of shape (batch_size, in_features)
        """
        self.input = x
        batch_size = x.shape[0]
        
        if self.weight is None:
            self.weight = [[0.0] * self.in_features for _ in range(self.in_features)]
            self.bias = [0.0] * self.in_features
        
        self.output = []
        for i in range(batch_size):
            row = []
            for j in range(self.in_features):
                val = self.bias[j]
                for k in range(self.in_features):
                    val += x[i][k] * self.weight[k][j]
                row.append(val)
            self.output.append(row)
        
        return self.output

    def backward(self, grad_output):
        """
        Backward pass
        grad_output: gradient of loss w.r.t output
        """
        batch_size = len(self.input)
        
        grad_weight = [[0.0] * self.in_features for _ in range(self.in_features)]
        grad_bias = [0.0] * self.in_features
        grad_input = [[0.0] * self.in_features for _ in range(batch_size)]
        
        for i in range(batch_size):
            for j in range(self.in_features):
                grad_bias[j] += grad_output[i][j]
                for k in range(self.in_features):
                    grad_weight[k][j] += self.input[i][k] * grad_output[i][j]
                    grad_input[i][k] += grad_output[i][j] * self.weight[k][j]
        
        return grad_input, grad_weight, grad_bias

    def update_parameters(self, grad_weight, grad_bias, learning_rate):
        """
        Update weight and bias using gradients
        """
        for i in range(self.in_features):
            self.bias[i] -= learning_rate * grad_bias[i]
            for j in range(self.in_features):
                self.weight[i][j] -= learning_rate * grad_weight[i][j]