def _async_eval_runner(
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
    import asyncio
    
    async def run_async():
        tasks = []
        for item in items:
            task = pair_eval_runner(
                item=item,
                flow=flow,
                evaluators=evaluators,
                study_config=study_config,
                rate_limiter=rate_limiter,
                raise_on_exception=raise_on_exception,
                pruner=pruner,
                timeout_pruner=timeout_pruner,
                cost_pruner=cost_pruner,
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        evaluation_results = []
        error_message = None
        
        for result in results:
            if isinstance(result, Exception):
                if raise_on_exception:
                    raise result
                error_message = str(result)
            else:
                evaluation_results.append(result)
        
        return evaluation_results, error_message
    
    return asyncio.run(run_async())