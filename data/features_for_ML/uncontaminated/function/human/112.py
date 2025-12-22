import math
import numpy as np
from llama_index.core.evaluation import BaseEvaluator, CorrectnessEvaluator
from syftr import core, custom_metrics
import asyncio
import typing as T
from aiolimiter import AsyncLimiter
from syftr.pruning import CostPruner, ParetoPruner, RuntimePruner
from syftr.configuration import EVAL__RAISE_ON_EXCEPTION
from syftr.flows import Flow, JudgeFlow, RetrieverFlow
from syftr.studies import AgentStudyConfig, SearchSpace, StudyConfig

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
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    prune_reason = None
    results = []
    batch_size = study_config.optimization.num_eval_batch
    num_batches = math.ceil(len(items) / batch_size)
    batches = [items[i : i + batch_size] for i in range(0, len(items), batch_size)]
    for i, batch in enumerate(batches):
        batch_result = loop.run_until_complete(
            _aeval_all_pair_runner(
                pair_eval_runner,
                list(batch),
                flow,
                evaluators,
                study_config.timeouts.single_eval_timeout,
                rate_limiter,
                raise_on_exception,
            )
        )
        results.extend(batch_result)
        run_times = [
            r.run_time for r in results if r and r.run_time and not np.isnan(r.run_time)
        ]
        # Compute stats and pruners if we have successful evals
        # or, if we are over the max fail rate, proceed to calculate_metrics, which will
        # error out if we don't have any successful trials.
        # max_eval_failure_rate only applies if there are zero successful evals so far
        if (
            run_times
            or i / num_batches > study_config.optimization.max_eval_failure_rate
        ):
            current_metrics = calculate_metrics(results, study_config)

            log.info(
                "Finished evaluation batch %s/%s with %s QA pairs. Metrics: %s, Flow: %s",
                i + 1,
                num_batches,
                len(batch),
                {
                    current_metrics["objective_1_name"]: current_metrics["obj1_value"],
                    current_metrics["objective_2_name"]: current_metrics["obj2_value"],
                    "num_errors": current_metrics["num_errors"],
                },
                flow,
            )

            if timeout_pruner:
                timeout_pruner.report_and_raise_on_prune(
                    step=(i + 1) * study_config.optimization.num_eval_batch,
                    p80_time=current_metrics["p80_time"],
                )

            if cost_pruner:
                cost_pruner.report_and_raise_on_prune(
                    step=(i + 1) * study_config.optimization.num_eval_batch,
                    total_cost=current_metrics["llm_cost_total"],
                    llm_cost_mean=current_metrics["llm_cost_mean"],
                )
            if pruner:
                if pruner.report_and_prune(
                    step=(i + 1) * study_config.optimization.num_eval_batch,
                    obj1=current_metrics["obj1_value"],
                    obj2=current_metrics["obj2_value"],
                    obj1_confidence=current_metrics["obj1_confidence"],
                    obj2_confidence=current_metrics["obj2_confidence"],
                ):
                    prune_reason = "pareto"
                    break
    return results, prune_reason