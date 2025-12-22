import logging
from typing import Dict, Optional

from .agent_metrics import AgentMetrics

class LoadBalancer:
    def __init__(self, orchestrator, config: Optional[Dict] = None):
        self.orchestrator = orchestrator
        self.config = config or {}
        self._metrics_history = {}
        self._setup_logging()

    def _update_metrics_history(self, metrics: Dict[str, AgentMetrics]):
        for agent_id, agent_metrics in metrics.items():
            if agent_id not in self._metrics_history:
                self._metrics_history[agent_id] = []
            self._metrics_history[agent_id].append(agent_metrics)

    def _calculate_load_trend(self, agent_id: str) -> float:
        if agent_id not in self._metrics_history or len(self._metrics_history[agent_id]) < 2:
            return 0.0
        latest_metrics = self._metrics_history[agent_id][-1]
        previous_metrics = self._metrics_history[agent_id][-2]
        return (latest_metrics.cpu_utilization - previous_metrics.cpu_utilization) / previous_metrics.cpu_utilization

    def _calculate_composite_load(self, metrics: AgentMetrics) -> float:
        return metrics.cpu_utilization + metrics.memory_utilization + metrics.network_utilization

    def _is_job_moveable(self, job: Dict) -> bool:
        return job.get('moveable', False)

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')