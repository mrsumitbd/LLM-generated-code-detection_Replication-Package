import asyncio
from azure.ai.inference.models import ChatCompletions, EmbeddingEncodingFormat
from azure.ai.inference.aio import ChatCompletionsClient, EmbeddingsClient
from typing import Any, cast
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from benchmark_qed.config.llm_config import AuthType, LLMConfig
from benchmark_qed.llm.type.base import BaseModelOutput, BaseModelResponse, Usage

class AzureInferenceChat:
    """An Azure Chat Model provider."""

    def __init__(self, llm_config: LLMConfig) -> None:
        if llm_config.auth_type == AuthType.AzureManagedIdentity:
            credential = DefaultAzureCredential()
        else:
            credential = AzureKeyCredential(llm_config.api_key.get_secret_value())
        self._client = ChatCompletionsClient(
            endpoint=llm_config.init_args["azure_endpoint"],
            credential=credential,  # type: ignore
            **llm_config.init_args,
        )
        self._model = llm_config.model
        self._semaphore = asyncio.Semaphore(llm_config.concurrent_requests)
        self._usage = Usage(model=llm_config.model)

    def get_usage(self) -> dict[str, Any]:
        """Get the usage of the Model."""
        return self._usage.model_dump()

    async def chat(
        self, messages: list[dict[str, str]], **kwargs: dict[str, Any]
    ) -> BaseModelResponse:
        """
        Chat with the Model using the given prompt.

        Args:
            prompt: The prompt to chat with.
            kwargs: Additional arguments to pass to the Model.

        Returns
        -------
            The response from the Model.
        """
        async with self._semaphore:
            response: ChatCompletions = cast(
                ChatCompletions,
                await self._client.complete(
                    model=self._model,
                    messages=messages,
                    **kwargs,  # type: ignore
                ),  # type: ignore
            )

        content = response.choices[0].message.content.replace(
            "<|im_start|>assistant<|im_sep|>", ""
        )

        history = [
            *messages,
            {"content": content, "role": response.choices[0].message.role},
        ]

        usage_dict = {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }

        self._usage.add_usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )

        return BaseModelResponse(
            output=BaseModelOutput(
                content=content,
            ),
            history=history,
            usage=usage_dict,
        )