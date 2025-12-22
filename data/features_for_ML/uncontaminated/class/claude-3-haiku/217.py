from functools import cached_property

class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self.agents = agents

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        return AsyncAPIKeysResourceWithRawResponse(self.agents.api_keys)

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        return AsyncChatResourceWithRawResponse(self.agents.chat)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        return AsyncEvaluationMetricsResourceWithRawResponse(self.agents.evaluation_metrics)

    @cached_property
    def evaluation_runs(self) -> AsyncEvaluationRunsResourceWithRawResponse:
        return AsyncEvaluationRunsResourceWithRawResponse(self.agents.evaluation_runs)

    @cached_property
    def evaluation_test_cases(self) -> AsyncEvaluationTestCasesResourceWithRawResponse:
        return AsyncEvaluationTestCasesResourceWithRawResponse(self.agents.evaluation_test_cases)

    @cached_property
    def evaluation_datasets(self) -> AsyncEvaluationDatasetsResourceWithRawResponse:
        return AsyncEvaluationDatasetsResourceWithRawResponse(self.agents.evaluation_datasets)

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithRawResponse:
        return AsyncFunctionsResourceWithRawResponse(self.agents.functions)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self.agents.versions)

    @cached_property
    def knowledge_bases(self) -> AsyncKnowledgeBasesResourceWithRawResponse:
        return AsyncKnowledgeBasesResourceWithRawResponse(self.agents.knowledge_bases)

    @cached_property
    def routes(self) -> AsyncRoutesResourceWithRawResponse:
        return AsyncRoutesResourceWithRawResponse(self.agents.routes)