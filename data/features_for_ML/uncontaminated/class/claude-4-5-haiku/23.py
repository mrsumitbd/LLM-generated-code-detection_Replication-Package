class AzureInferenceChat:
    """An Azure Chat Model provider."""

    def __init__(self, llm_config: LLMConfig) -> None:
        self.llm_config = llm_config
        self.client = None
        self.usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the Azure inference client."""
        try:
            from azure.ai.inference import ChatCompletionsClient
            from azure.core.credentials import AzureKeyCredential
            
            endpoint = self.llm_config.api_base
            api_key = self.llm_config.api_key
            
            self.client = ChatCompletionsClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(api_key)
            )
        except ImportError:
            raise ImportError("azure-ai-inference package is required")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Azure client: {e}")

    def get_usage(self) -> dict[str, Any]:
        return self.usage.copy()