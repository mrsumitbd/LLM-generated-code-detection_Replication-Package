import typing as T
from core import QAPair, Flow
from evaluators import BaseEvaluator
from study_config import StudyConfig, AgentStudyConfig
from async_limiter import AsyncLimiter
from pruners import ParetoPruner, RuntimePruner, CostPruner
from evaluation_result import SyftrEvaluationResult

def _async_eval_runner(
    pair_eval_runner: T.Callable,
    items: T.List[QAPair],
    flow: Flow,
    evaluators: T.Sequence[BaseEvaluator],
    study_config: T.Union[StudyConfig, AgentStudyConfig],
    rate_limiter: AsyncLimiter,
    raise_on_exception: bool = EVAL__RAISE_ON_EXCEPTION,
    pruner: ParetoPruner = None,
    timeout_pruner: RuntimePruner = None,
    cost_pruner: CostPruner = None,
) -> T.Tuple[T.List[SyftrEvaluationResult], T.Optional[str]]:
    """Evaluate Q&A items asynchronously using provided pair_eval_runner."""
    pass