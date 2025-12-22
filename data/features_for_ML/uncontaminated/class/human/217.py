from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .evaluation_runs import (
    EvaluationRunsResource,
    AsyncEvaluationRunsResource,
    EvaluationRunsResourceWithRawResponse,
    AsyncEvaluationRunsResourceWithRawResponse,
    EvaluationRunsResourceWithStreamingResponse,
    AsyncEvaluationRunsResourceWithStreamingResponse,
)
from .evaluation_test_cases import (
    EvaluationTestCasesResource,
    AsyncEvaluationTestCasesResource,
    EvaluationTestCasesResourceWithRawResponse,
    AsyncEvaluationTestCasesResourceWithRawResponse,
    EvaluationTestCasesResourceWithStreamingResponse,
    AsyncEvaluationTestCasesResourceWithStreamingResponse,
)
from .evaluation_datasets import (
    EvaluationDatasetsResource,
    AsyncEvaluationDatasetsResource,
    EvaluationDatasetsResourceWithRawResponse,
    AsyncEvaluationDatasetsResourceWithRawResponse,
    EvaluationDatasetsResourceWithStreamingResponse,
    AsyncEvaluationDatasetsResourceWithStreamingResponse,
)
from .functions import (
    FunctionsResource,
    AsyncFunctionsResource,
    FunctionsResourceWithRawResponse,
    AsyncFunctionsResourceWithRawResponse,
    FunctionsResourceWithStreamingResponse,
    AsyncFunctionsResourceWithStreamingResponse,
)
from .evaluation_metrics.evaluation_metrics import (
    EvaluationMetricsResource,
    AsyncEvaluationMetricsResource,
    EvaluationMetricsResourceWithRawResponse,
    AsyncEvaluationMetricsResourceWithRawResponse,
    EvaluationMetricsResourceWithStreamingResponse,
    AsyncEvaluationMetricsResourceWithStreamingResponse,
)
from .chat.chat import (
    ChatResource,
    AsyncChatResource,
    ChatResourceWithRawResponse,
    AsyncChatResourceWithRawResponse,
    ChatResourceWithStreamingResponse,
    AsyncChatResourceWithStreamingResponse,
)
from .routes import (
    RoutesResource,
    AsyncRoutesResource,
    RoutesResourceWithRawResponse,
    AsyncRoutesResourceWithRawResponse,
    RoutesResourceWithStreamingResponse,
    AsyncRoutesResourceWithStreamingResponse,
)
from .api_keys import (
    APIKeysResource,
    AsyncAPIKeysResource,
    APIKeysResourceWithRawResponse,
    AsyncAPIKeysResourceWithRawResponse,
    APIKeysResourceWithStreamingResponse,
    AsyncAPIKeysResourceWithStreamingResponse,
)
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .knowledge_bases import (
    KnowledgeBasesResource,
    AsyncKnowledgeBasesResource,
    KnowledgeBasesResourceWithRawResponse,
    AsyncKnowledgeBasesResourceWithRawResponse,
    KnowledgeBasesResourceWithStreamingResponse,
    AsyncKnowledgeBasesResourceWithStreamingResponse,
)

class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.create = async_to_raw_response_wrapper(
            agents.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            agents.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            agents.update,
        )
        self.list = async_to_raw_response_wrapper(
            agents.list,
        )
        self.delete = async_to_raw_response_wrapper(
            agents.delete,
        )
        self.retrieve_usage = async_to_raw_response_wrapper(
            agents.retrieve_usage,
        )
        self.update_status = async_to_raw_response_wrapper(
            agents.update_status,
        )
        self.wait_until_ready = async_to_raw_response_wrapper(
            agents.wait_until_ready,
        )

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        return AsyncAPIKeysResourceWithRawResponse(self._agents.api_keys)

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        return AsyncChatResourceWithRawResponse(self._agents.chat)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        return AsyncEvaluationMetricsResourceWithRawResponse(self._agents.evaluation_metrics)

    @cached_property
    def evaluation_runs(self) -> AsyncEvaluationRunsResourceWithRawResponse:
        return AsyncEvaluationRunsResourceWithRawResponse(self._agents.evaluation_runs)

    @cached_property
    def evaluation_test_cases(self) -> AsyncEvaluationTestCasesResourceWithRawResponse:
        return AsyncEvaluationTestCasesResourceWithRawResponse(self._agents.evaluation_test_cases)

    @cached_property
    def evaluation_datasets(self) -> AsyncEvaluationDatasetsResourceWithRawResponse:
        return AsyncEvaluationDatasetsResourceWithRawResponse(self._agents.evaluation_datasets)

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithRawResponse:
        return AsyncFunctionsResourceWithRawResponse(self._agents.functions)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._agents.versions)

    @cached_property
    def knowledge_bases(self) -> AsyncKnowledgeBasesResourceWithRawResponse:
        return AsyncKnowledgeBasesResourceWithRawResponse(self._agents.knowledge_bases)

    @cached_property
    def routes(self) -> AsyncRoutesResourceWithRawResponse:
        return AsyncRoutesResourceWithRawResponse(self._agents.routes)