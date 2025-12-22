import logging
from typing import Dict, Optional, List
from dataclasses import dataclass, field
import copy


@dataclass
class AgentMetrics:
    """Simple representation of an agent's resource usage."""
    cpu: float          # CPU usage percentage (0.0 - 100.0)
    memory: float       # Memory usage percentage (0.0 - 100.0)
    network: float      # Network usage percentage (0.0 - 100.0)
    timestamp: float = field(default_factory=lambda: 0.0)  # Unix epoch


class LoadBalancer:
    """
    A rudimentary load balancer that tracks agent metrics, computes load trends,
    and decides whether jobs can be moved between agents.
    """

    def __init__(self, orchestrator, config: Optional[Dict] = None):
        """
        Parameters
        ----------
        orchestrator
            Reference to the orchestrator that manages agents and jobs.
        config : dict, optional
            Configuration dictionary. Supported keys:
                * ``history_size``: int, number of metric snapshots to keep per agent.
                * ``log_level``: str, logging level (e.g., 'INFO', 'DEBUG').
        """
        self.orchestrator = orchestrator
        self.config = config or {}
        self.history_size: int = self.config.get("history_size", 10)
        self.metrics_history: Dict[str, List[AgentMetrics]] = {}
        self.logger = self._setup_logging()
        self.logger.debug("LoadBalancer initialized with config: %s", self.config)

    # --------------------------------------------------------------------- #
    #  Metrics handling
    # --------------------------------------------------------------------- #
    def _update_metrics_history(self, metrics: Dict[str, AgentMetrics]):
        """
        Store the latest metrics for each agent, maintaining a bounded history.

        Parameters
        ----------
        metrics : dict
            Mapping from agent_id to AgentMetrics.
        """
        for agent_id, metric in metrics.items():
            history = self.metrics_history.setdefault(agent_id, [])
            # Keep a copy to avoid accidental mutation
            history.append(copy.deepcopy(metric))
            if len(history) > self.history_size:
                history.pop(0)
        self.logger.debug("Updated metrics history: %s", self.metrics_history)

    def _calculate_load_trend(self, agent_id: str) -> float:
        """
        Compute the trend of the composite load for a given agent.

        The trend is defined as the relative change between the most recent
        and the previous composite load values.

        Parameters
        ----------
        agent_id : str
            Identifier of the agent.

        Returns
        -------
        float
            Trend value. Positive indicates increasing load, negative decreasing.
            Returns 0.0 if insufficient data.
        """
        history = self.metrics_history.get(agent_id, [])
        if len(history) < 2:
            self.logger.debug("Not enough data to compute trend for agent %s", agent_id)
            return 0.0

        prev_load = self._calculate_composite_load(history[-2])
        curr_load = self._calculate_composite_load(history[-1])

        if prev_load == 0:
            trend = curr_load
        else:
            trend = (curr_load - prev_load) / prev_load

        self.logger.debug(
            "Trend for agent %s: prev=%f, curr=%f, trend=%f",
            agent_id, prev_load, curr_load, trend
        )
        return trend

    def _calculate_composite_load(self, metrics: AgentMetrics) -> float:
        """
        Compute a weighted composite load score from raw metrics.

        Weights:
            * CPU: 0.5
            * Memory: 0.3
            * Network: 0.2

        Parameters
        ----------
        metrics : AgentMetrics
            The metrics to combine.

        Returns
        -------
        float
            Composite load score (0.0 - 100.0).
        """
        cpu_weight = 0.5
        mem_weight = 0.3
        net_weight = 0.2
        composite = (
            metrics.cpu * cpu_weight +
            metrics.memory * mem_weight +
            metrics.network * net_weight
        )
        self.logger.debug(
            "Composite load for metrics %s: %f",
            metrics, composite
        )
        return composite

    # --------------------------------------------------------------------- #
    #  Job handling
    # --------------------------------------------------------------------- #
    def _is_job_moveable(self, job: Dict) -> bool:
        """
        Determine whether a job can be moved to another agent.

        A job is considered moveable if it is not marked as critical or locked.

        Parameters
        ----------
        job : dict
            Job description. Expected keys:
                * ``critical``: bool
                * ``locked``: bool

        Returns
        -------
        bool
            True if the job can be moved, False otherwise.
        """
        critical = job.get("critical", False)
        locked = job.get("locked", False)
        moveable = not critical and not locked
        self.logger.debug(
            "Job %s moveable: %s (critical=%s, locked=%s)",
            job.get("id", "<unknown>"), moveable, critical, locked
        )
        return moveable

    # --------------------------------------------------------------------- #
    #  Logging
    # --------------------------------------------------------------------- #
    def _setup_logging(self):
        """
        Configure a logger for the LoadBalancer.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger("LoadBalancer")
        level_name = self.config.get("log_level", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        logger.setLevel(level)

        # Avoid adding multiple handlers if logger is reused
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger