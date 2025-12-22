class LoadBalancer:

    def __init__(self, orchestrator, config: Optional[Dict] = None):
        self.orchestrator = orchestrator
        self.config = config or {}
        self.metrics_history = {}
        self.history_size = self.config.get('history_size', 100)
        self.load_threshold_high = self.config.get('load_threshold_high', 0.8)
        self.load_threshold_low = self.config.get('load_threshold_low', 0.3)
        self.trend_weight = self.config.get('trend_weight', 0.2)
        self.cpu_weight = self.config.get('cpu_weight', 0.4)
        self.memory_weight = self.config.get('memory_weight', 0.3)
        self.job_count_weight = self.config.get('job_count_weight', 0.3)
        self._setup_logging()

    def _update_metrics_history(self, metrics: Dict[str, AgentMetrics]):
        for agent_id, agent_metrics in metrics.items():
            if agent_id not in self.metrics_history:
                self.metrics_history[agent_id] = []
            
            self.metrics_history[agent_id].append(agent_metrics)
            
            if len(self.metrics_history[agent_id]) > self.history_size:
                self.metrics_history[agent_id].pop(0)

    def _calculate_load_trend(self, agent_id: str) -> float:
        if agent_id not in self.metrics_history or len(self.metrics_history[agent_id]) < 2:
            return 0.0
        
        history = self.metrics_history[agent_id]
        if len(history) < 2:
            return 0.0
        
        recent_load = self._calculate_composite_load(history[-1])
        previous_load = self._calculate_composite_load(history[-2])
        
        trend = recent_load - previous_load
        return trend

    def _calculate_composite_load(self, metrics: AgentMetrics) -> float:
        cpu_load = getattr(metrics, 'cpu_usage', 0.0) / 100.0
        memory_load = getattr(metrics, 'memory_usage', 0.0) / 100.0
        job_count = getattr(metrics, 'active_jobs', 0)
        max_jobs = getattr(metrics, 'max_jobs', 1)
        
        job_load = job_count / max_jobs if max_jobs > 0 else 0.0
        
        composite_load = (
            self.cpu_weight * cpu_load +
            self.memory_weight * memory_load +
            self.job_count_weight * job_load
        )
        
        return min(1.0, max(0.0, composite_load))

    def _is_job_moveable(self, job: Dict) -> bool:
        if not isinstance(job, dict):
            return False
        
        moveable = job.get('moveable', True)
        if not moveable:
            return False
        
        job_type = job.get('type', '')
        non_moveable_types = self.config.get('non_moveable_job_types', [])
        if job_type in non_moveable_types:
            return False
        
        return True

    def _setup_logging(self):
        import logging
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)