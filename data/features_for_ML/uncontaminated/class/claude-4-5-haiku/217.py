class AsyncAgentsResourceWithRawResponse:

    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

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