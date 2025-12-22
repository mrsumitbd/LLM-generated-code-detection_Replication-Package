from functools import cached_property

# Import the raw‑response wrapper classes.  These imports assume that the
# corresponding modules are available in the same package or in the import
# path.  Adjust the import paths if necessary.
from .api_keys import AsyncAPIKeysResourceWithRawResponse
from .chat import AsyncChatResourceWithRawResponse
from .evaluation_metrics import AsyncEvaluationMetricsResourceWithRawResponse
from .evaluation_runs import AsyncEvaluationRunsResourceWithRawResponse
from .evaluation_test_cases import AsyncEvaluationTestCasesResourceWithRawResponse
from .evaluation_datasets import AsyncEvaluationDatasetsResourceWithRawResponse
from .functions import AsyncFunctionsResourceWithRawResponse
from .versions import AsyncVersionsResourceWithRawResponse
from .knowledge_bases import AsyncKnowledgeBasesResourceWithRawResponse
from .routes import AsyncRoutesResourceWithRawResponse

class AsyncAgentsResourceWithRawResponse:
    """
    A wrapper around :class:`AsyncAgentsResource` that exposes the same
    sub‑resources but returns the raw‑response versions of those resources.
    """

    def __init__(self, agents: "AsyncAgentsResource") -> None:
        """
        Parameters
        ----------
        agents
            The underlying :class:`AsyncAgentsResource` instance.
        """
        self._agents = agents

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        """Return the raw‑response API keys resource."""
        return AsyncAPIKeysResourceWithRawResponse(self._agents.api_keys)

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        """Return the raw‑response chat resource."""
        return AsyncChatResourceWithRawResponse(self._agents.chat)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        """Return the raw‑response evaluation metrics resource."""
        return AsyncEvaluationMetricsResourceWithRawResponse(self._agents.evaluation_metrics)

    @cached_property
    def evaluation_runs(self) -> AsyncEvaluationRunsResourceWithRawResponse:
        """Return the raw‑response evaluation runs resource."""
        return AsyncEvaluationRunsResourceWithRawResponse(self._agents.evaluation_runs)

    @cached_property
    def evaluation_test_cases(self) -> AsyncEvaluationTestCasesResourceWithRawResponse:
        """Return the raw‑response evaluation test cases resource."""
        return AsyncEvaluationTestCasesResourceWithRawResponse(self._agents.evaluation_test_cases)

    @cached_property
    def evaluation_datasets(self) -> AsyncEvaluationDatasetsResourceWithRawResponse:
        """Return the raw‑response evaluation datasets resource."""
        return AsyncEvaluationDatasetsResourceWithRawResponse(self._agents.evaluation_datasets)

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithRawResponse:
        """Return the raw‑response functions resource."""
        return AsyncFunctionsResourceWithRawResponse(self._agents.functions)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        """Return the raw‑response versions resource."""
        return AsyncVersionsResourceWithRawResponse(self._agents.versions)

    @cached_property
    def knowledge_bases(self) -> AsyncKnowledgeBasesResourceWithRawResponse:
        """Return the raw‑response knowledge bases resource."""
        return AsyncKnowledgeBasesResourceWithRawResponse(self._agents.knowledge_bases)

    @cached_property
    def routes(self) -> AsyncRoutesResourceWithRawResponse:
        """Return the raw‑response routes resource."""
        return AsyncRoutesResourceWithRawResponse(self._agents.routes)