from functools import cached_property

class AsyncAgentsResourceWithRawResponse:

    def __init__(self, agents: AsyncAgentsResource) -> None:
        pass

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        pass

    @cached_property
    def chat(self) -> AsyncChatResourceWithRawResponse:
        pass

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        pass

    @cached_property
    def evaluation_runs(self) -> AsyncEvaluationRunsResourceWithRawResponse:
        pass

    @cached_property
    def evaluation_test_cases(self) -> AsyncEvaluationTestCasesResourceWithRawResponse:
        pass

    @cached_property
    def evaluation_datasets(self) -> AsyncEvaluationDatasetsResourceWithRawResponse:
        pass

    @cached_property
    def functions(self) -> AsyncFunctionsResourceWithRawResponse:
        pass

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        pass

    @cached_property
    def knowledge_bases(self) -> AsyncKnowledgeBasesResourceWithRawResponse:
        pass

    @cached_property
    def routes(self) -> AsyncRoutesResourceWithRawResponse:
        pass