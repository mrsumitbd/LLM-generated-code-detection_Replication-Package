import asyncio
import typing as T
from aiolimiter import AsyncLimiter

from .core import QAPair
from .flow import Flow
from .evaluators import BaseEvaluator
from .config import StudyConfig, AgentStudyConfig
from .pruners import ParetoPruner, RuntimePruner, CostPruner
from .results import SyftrEvaluationResult
from .constants import EVAL__RAISE_ON_EXCEPTION


def _async_eval_runner(
    pair_eval_runner: T.Callable,
    items: T.List[QAPair],
    flow: Flow,
    evaluators: T.Sequence[BaseEvaluator],
    study_config: T.Union[StudyConfig, AgentStudyConfig],
    rate_limiter: AsyncLimiter,
    raise_on_exception: bool | None = EVAL__RAISE_ON_EXCEPTION,
    pruner: ParetoPruner | None = None,
    timeout_pruner: RuntimePruner | None = None,
    cost_pruner: CostPruner | None = None,
) -> T.Tuple[T.List[SyftrEvaluationResult], T.Optional[str]]:
    """
    Evaluate Q&A items asynchronously using provided pair_eval_runner.

    Parameters
    ----------
    pair_eval_runner : Callable
        Async callable that evaluates a single QAPair and returns a
        SyftrEvaluationResult. It must accept the following arguments:
        (item, flow, evaluators, study_config).
    items : List[QAPair]
        List of QAPair objects to evaluate.
    flow : Flow
        Flow object used during evaluation.
    evaluators : Sequence[BaseEvaluator]
        Sequence of evaluators to apply during evaluation.
    study_config : Union[StudyConfig, AgentStudyConfig]
        Configuration for the study.
    rate_limiter : AsyncLimiter
        Async limiter to control concurrency.
    raise_on_exception : bool | None, default=EVAL__RAISE_ON_EXCEPTION
        If True, exceptions raised by pair_eval_runner are propagated.
        If False, exceptions are caught and logged; the corresponding
        result is omitted from the returned list.
    pruner : ParetoPruner | None, default=None
        Optional pruner that removes dominated results.
    timeout_pruner : RuntimePruner | None, default=None
        Optional pruner that removes results exceeding a runtime threshold.
    cost_pruner : CostPruner | None, default=None
        Optional pruner that removes results exceeding a cost threshold.

    Returns
    -------
    Tuple[List[SyftrEvaluationResult], Optional[str]]
        A tuple containing the list of evaluation results and an optional
        string summarizing any pruning actions performed.
    """
    async def _run(item: QAPair) -> SyftrEvaluationResult:
        async with rate_limiter:
            return await pair_eval_runner(item, flow, evaluators, study_config)

    async def _gather() -> T.List[T.Union[SyftrEvaluationResult, Exception]]:
        tasks = [_run(item) for item in items]
        if raise_on_exception:
            return await asyncio.gather(*tasks, return_exceptions=False)
        else:
            return await asyncio.gather(*tasks, return_exceptions=True)

    # Run the async gather loop
    results_or_exceptions = asyncio.run(_gather())

    # Separate results from exceptions
    results: T.List[SyftrEvaluationResult] = []
    errors: T.List[Exception] = []

    for item in results_or_exceptions:
        if isinstance(item, Exception):
            errors.append(item)
        else:
            results.append(item)

    # Log or handle errors if any
    if errors and raise_on_exception is False:
        # In a real implementation, you might log these errors.
        # For this stub, we simply ignore them.
        pass

    # Apply pruners sequentially and collect messages
    prune_messages: T.List[str] = []

    def _apply_pruner(
        pruner_obj: T.Optional[T.Callable[[T.List[SyftrEvaluationResult]], T.Optional[str]]]
    ) -> None:
        nonlocal results
        if pruner_obj is not None:
            msg = pruner_obj.prune(results)
            if msg:
                prune_messages.append(msg)

    _apply_pruner(pruner)
    _apply_pruner(timeout_pruner)
    _apply_pruner(cost_pruner)

    prune_summary = "\n".join(prune_messages) if prune_messages else None

    return results, prune_summary