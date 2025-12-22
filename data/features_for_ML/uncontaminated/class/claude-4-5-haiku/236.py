import anthropic
import json
from dataclasses import dataclass, field, asdict


@dataclass
class OptimizationConfig:
    """Configuration for mathematical optimization."""
    
    model: str = "claude-3-5-sonnet-20241022"
    max_iterations: int = 10
    convergence_threshold: float = 1e-6
    learning_rate: float = 0.01
    use_gradient_descent: bool = True
    random_seed: int = 42
    verbose: bool = False
    optimization_method: str = "gradient_descent"
    constraints: dict = field(default_factory=dict)
    bounds: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert configuration to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "OptimizationConfig":
        """Create configuration from dictionary."""
        return cls(**config_dict)
    
    @classmethod
    def from_json(cls, json_str: str) -> "OptimizationConfig":
        """Create configuration from JSON string."""
        config_dict = json.loads(json_str)
        return cls.from_dict(config_dict)
    
    def validate(self) -> bool:
        """Validate configuration parameters."""
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        if self.convergence_threshold <= 0:
            raise ValueError("convergence_threshold must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.optimization_method not in ["gradient_descent", "newton", "bfgs"]:
            raise ValueError("optimization_method must be one of: gradient_descent, newton, bfgs")
        return True
    
    def get_optimization_prompt(self, objective: str) -> str:
        """Generate optimization prompt for Claude."""
        config_str = self.to_json()
        prompt = f"""You are an expert mathematician and optimization specialist.

Configuration:
{config_str}

Objective:
{objective}

Please provide a detailed optimization solution considering the configuration parameters."""
        return prompt
    
    def optimize_with_claude(self, objective: str) -> str:
        """Use Claude to help with optimization based on this configuration."""
        self.validate()
        
        client = anthropic.Anthropic()
        prompt = self.get_optimization_prompt(objective)
        
        message = client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text