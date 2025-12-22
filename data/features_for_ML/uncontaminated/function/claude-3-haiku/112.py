async def _async_eval_runner(
    pair_eval_runner: T.Callable,
    items: T.List[core.QAPair],
    flow: Flow,
    evaluators: T.Sequence[BaseEvaluator],
    study_config: T.Union[StudyConfig, AgentStudyConfig],
    rate_limiter: AsyncLimiter,
    raise_on_exception: bool | None = EVAL__RAISE_ON_EXCEPTION,
    pruner: ParetoPruner | None = None,
    timeout_pruner: RuntimePruner | None = None,
    cost_pruner: CostPruner | None = None,
) -> T.Tuple[T.List[SyftrEvaluationResult], T.Optional[str]]:
    """Evaluate Q&A items asynchronously using provided pair_eval_runner."""
    results = []
    errors = []

    async with rate_limiter:
        for item in items:
            try:
                result = await pair_eval_runner(item, flow, evaluators, study_config)
                if pruner:
                    pruner.prune(result)
                if timeout_pruner:
                    timeout_pruner.prune(result)
                if cost_pruner:
                    cost_pruner.prune(result)
                results.append(result)
            except Exception as e:
                if raise_on_exception:
                    raise
                errors.append(str(e))

    return results, None if not errors else "\n".join(errors)